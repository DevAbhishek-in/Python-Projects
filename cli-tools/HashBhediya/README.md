# 🐺 HashBhediya

**An AI-powered, multithreaded hash-cracking tool built for authorized security testing and learning.**

> ⚠️ **Disclaimer:** HashBhediya is built strictly for **educational purposes and authorized security testing**. Do not use it on systems, accounts, or hashes you don't own or don't have explicit permission to test. Misuse is entirely the user's responsibility.

---

## 🤖 About This Project

HashBhediya is a lightweight, terminal-based hash cracker built entirely with the help of AI tools. **100% of the code in this project was generated using AI assistance** — this is disclosed openly and honestly as part of the development process.

---

## ✨ Features

- 🔓 **Dictionary Attack Mode** — crack hashes using custom or built-in wordlists
- 🔢 **Numeric Brute-Force Mode** — brute-forces purely numeric passwords/PINs up to a configurable digit length
- ⚡ **Multithreaded Engine** — splits work across multiple CPU threads for faster cracking
- 🧠 **Auto Wordlist Downloader** — automatically fetches the official wordlists from this repo if they're missing
- 🔐 **Multiple Hash Algorithms Supported** — MD5, SHA1, SHA256
- 🖥️ **Two Output Modes** — Silent mode (clean) or Buffer flow mode (live attempt preview)
- 💾 **Auto-Save Results** — cracked plaintext is automatically saved to a result file
- 🧹 **Clean Exit Handling** — safely stops on interruption without leaving junk processes running

---

## 🎯 Why Use HashBhediya?

- Simple, no-clutter terminal interface — no complicated setup
- Works great on **Termux (Android)** as well as Linux/Windows/macOS
- No heavy third-party dependencies for core functionality
- Great for learning how dictionary attacks and brute-force attacks actually work
- Fast — multithreading means it doesn't sit idle on a single core

---

## 📦 Installation

Copy the command below (tap it, it copies with one click on GitHub), paste it into your terminal, and hit enter:

```bash
git clone https://github.com/DevAbhishek-in/Python-Projects.git && cd Python-Projects/cli-tools/HashBhediya && python3 tool.py
```

This will:
1. Clone the repository
2. Move into the HashBhediya folder
3. Launch the tool directly

---

## 🚀 Usage

1. Run `tool.py`
2. Choose attack mode:
   - `1` → Numeric brute-force attack
   - `2` → Dictionary attack (built-in or custom wordlist)
3. Select the hash algorithm (MD5 / SHA1 / SHA256)
4. Paste the target hash
5. Choose output mode (Silent / Buffer flow)
6. Let it run — if a match is found, it's saved automatically to `cracked_result.txt`

---

## 🛑 If the Program Crashes or Freezes

If your terminal freezes, gets stuck, or the tool crashes mid-run, immediately press:

```
Ctrl + C
```

This safely interrupts the program and stops all running threads cleanly without corrupting your terminal session.

---

## 📁 Wordlists

The `Wordlists/` folder contains the official wordlist files used for dictionary attacks. If they're not found locally, the tool will offer to auto-download them from this repository.

---

## 🛠️ Requirements

- Python 3.7+
- Internet connection (only needed for auto wordlist download)
- No external pip packages required — built using Python's standard library

---

## 📜 License & Responsibility

This tool is provided as-is for educational purposes. The developer is not responsible for any misuse. Always get proper authorization before testing any system.

---

## 👤 Author

**DevAbhishek-in**
Built with AI-assisted development as part of ongoing cybersecurity learning and CLI tool projects.
