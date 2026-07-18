#!/usr/bin/env python3
"""
================================================================================
 tool.py — Minimalist Multithreaded Hash Cracking Utility
 Educational / Authorized Security Testing Use Only
================================================================================
"""

import os
import sys
import hashlib
import signal
import itertools
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------------------------------------------------------
# Global config
# --------------------------------------------------------------------------
WORDLIST_DIR = "wordlists"          # <-- directory the tool expects/clones into
RESULT_FILE = "cracked_result.txt"
MAX_WORKERS = min(32, (os.cpu_count() or 4) * 2)

NUMERIC_CHARS = "0123456789"

# Shared cross-thread signals
found_event = threading.Event()
result_lock = threading.Lock()
result_data = {"plaintext": None, "hash": None}


# ==========================================================================
# >>> DEVELOPER CUSTOMIZATION ZONE <<<
# ==========================================================================
def download_default_wordlists():
    """
    Placeholder for automated wordlist provisioning.

    ------------------------------------------------------------------
    PASTE YOUR CUSTOM GIT CLONE / DOWNLOAD LOGIC BELOW THIS LINE.
    Example (uncomment & edit):

        subprocess.run(
            ["git", "clone", "<YOUR_REPO_URL_HERE>", WORDLIST_DIR],
            check=True
        )

    The cloned/downloaded directory MUST end up named exactly
    "wordlists/" in the current working directory and should
    contain the 6 expected .txt files.
    ------------------------------------------------------------------
    """
    import urllib.request

    base_url = "https://raw.githubusercontent.com/DevAbhishek-in/Python-Projects/main/cli-tools/HashBhediya/Wordlists/"
    filenames = [
        "wordlist1.txt", "wordlist2.txt", "wordlist3.txt",
        "wordlist4.txt", "wordlist5.txt", "wordlist6.txt",
    ]

    try:
        os.makedirs(WORDLIST_DIR, exist_ok=True)
        for name in filenames:
            url = base_url + name
            dest = os.path.join(WORDLIST_DIR, name)
            urllib.request.urlretrieve(url, dest)
        return os.path.isdir(WORDLIST_DIR)
    except Exception:
        return False


# ==========================================================================
# Hashing helpers
# ==========================================================================
def compute_hash(text: str, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(text.encode("utf-8", errors="ignore"))
    return h.hexdigest()


def save_result(plaintext: str, target_hash: str):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(f"plaintext: {plaintext}\nhash: {target_hash}\n")


# ==========================================================================
# Wordlist / dependency verification
# ==========================================================================
def ensure_wordlists():
    """Blocks dictionary attack path unless wordlists/ exists (or is cloned)."""
    if os.path.isdir(WORDLIST_DIR) and os.listdir(WORDLIST_DIR):
        return True

    print("Default wordlists folder not found.")
    choice = input("Download the official 6 wordlists via Git? (y/n): ").strip().lower()
    if choice != "y":
        return False

    print("Fetching wordlists...")
    ok = download_default_wordlists()
    if not ok or not os.path.isdir(WORDLIST_DIR):
        print("[X] Wordlist download failed or placeholder not configured.")
        return False
    return True


def list_builtin_wordlists():
    files = sorted(
        f for f in os.listdir(WORDLIST_DIR)
        if os.path.isfile(os.path.join(WORDLIST_DIR, f))
    )
    return files


def select_wordlist_path():
    print("\n1) Built-in wordlist   2) Custom wordlist")
    choice = input("> ").strip()

    if choice == "1":
        if not ensure_wordlists():
            return None
        files = list_builtin_wordlists()
        if not files:
            print("[X] No files found in wordlists/.")
            return None
        for i, f in enumerate(files, 1):
            print(f"  {i}. {f}")
        idx = input("Select file #: ").strip()
        try:
            return os.path.join(WORDLIST_DIR, files[int(idx) - 1])
        except (ValueError, IndexError):
            print("[X] Invalid selection.")
            return None

    elif choice == "2":
        path = input("Path/filename: ").strip()
        if not os.path.isfile(path):
            print("[X] File not found.")
            return None
        return path

    print("[X] Invalid option.")
    return None


# ==========================================================================
# Threaded worker chunks
# ==========================================================================
def _crack_chunk_wordlist(lines, target_hash, algo, mode):
    for word in lines:
        if found_event.is_set():
            return
        word = word.strip("\n\r")
        if not word:
            continue
        try:
            h = compute_hash(word, algo)
        except Exception:
            continue
        if mode == "buffer":
            print(f"\r{word[:40]:<40}", end="", flush=True)
        if h == target_hash:
            with result_lock:
                if not found_event.is_set():
                    result_data["plaintext"] = word
                    result_data["hash"] = h
                    found_event.set()
            return


def _crack_chunk_numeric(start, end, length, target_hash, algo, mode):
    for n in range(start, end):
        if found_event.is_set():
            return
        candidate = str(n).zfill(length)
        try:
            h = compute_hash(candidate, algo)
        except Exception:
            continue
        if mode == "buffer":
            print(f"\r{candidate:<40}", end="", flush=True)
        if h == target_hash:
            with result_lock:
                if not found_event.is_set():
                    result_data["plaintext"] = candidate
                    result_data["hash"] = h
                    found_event.set()
            return


# ==========================================================================
# Attack orchestrators
# ==========================================================================
def run_dictionary_attack(path, target_hash, algo, mode):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    if not lines:
        print("[X] Wordlist is empty.")
        return False

    chunk_size = max(1, len(lines) // MAX_WORKERS)
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(_crack_chunk_wordlist, c, target_hash, algo, mode)
            for c in chunks
        ]
        try:
            for _ in as_completed(futures):
                if found_event.is_set():
                    break
        except KeyboardInterrupt:
            found_event.set()
            executor.shutdown(wait=False, cancel_futures=True)
            raise

    return found_event.is_set()


def run_numeric_attack(max_length, target_hash, algo, mode):
    for length in range(1, max_length + 1):
        if found_event.is_set():
            break
        total = 10 ** length
        step = max(1, total // MAX_WORKERS)
        bounds = list(range(0, total, step)) + [total]

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(
                    _crack_chunk_numeric,
                    bounds[i], bounds[i + 1], length, target_hash, algo, mode
                )
                for i in range(len(bounds) - 1)
            ]
            try:
                for _ in as_completed(futures):
                    if found_event.is_set():
                        break
            except KeyboardInterrupt:
                found_event.set()
                executor.shutdown(wait=False, cancel_futures=True)
                raise

    return found_event.is_set()


# ==========================================================================
# Minimal CLI
# ==========================================================================
def prompt_algo():
    print("Hash type: 1) MD5  2) SHA1  3) SHA256")
    return {"1": "md5", "2": "sha1", "3": "sha256"}.get(input("> ").strip(), "md5")


def prompt_mode():
    print("Mode: 1) Silent  2) Buffer flow")
    return "buffer" if input("> ").strip() == "2" else "silent"


def main():
    print("== tool.py :: hash cracker ==")
    print("1) Numeric attack   2) Dictionary attack")
    choice = input("> ").strip()

    algo = prompt_algo()
    target_hash = input("Target hash: ").strip().lower()
    if not target_hash:
        print("[X] No hash given.")
        return
    mode = prompt_mode()

    found = False
    if choice == "1":
        try:
            max_len = int(input("Max digit length (1-25): ").strip())
            max_len = max(1, min(25, max_len))
        except ValueError:
            max_len = 6
        found = run_numeric_attack(max_len, target_hash, algo, mode)

    elif choice == "2":
        path = select_wordlist_path()
        if path is None:
            print("[X] Dictionary attack blocked: no valid wordlist.")
            return
        found = run_dictionary_attack(path, target_hash, algo, mode)

    else:
        print("[X] Invalid option.")
        return

    if mode == "buffer":
        print()  # newline after live overwrite output

    if found:
        save_result(result_data["plaintext"], result_data["hash"])
        print(f"[OK] Cracked: {result_data['plaintext']}  ->  saved to {RESULT_FILE}")
    else:
        print("[X] No match found.")


# ==========================================================================
# Entry point — clean signal handling, no stack-trace clutter
# ==========================================================================
def _sigint_handler(signum, frame):
    found_event.set()
    print("\n[!] Interrupted. Exiting cleanly.")
    sys.exit(130)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _sigint_handler)
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Exiting cleanly.")
        sys.exit(130)
    except Exception as e:
        print(f"[X] Error: {e}")
        sys.exit(1)
