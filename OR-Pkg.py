#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Package Installer
Creator: Amir Terrorist
Run: python termux_pkg.py
"""

import os
import sys
import time
import shutil
import subprocess

# ---------- Colors ----------
class C:
    R = "\033[1;31m"
    G = "\033[1;32m"
    B = "\033[1;34m"
    Y = "\033[1;33m"
    C = "\033[1;36m"
    M = "\033[1;35m"
    W = "\033[1;37m"
    NC = "\033[0m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def cprint(text="", color=C.NC, end="\n"):
    print(f"{color}{text}{C.NC}", end=end)
    sys.stdout.flush()


# ---------- Loading bar ----------
def loading_bar(text, delay=0.02):
    cprint(f"[*] {text}", C.C)
    total = 100
    step = 4
    for i in range(0, total + 1, step):
        filled = i // step
        empty = (total // step) - filled
        bar = "#" * filled + " " * empty
        sys.stdout.write(f"\r{C.G}[{bar}] {i:3d}%{C.NC}")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")


# ---------- Run command ----------
def run(cmd):
    """Run a shell command, return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def install_packages(pkgs):
    """Install packages one by one, skip missing ones gracefully."""
    failed = []
    for pkg in pkgs:
        cprint(f"[+] Installing {pkg} ...", C.C)
        ok, out = run(f"pkg install -y {pkg}")
        if not ok:
            # Some pkgs exist under different names or are unavailable
            cprint(f"[!] Failed: {pkg} (skipped)", C.Y)
            failed.append(pkg)
        else:
            cprint(f"[✔] {pkg} installed", C.G)
    return failed


# ---------- Banner ----------
def banner():
    clear()
    cprint("=" * 50, C.R)
    cprint("     _    __  __ ___ ____", C.R)
    cprint("    / \\  |  \\/  |_ _|  _ \\", C.R)
    cprint("   / _ \\ | |\\/| || || |_) |", C.R)
    cprint("  / ___ \\| |  | || ||  _ <", C.R)
    cprint(" /_/   \\_\\_|  |_|___|_| \\_\\", C.R)
    cprint("=" * 50, C.C)
    cprint("        SYSTEM CREATOR: Amir Terrorist", C.Y)
    cprint("=" * 50, C.C)
    cprint(" Select Package Level Installation:", C.W)
    cprint("   [1] Ordinary pkg         (Essential Tools)", C.G)
    cprint("   [2] Professional pkg     (Networking & Dev)", C.B)
    cprint("   [3] Very professional pkg (Heavy Cyber Tools)", C.M)
    cprint("=" * 50, C.C)


# ---------- Package sets ----------
PKG_SETS = {
    "1": {
        "title": "Ordinary",
        "color": C.G,
        "pkgs": ["git", "python", "curl", "wget", "nano",
                 "tar", "zip", "unzip", "htop", "fastfetch"],
    },
    "2": {
        "title": "Professional",
        "color": C.B,
        "pkgs": ["git", "python", "nodejs", "clang", "make", "cmake",
                 "golang", "rust", "openssl", "libffi", "libxml2",
                 "libxslt", "sqlite", "nmap", "netcat-openbsd"],
    },
    "3": {
        "title": "Very Professional / Cyber",
        "color": C.M,
        "pkgs": ["git", "python", "clang", "make", "cmake", "nmap",
                 "tcpdump", "torsocks", "perl", "ruby", "libpcap"],
    },
}


def main():
    # Check we are on Termux (pkg available)
    if shutil.which("pkg") is None:
        cprint("[✖] 'pkg' command not found. This script is for Termux only.", C.R)
        sys.exit(1)

    # Loading bars
    clear()
    cprint("=" * 50, C.R)
    cprint("      INITIALIZING CYBERNETIC CORE...", C.M)
    cprint("=" * 50 + "\n", C.R)

    loading_bar("Loading System Modules & Dependencies")
    loading_bar("Bypassing Security Firewalls & Encryption")
    loading_bar("Establishing Secure Terminal Connection")

    # Menu
    banner()
    try:
        choice = input(f"{C.W}root@AmirTerrorist:~#{C.NC} ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        cprint("[✖] Aborted.", C.R)
        sys.exit(1)

    if choice not in PKG_SETS:
        cprint("[✖] Invalid Option Selected! Exiting...", C.R)
        sys.exit(1)

    # Update repos
    cprint("\n[+] Updating Termux Repository...", C.C)
    ok, out = run("pkg update -y && pkg upgrade -y")
    if not ok:
        cprint("[✖] Failed to update repositories.", C.R)
        print(out)
        sys.exit(1)
    cprint("[✔] Repository updated.", C.G)

    # Install
    sel = PKG_SETS[choice]
    cprint(f"\n[+] Installing {sel['title']} Packages...", sel["color"])
    failed = install_packages(sel["pkgs"])

    if failed:
        cprint(f"\n[!] Completed with {len(failed)} skipped package(s): "
               f"{', '.join(failed)}", C.Y)
    else:
        cprint(f"\n[✔] {sel['title']} Packages Installed Successfully!", C.G)

    cprint("\n[★] All operations completed by Amir Terrorist. Stay Secure!", C.Y)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        cprint("\n[✖] Interrupted by user.", C.R)
        sys.exit(130)