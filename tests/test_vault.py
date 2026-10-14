"""Tests for encrypted SQLite password vault and legacy migration."""

from __future__ import annotations

import json
import sqlite3
import tempfile
from pathlib import Path

import pytest

from lib.vault import (
    InvalidMasterPasswordError,
    PasswordVault,
    VaultNotInitializedError,
    copy_password_to_clipboard,
)


def test_vault_lifecycle() -> None:
    """Test full vault lifecycle: init, unlock, CRUD, lock, fail on wrong password."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / ".test_vault.db"
        vault = PasswordVault(db_path=db_path)

        assert not vault.is_initialized()
        with pytest.raises(VaultNotInitializedError):
            vault.unlock("some_password")

        # Initialize
        vault.initialize_vault("MasterKey123!")
        assert vault.is_initialized()
        assert vault.is_unlocked

        # Add entries
        entry_one_id = vault.add_entry(service="GitHub", password_text="GhPass456!", reminder="Work account")
        entry_two_id = vault.add_entry(service="ProtonMail", password_text="SecretPm789!", reminder="Personal")
        assert entry_one_id > 0
        assert entry_two_id > entry_one_id

        # Retrieve entries
        all_entries = vault.get_entries()
        assert len(all_entries) == 2

        # Search filter
        filtered_entries = vault.get_entries(search_query="proton")
        assert len(filtered_entries) == 1
        assert filtered_entries[0]["service"] == "ProtonMail"
        assert filtered_entries[0]["password"] == "SecretPm789!"

        # Lock vault
        vault.lock()
        assert not vault.is_unlocked

        # Unlock with wrong password
        with pytest.raises(InvalidMasterPasswordError):
            vault.unlock("WrongPassword!")

        # Unlock with correct password
        assert vault.unlock("MasterKey123!")

        # Delete entry
        assert vault.delete_entry(entry_one_id)
        assert len(vault.get_entries()) == 1


def test_vault_legacy_migration() -> None:
    """Test automatic migration from legacy unencrypted password table."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / ".legacy.db"

        # Create unencrypted legacy database table
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE password (password TEXT, date TEXT, reminder TEXT)")
            cur.execute("INSERT INTO password VALUES ('Plaintext123', '2024-01-01', 'Old Note')")
            conn.commit()

        vault = PasswordVault(db_path=db_path)
        assert vault.is_legacy_unencrypted()

        # Migrate to encrypted vault
        migrated_count = vault.migrate_legacy("NewMasterKey999!")
        assert migrated_count == 1
        assert not vault.is_legacy_unencrypted()
        assert vault.is_initialized()

        # Check entries were encrypted and are decryptable
        entries = vault.get_entries()
        assert len(entries) == 1
        assert entries[0]["password"] == "Plaintext123"
        assert entries[0]["reminder"] == "Old Note"


def test_vault_export_and_import() -> None:
    """Test exporting vault records to JSON and CSV (plaintext and encrypted) and importing them."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / ".export_test.db"
        vault = PasswordVault(db_path=db_path)
        vault.initialize_vault("SecretMasterPass!")

        vault.add_entry(service="AWS", password_text="SuperSecretAWSKey", reminder="Cloud root")

        # Plaintext JSON export
        json_export = Path(temp_dir) / "export.json"
        exported_count = vault.export_entries(json_export, export_format="json", plaintext=True)
        assert exported_count == 1

        json_data = json.loads(json_export.read_text(encoding="utf-8"))
        assert json_data[0]["service"] == "AWS"
        assert json_data[0]["password"] == "SuperSecretAWSKey"

        # Encrypted JSON export (must contain genuine ciphertext, NOT dummy string)
        enc_export = Path(temp_dir) / "enc_export.json"
        vault.export_entries(enc_export, export_format="json", plaintext=False)
        enc_data = json.loads(enc_export.read_text(encoding="utf-8"))
        assert enc_data[0]["password"] != "SuperSecretAWSKey"
        assert enc_data[0]["password"] != "[ENCRYPTED_VAULT_BACKUP]"
        assert len(enc_data[0]["password"]) > 20

        # CSV export
        csv_export = Path(temp_dir) / "export.csv"
        vault.export_entries(csv_export, export_format="csv", plaintext=True)
        csv_content = csv_export.read_text(encoding="utf-8")
        assert "SuperSecretAWSKey" in csv_content

        # Import into fresh vault
        restore_db_path = Path(temp_dir) / ".restore_test.db"
        restore_vault = PasswordVault(db_path=restore_db_path)
        restore_vault.initialize_vault("NewVaultKey456!")
        imported_count = restore_vault.import_entries(json_export)
        assert imported_count == 1
        restored_entries = restore_vault.get_entries()
        assert len(restored_entries) == 1
        assert restored_entries[0]["service"] == "AWS"
        assert restored_entries[0]["password"] == "SuperSecretAWSKey"


def test_clipboard_copy() -> None:
    """Test clipboard copy helper (tolerates systems without GUI clipboard)."""
    result = copy_password_to_clipboard("test_pass", auto_clear_seconds=0)
    assert isinstance(result, bool)
