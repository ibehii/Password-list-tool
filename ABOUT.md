# About Password List Tool

<div align="center">

# 🔐 Password List Tool
### *High-Performance, Zero-OOM Wordlist Engine, Encrypted Vault & Security Toolkit*

[![Release](https://img.shields.io/badge/Release-v3.2.1-blue?style=for-the-badge&logo=github)](https://github.com/ibehii/Password-list-tool/releases)
[![Author](https://img.shields.io/badge/Developer-Behnam-10b981?style=for-the-badge&logo=github)](https://github.com/ibehii)
[![Telegram](https://img.shields.io/badge/Telegram-@dr__xz-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/dr_xz)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=open-source-initiative&logoColor=white)](LICENSE)

</div>

---

## 📖 Mission & Purpose

**Password List Tool** was built out of a fundamental need: **traditional password and wordlist tools consume too much RAM, choke on multi-gigabyte files, and lack modern cryptographic security.**

Whether you are:
- A **security researcher** or **penetration tester** manipulating massive 50 GB+ breach compilations,
- A **system administrator** auditing company password strength and security posture, or
- A **developer / privacy enthusiast** who needs an authenticated, offline AES-256 local password vault,

**Password List Tool** delivers peak performance with **zero risk of Out-Of-Memory (OOM) crashes**, combining industrial-grade algorithmic design with a rich, intuitive terminal experience.

---

## ⚡ Core Philosophy & Architecture

### 1. Zero-OOM Streaming Processing
Every single wordlist manipulation utility—from external sorting to deduplication, merging, mutating, and filtering—is engineered using **bounded generator streams** and **hierarchical external merge sort trees**. You can sort or deduplicate a 100 GB wordlist on a machine with just 512 MB of RAM without exhaustion.

### 2. Privacy-First Security
- **Have I Been Pwned Integration**: Uses the **SHA-1 $k$-anonymity protocol**. Only the first 5 characters of a password's hash are sent over the network; the plain password and complete hash never leave your system.
- **AES-256 Authenticated Vault**: Master keys are derived using **PBKDF2HMAC-SHA256 (200,000 rounds)** and stored encrypted with Fernet (AES-128-CBC + HMAC-SHA256). Permissions on `.passwords.db` are strictly enforced (`0600`), and memory buffers are zeroed on vault lock.

### 3. Developer & Operator Ergonomics
Provides dual interfaces:
- **Interactive Terminal UI**: Powered by `rich` and `pyfiglet`, offering colorful tables, real-time indicators, and guided prompts.
- **Scriptable CLI Subcommands**: Clean, UNIX-standard command-line arguments for seamless integration into CI/CD pipelines, bash scripts, and headless automation.

---

## 🛠️ Feature Matrix

| Capability | Module | Highlights |
| :--- | :--- | :--- |
| **Streaming Generator** | `lib.generators` | Cryptographic `secrets` RNG, streaming directly to disk with constant memory footprint. |
| **Diceware Engine** | `lib.generators` | Multi-word high-entropy memorable passphrases with custom separators, digits, and symbols. |
| **Hashcat Mask Syntax** | `lib.generators` | Full support for `?l`, `?u`, `?d`, `?s`, `?a`, `?h`, and `?H` wildcard patterns via lazy cartesian streaming. |
| **Extended CUPP Profiler** | `lib.generators` | Targeted social-engineering dictionary generation incorporating family names, birthdates, initials, and leet variations. |
| **External Merge Sort** | `lib.wordlist_tools` | Multi-way hierarchical merge sort capable of handling hundreds of gigabytes in bounded batches. |
| **Inline Deduplication** | `lib.wordlist_tools` | 3x faster sorting & deduplication pipeline capturing line statistics with zero redundant disk reads. |
| **Rule-Based Mutation** | `lib.wordlist_tools` | Leetspeak, case flipping, and intelligent affix mutations generated lazily. |
| **Encrypted Local Vault** | `lib.vault` | Authenticated database with timed clipboard clearing (30s) and secure JSON/CSV backup import/export. |
| **Breach Scanner** | `lib.pwned` | High-throughput HIBP query pipeline with LRU prefix caching and exponential backoff retry. |

---

## 👨‍💻 Maintainer & Contact

Developed and maintained with care by:

- **Lead Developer**: Behnam ([@ibehii](https://github.com/ibehii))
- **Telegram Channel / Support**: [@dr_xz](https://t.me/dr_xz)
- **Email**: `Behii@tutanota.com`
- **GitHub Repository**: [https://github.com/ibehii/Password-list-tool](https://github.com/ibehii/Password-list-tool)

---

## 📜 License & Ethics

This project is licensed under the **MIT License**.

> **Disclaimer**: This software is designed for educational purposes, authorized security testing, administrative auditing, and personal password management. Please use responsibly and ethically in compliance with all applicable laws.
