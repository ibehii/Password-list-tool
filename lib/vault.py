#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  ____________________________________________
"""Secure encrypted SQLite password vault.

Implements PBKDF2HMAC (SHA-256) key derivation and AES-256 authenticated encryption (Fernet).
Includes clipboard auto-clear, backup export/import (JSON/CSV), secure file permissions,
and automatic migration from legacy unencrypted password tables.
"""

from __future__ import annotations

import base64
import csv
import json
import os
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CANARY_STRING = "VAULT_CANARY_AUTHENTICATED_TOKEN_V2"
PBKDF2_ITERATIONS = 200_000
DEFAULT_DB_DIR = Path(__file__).resolve().parent / "db"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / ".passwords.db"


class VaultError(Exception):
    """Base exception for password vault errors."""


class InvalidMasterPasswordError(VaultError):
    """Raised when the provided master password fails decryption/verification."""


class VaultNotInitializedError(VaultError):
    """Raised when trying to unlock an uninitialized vault."""


def derive_encryption_key(master_password: str, salt_bytes: bytes) -> bytes:
    """Derive a URL-safe base64 32-byte Fernet key from master password and salt."""
    key_derivation = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=PBKDF2_ITERATIONS,
    )
    derived_raw_key = key_derivation.derive(master_password.encode("utf-8"))
    return base64.urlsafe_b64encode(derived_raw_key)


class PasswordVault:
    """Encrypted SQLite vault manager."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path).resolve() if db_path else DEFAULT_DB_PATH
        self._fernet: Optional[Fernet] = None
        self._master_salt: Optional[bytes] = None

    @property
    def is_unlocked(self) -> bool:
        """Check if vault currently has an active encryption key."""
        return self._fernet is not None

    def exists(self) -> bool:
        """Check if the database file exists."""
        return self.db_path.exists()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Open a database connection ensuring restrictive permissions and guaranteed closure."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            if self.db_path.exists():
                try:
                    os.chmod(self.db_path, 0o600)
                except OSError:
                    pass
            with connection:
                yield connection
        finally:
            connection.close()

    def is_legacy_unencrypted(self) -> bool:
        """Detect whether the database has old unencrypted schema without vault_meta."""
        if not self.exists():
            return False
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vault_meta'")
            has_vault_meta = cursor.fetchone() is not None
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password'")
            has_old_table = cursor.fetchone() is not None
            return (not has_vault_meta) and has_old_table

    def is_initialized(self) -> bool:
        """Check if vault has been initialized with vault_meta."""
        if not self.exists():
            return False
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vault_meta'")
            return cursor.fetchone() is not None

    def initialize_vault(self, master_password: str) -> None:
        """Initialize a new encrypted vault with master password."""
        if not master_password:
            raise ValueError("Master password cannot be empty")

        salt_bytes = secrets.token_bytes(16)
        encryption_key = derive_encryption_key(master_password, salt_bytes)
        fernet = Fernet(encryption_key)
        verifier_token = fernet.encrypt(CANARY_STRING.encode("utf-8")).decode("utf-8")

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault_meta (
                    meta_key TEXT PRIMARY KEY,
                    meta_value TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    creation_date TEXT NOT NULL,
                    reminder TEXT
                )
            """)
            cursor.execute("INSERT OR REPLACE INTO vault_meta VALUES ('salt', ?)", (salt_bytes.hex(),))
            cursor.execute("INSERT OR REPLACE INTO vault_meta VALUES ('verifier', ?)", (verifier_token,))
            connection.commit()

        self._fernet = fernet
        self._master_salt = salt_bytes

    def unlock(self, master_password: str) -> bool:
        """Unlock vault with master password and verify canary token."""
        if not self.is_initialized():
            raise VaultNotInitializedError("Vault is not initialized yet.")

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT meta_value FROM vault_meta WHERE meta_key = 'salt'")
            salt_row = cursor.fetchone()
            cursor.execute("SELECT meta_value FROM vault_meta WHERE meta_key = 'verifier'")
            verifier_row = cursor.fetchone()

        if not salt_row or not verifier_row:
            raise VaultError("Vault metadata is corrupted or incomplete.")

        salt_bytes = bytes.fromhex(salt_row[0])
        encryption_key = derive_encryption_key(master_password, salt_bytes)
        fernet = Fernet(encryption_key)

        try:
            decrypted_canary = fernet.decrypt(verifier_row[0].encode("utf-8")).decode("utf-8")
            if decrypted_canary != CANARY_STRING:
                raise InvalidMasterPasswordError("Master password check failed.")
        except InvalidToken as exc:
            raise InvalidMasterPasswordError("Invalid master password.") from exc

        self._fernet = fernet
        self._master_salt = salt_bytes
        return True

    def lock(self) -> None:
        """Lock the vault and clear in-memory key."""
        if self._master_salt is not None:
            try:
                byte_buffer = bytearray(self._master_salt)
                for byte_idx in range(len(byte_buffer)):
                    byte_buffer[byte_idx] = 0
            except Exception:
                pass
        self._fernet = None
        self._master_salt = None

    def migrate_legacy(self, master_password: str) -> int:
        """Migrate legacy unencrypted entries to encrypted vault_entries table."""
        if not self.is_legacy_unencrypted():
            return 0

        legacy_rows: list[tuple[str, str, str]] = []
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT password, date, reminder FROM password")
            legacy_rows = cursor.fetchall()

        self.initialize_vault(master_password)

        if not self._fernet:
            raise VaultError("Failed to initialize vault during legacy migration.")

        migrated_count = 0
        with self._get_connection() as connection:
            cursor = connection.cursor()
            for raw_pass, date_val, reminder_val in legacy_rows:
                encrypted_pass = self._fernet.encrypt(raw_pass.encode("utf-8")).decode("utf-8")
                cursor.execute(
                    "INSERT INTO vault_entries (service, encrypted_password, creation_date, reminder) VALUES (?, ?, ?, ?)",
                    ("Legacy Imported", encrypted_pass, date_val, reminder_val or ""),
                )
                migrated_count += 1
            cursor.execute("DROP TABLE password")
            connection.commit()

        return migrated_count

    def add_entry(self, service: str, password_text: str, reminder: str = "") -> int:
        """Add an encrypted password entry into the vault."""
        if not self._fernet:
            raise VaultError("Vault must be unlocked before adding entries.")

        encrypted_pass = self._fernet.encrypt(password_text.encode("utf-8")).decode("utf-8")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        service_clean = service.strip() or "General"

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO vault_entries (service, encrypted_password, creation_date, reminder) VALUES (?, ?, ?, ?)",
                (service_clean, encrypted_pass, timestamp, reminder.strip()),
            )
            connection.commit()
            return cursor.lastrowid or 0

    def get_entries(self, search_query: Optional[str] = None) -> list[dict]:
        """Retrieve and decrypt password entries matching optional query."""
        if not self._fernet:
            raise VaultError("Vault must be unlocked to read entries.")

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, service, encrypted_password, creation_date, reminder FROM vault_entries ORDER BY id DESC")
            records = cursor.fetchall()

        decrypted_entries: list[dict] = []
        search_filter = search_query.strip().lower() if search_query else None

        for entry_id, service_name, encrypted_pass, date_str, reminder_note in records:
            try:
                decrypted_pass = self._fernet.decrypt(encrypted_pass.encode("utf-8")).decode("utf-8")
            except InvalidToken:
                decrypted_pass = "[DECRYPTION_ERROR]"

            if search_filter:
                match_service = search_filter in service_name.lower()
                match_reminder = search_filter in (reminder_note or "").lower()
                if not (match_service or match_reminder):
                    continue

            decrypted_entries.append({
                "id": entry_id,
                "service": service_name,
                "password": decrypted_pass,
                "date": date_str,
                "reminder": reminder_note or "",
            })

        return decrypted_entries

    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        if not self._fernet:
            raise VaultError("Vault must be unlocked to delete entries.")

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM vault_entries WHERE id = ?", (entry_id,))
            connection.commit()
            return cursor.rowcount > 0

    def export_entries(self, export_path: Path, export_format: str = "json", plaintext: bool = False) -> int:
        """Export vault contents to JSON or CSV format.

        If plaintext is False, exports genuine AES-256 ciphertext strings so
        the backup file remains fully secured and authentic.
        """
        if not self._fernet:
            raise VaultError("Vault must be unlocked before exporting.")

        export_path = Path(export_path).resolve()
        export_path.parent.mkdir(parents=True, exist_ok=True)

        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, service, encrypted_password, creation_date, reminder FROM vault_entries ORDER BY id ASC")
            raw_records = cursor.fetchall()

        export_records: list[dict] = []
        for entry_id, service_name, encrypted_pass, date_str, reminder_note in raw_records:
            if plaintext:
                try:
                    password_value = self._fernet.decrypt(encrypted_pass.encode("utf-8")).decode("utf-8")
                except InvalidToken:
                    password_value = "[DECRYPTION_ERROR]"
            else:
                password_value = encrypted_pass

            export_records.append({
                "id": entry_id,
                "service": service_name,
                "password": password_value,
                "date": date_str,
                "reminder": reminder_note or "",
            })

        format_choice = export_format.strip().lower()
        if format_choice == "csv":
            with open(export_path, "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = ["id", "service", "password", "date", "reminder"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(export_records)
        else:
            with open(export_path, "w", encoding="utf-8") as json_file:
                json.dump(export_records, json_file, indent=2)

        return len(export_records)

    def import_entries(self, import_path: Path, import_format: Optional[str] = None) -> int:
        """Import password records from JSON or CSV backup into active vault."""
        if not self._fernet:
            raise VaultError("Vault must be unlocked before importing entries.")

        import_path = Path(import_path).resolve()
        if not import_path.is_file():
            raise FileNotFoundError(f"Import file not found: {import_path}")

        format_choice = import_format.lower() if import_format else import_path.suffix.lstrip(".").lower()
        records_to_import: list[dict] = []

        if format_choice == "csv":
            with open(import_path, "r", encoding="utf-8", errors="ignore") as csv_file:
                reader = csv.DictReader(csv_file)
                for row_record in reader:
                    records_to_import.append(dict(row_record))
        else:
            with open(import_path, "r", encoding="utf-8", errors="ignore") as json_file:
                raw_json = json.load(json_file)
                if isinstance(raw_json, list):
                    records_to_import = [dict(record_item) for record_item in raw_json]

        imported_count = 0
        with self._get_connection() as connection:
            cursor = connection.cursor()
            for record_item in records_to_import:
                service_val = str(record_item.get("service", "Imported")).strip() or "Imported"
                pass_val = str(record_item.get("password", ""))
                date_val = str(record_item.get("date", "")).strip() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reminder_val = str(record_item.get("reminder", "")).strip()

                if not pass_val:
                    continue

                # Check if password is valid ciphertext or plaintext
                try:
                    self._fernet.decrypt(pass_val.encode("utf-8"))
                    encrypted_to_store = pass_val
                except Exception:
                    # Treat as plaintext and encrypt
                    encrypted_to_store = self._fernet.encrypt(pass_val.encode("utf-8")).decode("utf-8")

                cursor.execute(
                    "INSERT INTO vault_entries (service, encrypted_password, creation_date, reminder) VALUES (?, ?, ?, ?)",
                    (service_val, encrypted_to_store, date_val, reminder_val),
                )
                imported_count += 1

            connection.commit()

        return imported_count


def copy_password_to_clipboard(password_text: str, auto_clear_seconds: int = 30) -> bool:
    """Copy password to system clipboard with automatic timed clearance."""
    try:
        import pyperclip
        pyperclip.copy(password_text)
    except Exception:
        return False

    if auto_clear_seconds > 0:
        def _clear_worker() -> None:
            time.sleep(auto_clear_seconds)
            try:
                import pyperclip
                if pyperclip.paste() == password_text:
                    pyperclip.copy("")
            except Exception:
                pass

        clearance_thread = threading.Thread(target=_clear_worker, daemon=True)
        clearance_thread.start()

    return True
