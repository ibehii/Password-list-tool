# **Password List Tool v3.2.0**
![](https://skillicons.dev/icons?i=py,vscode,md)
[![GitHub](https://img.shields.io/badge/GitHub-ibehii-blue?logo=github)](https://github.com/ibehii)
[![Telegram](https://img.shields.io/badge/Telegram-dr__xz-2CA5E0?logo=telegram)](https://t.me/dr_xz)

A high-performance, memory-efficient password generator, wordlist manipulation toolkit, and encrypted password vault built in Python. Designed to handle multi-gigabyte files with maximum speed and constant low memory usage using streaming algorithms.

---

## ⚡ Highlights & Key Features

- **Extreme Speed & Zero-OOM Streaming**: External merge sort, chunked deduplication, multi-file merger, line counter, and filtering engines stream data line-by-line using buffered I/O. Never crashes with Out-Of-Memory (OOM) even on 100GB+ wordlists.
- **Rich Beautiful Terminal UI**: Interactive menus, panels, progress indicators, and formatted tables powered by `rich`.
- **Targeted Profile Wordlist Generator (CUPP Style)**: Generates intelligent permutations from target names, birthdays, nicknames, mother/father names, partners, children, pets, companies, name abbreviations/initials, keywords, special years, and leetspeak variations.
- **Diceware / Passphrase Generator**: High-entropy, memorable multi-word passphrases generated from a curated English wordlist.
- **Pattern & Mask Generator**: Hashcat-compatible mask syntax (`?l`, `?u`, `?d`, `?s`, `?a`, `?h`, `?H`) streaming combinations directly to disk.
- **Wordlist Filtering Engine**: Filter massive lists by minimum/maximum length, character classes (lower, upper, digit, symbol), regex, or custom charsets.
- **Mutation & Leetspeak Engine**: Rule-based mutations (`a` -> `@`, `e` -> `3`, `i` -> `1`, `o` -> `0`, casing changes, prefixes, and suffixes).
- **Large File Splitter & Line Counter**: Split huge wordlists into smaller chunk files and count lines in milliseconds via binary block scanning.
- **Have I Been Pwned (HIBP) Breach Checker**: Uses SHA-1 k-anonymity API—passwords are **never** transmitted over the network.
- **Encrypted Password Vault (AES-256)**: Secure SQLite database (`.passwords.db`) protected by PBKDF2HMAC (SHA-256, 200,000 iterations) and AES-256 (Fernet) encryption. Includes search, clipboard integration with automatic 30-second clearance, and JSON/CSV backup exports. Automatic migration for legacy unencrypted databases.
- **CLI Automation Mode**: Full `argparse` CLI support for scripting and automation, alongside the interactive terminal interface.

---

## 🚀 Installation

```bash
git clone https://github.com/ibehii/Password-list-tool.git
cd Password-list-tool
pip install -r requirements.txt
```

Or install in editable mode using `pyproject.toml`:

```bash
pip install -e .
```

---

## 💻 Usage

### Interactive Menu

Run the application with no arguments to launch the Rich interactive menu:

```bash
python PasswordGenerator.py
```

### CLI Automation Mode

Run specific tasks directly from the command line:

```bash
# Generate 100,000 passwords to a file
python PasswordGenerator.py generate -c 100000 -l 18 -o rockyou_custom.txt

# Generate a 5-word Diceware passphrase
python PasswordGenerator.py passphrase -w 5 -s "-"

# Generate Hashcat mask combinations
python PasswordGenerator.py mask "Admin?d?d?d!" -o admin_masks.txt

# Generate targeted CUPP wordlist (supports mother, father, abbreviations, etc.)
python PasswordGenerator.py cupp --first-name Alice --last-name Smith --mother Mary --father John --name-abbr AS --birthdate 1995 --company Acme -o alice.txt

# Sort a huge wordlist via streaming external merge sort
python PasswordGenerator.py sort huge_wordlist.txt -o sorted_wordlist.txt

# Deduplicate a wordlist without loading it into RAM
python PasswordGenerator.py dedupe huge_wordlist.txt -o deduped_wordlist.txt

# Merge multiple lists with deduplication
python PasswordGenerator.py merge list1.txt list2.txt list3.txt -o combined.txt --dedupe

# Filter wordlist by criteria
python PasswordGenerator.py filter huge.txt -o filtered.txt --min 8 --max 20 --require-digit --require-symbol

# Mutate a wordlist with leetspeak and casing
python PasswordGenerator.py mutate base_words.txt -o mutated.txt

# Split a large file into chunks of 1,000,000 lines
python PasswordGenerator.py split massive.txt -o ./chunks --lines 1000000

# Fast line count
python PasswordGenerator.py count massive.txt

# Check password breach status via HIBP k-anonymity
python PasswordGenerator.py pwned "P@ssw0rd123"

# Check password strength and crack time
python PasswordGenerator.py strength "CorrectHorseBatteryStaple"
```

---

## 🧪 Testing

Run the automated test suite:

```bash
pytest
```
