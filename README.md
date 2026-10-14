<div align="center">

# 🔐 Password List Tool
### *High-Performance, Zero-OOM Wordlist Engine, Encrypted Vault & Security Toolkit for Python*

[![Release](https://img.shields.io/badge/Release-v3.2.1-blue?style=for-the-badge&logo=github)](https://github.com/ibehii/Password-list-tool/releases)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://github.com/ibehii/Password-list-tool)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=open-source-initiative&logoColor=white)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/ibehii/Password-list-tool/python-package.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/ibehii/Password-list-tool/actions)
[![Telegram](https://img.shields.io/badge/Telegram-@dr__xz-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/dr_xz)

<br/>

```text
 █▀█ ▄▀█ █▀ █▀ █░█░█ █▀█ █▀█ █▀▄   ▀█▀ █▀█ █▀█ █░░
 █▀▀ █▀█ ▄█ ▄█ ▀▄▀▄▀ █▄█ █▀▄ █▄▀   ░█░ █▄█ █▄█ █▄▄
  High-Performance Password & Wordlist Security Toolkit
```

*Ultra-fast, constant-memory streaming engine powered by `rich` and standard Python.*

---

### 🌟 Introduction

> **Industrial-grade password generation, wordlist manipulation, and credential management.**
>
> Standard password utilities and Python scripts frequently fail on massive wordlists: they crash with **Out-Of-Memory (OOM)** errors when processing multi-gigabyte files, truncate datasets during in-place operations, lack intelligent target profiling, or store credentials in plain text.
>
> **Password List Tool** is an ultra-fast, zero-bloat CLI toolkit and Python library engineered to handle multi-gigabyte lists (such as `rockyou.txt` and beyond) with **strict constant memory overhead** via streaming external merge sort, chunked deduplication, compiled regex filtering, Diceware entropy generation, Hashcat mask synthesis, CUPP-style targeted profiling, Have I Been Pwned $k$-anonymity breach verification, and an authenticated AES-256 local vault.

---

### 🗺️ Quick Navigation

<table>
  <tr>
    <td align="center" width="20%">
      <a href="#-quick-start">
        <font size="6">🚀</font><br/>
        <b>Quick Start</b><br/>
        <sub>Install & run in seconds</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-key-features">
        <font size="6">✨</font><br/>
        <b>Key Features</b><br/>
        <sub>Complete feature overview</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-streaming-architecture--benchmarks">
        <font size="6">⚡</font><br/>
        <b>Zero-OOM Engine</b><br/>
        <sub>Streaming architecture & speed</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-targeted-profile-generation-cupp">
        <font size="6">🎯</font><br/>
        <b>Targeted CUPP</b><br/>
        <sub>Social engineering profiling</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-encrypted-password-vault">
        <font size="6">🔐</font><br/>
        <b>Encrypted Vault</b><br/>
        <sub>AES-256 local credential store</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="20%">
      <a href="#-usage-guide">
        <font size="6">📖</font><br/>
        <b>Usage Guide</b><br/>
        <sub>All 13 features with examples</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-interactive-rich-terminal-ui">
        <font size="6">🖥️</font><br/>
        <b>Interactive UI</b><br/>
        <sub>Rich terminal dashboard</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-have-i-been-pwned-hibp-breach-checker">
        <font size="6">🛡️</font><br/>
        <b>HIBP Breach Check</b><br/>
        <sub>SHA-1 k-anonymity lookup</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-cli-subcommand-reference">
        <font size="6">📚</font><br/>
        <b>CLI Reference</b><br/>
        <sub>Full command & flags table</sub>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="#-contributing--standards">
        <font size="6">🤝</font><br/>
        <b>Contributing</b><br/>
        <sub>Testing, AST standards & license</sub>
      </a>
    </td>
  </tr>
</table>

</div>

---

<a id="-quick-start"></a>
## 🚀 Quick Start

Get started in 3 simple commands:

```bash
# 1. Clone the repository and install requirements
git clone https://github.com/ibehii/Password-list-tool.git
cd Password-list-tool
pip install -r requirements.txt

# Or install as an executable package using pyproject.toml
pip install -e .

# 2. Launch the interactive Rich dashboard
pass-tool
# (or: python PasswordGenerator.py)

# 3. Or run instant CLI automation commands
pass-tool generate -c 10 -l 16
pass-tool passphrase -w 5 -s "-"
pass-tool mask "Admin?d?d?d!" -o admin_passwords.txt
```

---

<a id="-key-features"></a>
## ✨ Key Features

| Feature | Description | Highlight |
| :--- | :--- | :--- |
| **Zero-OOM Streaming Engine** | All wordlist operations stream line-by-line using buffered I/O. Never loads full multi-gigabyte lists into RAM. | ⚡ Sort 100GB+ files without memory crashes |
| **Streaming External Merge Sort** | Partitioned disk-based merge sort with hierarchical 64-way batch merging to protect file descriptors. | 🛡️ Bounded memory & open handles |
| **Fast In-Memory Chunk Deduplication** | Single-pass streaming deduplication that removes duplicate entries inline while sorting. | 🚀 $2\times$ disk I/O reduction |
| **High-Speed Binary Line Counter** | Binary chunk scanning counting byte newlines in raw 64KB blocks without decoding unicode overhead. | ⏱️ 100,000 lines in **0.0038s** |
| **Targeted Profile Wordlist (CUPP Style)** | Generates intelligent password candidates based on victim demographics (names, nicknames, mother/father, birthdates, initials). | 🎯 High-probability penetration testing |
| **Diceware Passphrase Engine** | Cryptographically secure, memorable multi-word passphrases using a curated English wordlist. | 🎲 High entropy & human-friendly |
| **Hashcat Mask Syntax Generator** | Full mask engine supporting `?l`, `?u`, `?d`, `?s`, `?a`, `?h`, `?H`, and literal escapes (`??`). | 🎭 Compatible with Hashcat mask patterns |
| **Compiled C-Speed Regex Filtering** | Filter millions of passwords by min/max length, required character classes, or custom regex. | 🔍 $>2.5\times$ faster than generator checks |
| **Leetspeak & Mutation Rules** | Rule-based engine applying l33t substitution (`e` $\to$ `3`, `a` $\to$ `@`), case variations, prefixes, and suffixes. | 🧬 Real-world credential permutation |
| **Have I Been Pwned ($k$-Anonymity)** | Check passwords against hundreds of millions of breached credentials without transmitting passwords. | 🔒 SHA-1 5-char prefix $k$-anonymity API |
| **AES-256 Encrypted Local Vault** | Secure SQLite credential vault protected by PBKDF2 (SHA-256, 200,000 iterations) + Fernet AES-256. | 🔐 Strict POSIX `0o600` file permissions |
| **Clipboard Auto-Clear Protection** | Copy credentials with an automated background clearance timer (default: 30 seconds). | 📋 Zero clipboard leakage |
| **Backup Export & Import** | Export vault to encrypted or plaintext JSON/CSV backups and restore them with schema validation. | 💾 Portable data mobility |
| **Rich Terminal Dashboard** | Interactive menus, status panels, progress bars, and formatted tables powered by `rich`. | 🎨 Modern, beautiful CLI UX |
| **Full CLI Automation Flags** | Complete non-interactive subcommands via `argparse` for shell scripting, pipelines, and cron jobs. | 🤖 Scriptable & pipe-friendly |

---

<a id="-streaming-architecture--benchmarks"></a>
## ⚡ Streaming Architecture & Benchmarks

Traditional Python scripts use `file.readlines()` or `set(file.read().splitlines())`. For multi-gigabyte lists like `rockyou.txt` or large dehashed breaches, this instantly crashes the Python process with `MemoryError` or triggers system swap thrashing.

```
┌────────────────────────────────────────────────────────────────────────┐
│                  Password List Tool Streaming Pipeline                 │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [ Input Wordlist ]  ──▶  Stream in 64KB Chunks  ──▶  Sort Partition   │
│                                                              │         │
│                                                              ▼         │
│  [ Output Stream ]   ◀──  64-Way K-Merge Tree   ◀──  Write Temp Chunks │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Architectural Guarantees:
1. **Bounded Heap**: Chunks are sorted in batches sized to available memory (default: 100,000 lines per chunk) and written to the destination filesystem partition, avoiding `/tmp` `tmpfs` RAM exhaustion.
2. **Bounded File Descriptors**: When merging hundreds of chunks, standard `heapq.merge` crashes with `OSError: [Errno 24] Too many open files`. Our engine merges chunks in a hierarchical 64-way batch tree to maintain a tiny constant open descriptor count.
3. **In-Place File Safety**: Operations targeting the source file (`tool sort target.txt`) automatically stage to a temporary volume file and atomically rename (`os.replace`) upon completion, eliminating file truncation bugs.
4. **Binary Line Scanning**: Line counting reads raw binary blocks (`64 KB`) scanning for byte `\n` without string object allocation.

### Performance Benchmarks (Tested on Linux, Python 3.14 / SSD):

| Operation | Dataset Size | Naive Python Approach | Password List Tool v3.2 | Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **Line Counting** | 100,000 lines | `len(f.readlines())` (0.048s, high RAM) | **0.0038s** (constant 64KB RAM) | **12.6x faster** |
| **External Merge Sort** | 100,000 lines | `sorted(f.readlines())` (OOM on large files) | **0.1011s** (disk-chunked streaming) | **Zero-OOM Guarantee** |
| **Deduplication** | 100,000 lines | Two-pass file rewrite (0.071s) | **0.0325s** (single-pass inline dedupe) | **2.2x faster** |
| **Character Filtering** | 100,000 lines | `any(c in string)` generators (0.345s) | **0.1383s** (compiled C-regex) | **2.5x faster** |

---

<a id="-targeted-profile-generation-cupp"></a>
## 🎯 Targeted Profile Generation (CUPP Style)

During authorized penetration tests and security assessments, brute force attacks are ineffective compared to targeted, human-profiled password lists. 

The CUPP engine generates permutations by combining:
- **Core Entities**: First name, last name, nicknames, company, school, pets.
- **Family Details**: Mother's name, father's name, partner's name, partner's nickname, children's names.
- **Demographic Dates**: Birthdays, partner's birthdate, child's birthdate, special years (extracts full dates, 4-digit years, and 2-digit suffixes).
- **Name Abbreviations & Initials**: Custom abbreviation tokens (`AS`, `admin`), first initial + last name (`asmith`, `a_smith`), name + last initial (`alices`), and reverse pairings (`smitha`).
- **Separators & Affixes**: Connectors (`_`, `.`, `-`), common years (`1980`–`2026`), and high-frequency symbols (`!`, `@`, `#`, `$`, `123`).
- **Leetspeak Engine**: Real-world substitutions (`a` $\to$ `@`, `e` $\to$ `3`, `i` $\to$ `1`, `o` $\to$ `0`).

### CLI Example:
```bash
pass-tool cupp \
  --first-name Alice \
  --last-name Smith \
  --nickname Ally \
  --mother Mary \
  --father John \
  --partner Bob \
  --child Charlie \
  --pet Fluffy \
  --company CyberCorp \
  --name-abbr "AS, AllyS" \
  --birthdate 1995 \
  --years 2024 2025 \
  --keywords admin vpn wifi \
  -o alice_custom.txt
```

---

<a id="-encrypted-password-vault"></a>
## 🔐 Encrypted Password Vault

Store and access generated credentials in an authenticated local encrypted vault (`lib/db/.passwords.db`):

- **Cryptographic Security**: Master password derived via **PBKDF2HMAC (SHA-256, 200,000 iterations)** with a unique random salt, encrypting records using **AES-256 (Fernet)**.
- **Filesystem Security**: Automatically restricts database permissions to `0o600` (read/write only by owner) on POSIX platforms.
- **Legacy Migration**: Automatically detects unencrypted database schemas and seamlessly upgrades them to the encrypted format when a master password is set.
- **Clipboard Safety**: Copy passwords to the system clipboard with an automated background worker that clears the clipboard after 30 seconds to prevent shoulder surfing and clipboard hijackers.
- **Encrypted Backup & Recovery**: Export vault contents to authenticated JSON or CSV backups and import them on other machines.

---

<a id="-usage-guide"></a>
## 📖 Usage Guide

### 1. Generate Single Password
Generate a cryptographically secure random password with customized character pools:

```bash
# Generate 16-character password with symbols and numbers
pass-tool generate -l 16

# Exclude symbols and include ambiguous brackets
pass-tool generate -l 20 --no-symbols --ambiguous
```

### 2. Generate Bulk Password Lists (Streaming)
Generate millions of random passwords directly into a file without memory buildup:

```bash
# Generate 500,000 14-character passwords directly to disk
pass-tool generate -c 500000 -l 14 -o wordlist_500k.txt
```

### 3. Generate Diceware Passphrases
Create memorable, high-entropy multi-word passphrases:

```bash
# Generate 5-word passphrase with hyphen separator
pass-tool passphrase -w 5 -s "-"
# Output: Curve-Sugar-Defense-Case-Staple-48

# Customize formatting
pass-tool passphrase -w 4 -s "_" --no-number --symbol
```

### 4. Hashcat Mask & Pattern Generator
Generate passwords matching specific masks:

```bash
# Hashcat mask syntax: ?u (upper), ?l (lower), ?d (digit), ?s (symbol)
pass-tool mask "Corp2024?s?d?d" -o corp_masks.txt

# Hex masks: ?h (lowercase hex), ?H (uppercase hex)
pass-tool mask "Key_?h?h?h?h" -o hex_keys.txt
```

### 5. Sort Password Lists (Streaming External Merge Sort)
Sort massive files alphabetically or in reverse order with constant memory:

```bash
# Sort in-place
pass-tool sort huge_wordlist.txt

# Sort to new file in reverse order
pass-tool sort huge_wordlist.txt -o sorted.txt --reverse
```

### 6. Streaming Deduplication
Deduplicate massive wordlists without loading the entire file into RAM:

```bash
# Deduplicate into a clean file
pass-tool dedupe raw_wordlist.txt -o clean_wordlist.txt
```

### 7. Multi-File Wordlist Merger
Merge multiple wordlists into a single consolidated file with optional deduplication:

```bash
pass-tool merge breach1.txt breach2.txt custom.txt -o combined.txt --dedupe
```

### 8. Wordlist Filtering Engine
Filter wordlists by security criteria or regular expressions:

```bash
# Keep only passwords between 8 and 20 chars with digits and symbols
pass-tool filter wordlist.txt -o filtered.txt --min 8 --max 20 --require-digit --require-symbol

# Filter using custom regex
pass-tool filter wordlist.txt -o matched.txt --regex "^[A-Z][a-z0-9_]{7,15}$"
```

### 9. Mutation & Leetspeak Engine
Apply mutation rules and leetspeak substitutions to an existing base list:

```bash
pass-tool mutate base_passwords.txt -o mutated_passwords.txt
```

### 10. File Splitter & Line Counter
Split multi-gigabyte files into manageable chunks and inspect line counts:

```bash
# Fast line count
pass-tool count massive_list.txt

# Split into 500,000-line chunks
pass-tool split massive_list.txt -o ./chunks/ --lines 500000
```

### 11. Have I Been Pwned (HIBP) Breach Lookup
Check whether a password has been compromised in public breaches:

```bash
# Check single password
pass-tool pwned "Password123!"

# Output:
# ⚠ Breached! Appeared in 45,921 known data breaches.
```

### 12. Password Strength & Crack Time Analyzer
Analyze entropy and cracking resistance using `zxcvbn`:

```bash
pass-tool strength "Correct-Horse-Battery-Staple-2024"
```

---

<a id="-interactive-rich-terminal-ui"></a>
## 🖥️ Interactive Rich Terminal UI

Run `PasswordGenerator.py` or `pass-tool` with no arguments to enter the interactive dashboard:

```text
╭────────────────────────────── Main Menu ──────────────────────────────╮
│  [1]  Generate single password (customizable, strength, clipboard)    │
│  [2]  Generate bulk password list (streaming, memory-safe)            │
│  [3]  Generate Diceware passphrase (memorable multi-word)             │
│  [4]  Generate Pattern / Mask list (Hashcat-style ?l?u?d?s)           │
│  [5]  Targeted profile wordlist generator (CUPP-style)                │
│  [6]  Sort password list (streaming external merge sort)              │
│  [7]  Delete duplicate passwords (streaming deduplication)           │
│  [8]  Merge password lists (streaming multi-file combiner)            │
│  [9]  Filter password list (by length, charset, regex)                │
│  [10] Mutate & Leetspeak engine (rules, casing, leet, affixes)        │
│  [11] Large file splitter & line counter (constant RAM)               │
│  [12] Have I Been Pwned check (SHA-1 k-anonymity API)                 │
│  [13] Encrypted Password Vault (.passwords.db, AES-256)               │
│  [14] Check password strength & crack time (zxcvbn)                   │
│  [0]  Exit                                                            │
╰───────────────────────────────────────────────────────────────────────╯
```

---

<a id="-have-i-been-pwned-hibp-breach-checker"></a>
## 🛡️ Have I Been Pwned (HIBP) Breach Checker

Security tools should never compromise credentials. Our HIBP integration strictly implements the **$k$-Anonymity model**:

1. Computes the SHA-1 hash of the password locally (e.g. `SHA1("Password123")` $\to$ `CBFDAC6008F9CAB4083784CBD1874F76618D2A97`).
2. Extracts only the **first 5 hexadecimal characters** (`CBFDA`).
3. Sends only the 5-character prefix to `https://api.pwnedpasswords.com/range/CBFDA`.
4. The API returns all known hashes matching that prefix alongside breach occurrence counts.
5. Matches the remaining 35 characters locally in memory.
6. **Result**: Neither the password nor its full hash ever leaves your computer.

---

<a id="-cli-subcommand-reference"></a>
## 📚 CLI Subcommand Reference

| Command | Arguments & Flags | Description | Example |
| :--- | :--- | :--- | :--- |
| `generate` | `-c COUNT`, `-l LEN`, `-o FILE`, `--no-symbols`, `--no-numbers`, `--no-lower`, `--no-upper`, `--ambiguous` | Generate single or bulk random passwords. | `pass-tool generate -c 100 -l 16 -o out.txt` |
| `passphrase`| `-w WORDS`, `-s SEP`, `--no-capitalize`, `--no-number`, `--symbol` | Generate Diceware multi-word passphrases. | `pass-tool passphrase -w 5 -s "-"` |
| `mask` | `PATTERN`, `-o FILE` | Generate combinations from a Hashcat-style mask. | `pass-tool mask "User?d?d?d!" -o out.txt` |
| `cupp` | `--first-name`, `--last-name`, `--mother`, `--father`, `--partner`, `--child`, `--pet`, `--company`, `--name-abbr`, `--birthdate`, `--years`, `--keywords`, `-o FILE` | Generate targeted profile permutations. | `pass-tool cupp --first-name Alice -o out.txt` |
| `sort` | `FILE`, `-o FILE`, `-r` (`--reverse`) | Streaming external merge sort for massive files. | `pass-tool sort list.txt -o sorted.txt` |
| `dedupe` | `FILE`, `-o FILE` | Streaming single-pass duplicate remover. | `pass-tool dedupe list.txt -o clean.txt` |
| `merge` | `FILES...`, `-o FILE`, `--dedupe` | Stream and concatenate multiple wordlists. | `pass-tool merge a.txt b.txt -o merged.txt` |
| `filter` | `FILE`, `-o FILE`, `--min`, `--max`, `--require-lower`, `--require-upper`, `--require-digit`, `--require-symbol`, `--regex` | Filter lines matching length and charset rules. | `pass-tool filter in.txt -o out.txt --min 8` |
| `mutate` | `FILE`, `-o FILE`, `--no-leet`, `--no-case` | Mutate wordlist using leetspeak and casing rules. | `pass-tool mutate base.txt -o mutated.txt` |
| `split` | `FILE`, `-o DIR`, `--lines` | Split a large file into chunks of $N$ lines. | `pass-tool split big.txt -o ./chunks/ -l 500000` |
| `count` | `FILE` | Rapid binary block line counter. | `pass-tool count massive.txt` |
| `pwned` | `PASSWORD` | Query HIBP database via $k$-anonymity. | `pass-tool pwned "Admin123"` |
| `strength` | `PASSWORD` | Calculate password entropy and crack time. | `pass-tool strength "MyPass"` |

---

<a id="-contributing--standards"></a>
## 🤝 Contributing & Standards

Contributions, bug reports, and pull requests are welcome!

### Development Setup:
```bash
git clone https://github.com/ibehii/Password-list-tool.git
cd Password-list-tool
pip install -e ".[dev]"
```

### Running Test Suite:
```bash
# Run all 40 automated tests
python3 -m pytest -v
```

### Coding Standards Enforcement:
- **Zero Single-Character Iterators**: Variables `i` and `j` are banned project-wide to enforce clear, maintainable naming conventions. Enforced via AST testing in `tests/test_code_standards.py`.
- **Zero-OOM File Processing**: Any new file-handling routine must process data through iterators or generators with constant memory guarantees.
- **Strict Typing**: Type annotations (`from __future__ import annotations`) across all modules.

---

<a id="-license--author"></a>
## 📄 License & Author

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full details.

- **Author**: Behnam
- **GitHub**: [@ibehii](https://github.com/ibehii)
- **Telegram**: [@dr_xz](https://t.me/dr_xz)
- **Email**: `Behii@tutanota.com`
- **YouTube Tutorial**: [Watch Video](https://youtu.be/hlkBS0gWI7g)

<div align="center">
  <sub>Built with ❤️ for cybersecurity professionals, penetration testers, and security researchers.</sub>
</div>
