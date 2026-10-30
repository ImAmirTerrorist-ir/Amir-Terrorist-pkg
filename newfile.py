#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Package Installer  —  CYBER UI EDITION
Creator: Amir Terrorist
"""

import os
import sys
import time
import shutil
import random
import subprocess

# ---------- Colors ----------
class C:
    R = "\033[1;31m"; G = "\033[1;32m"; B = "\033[1;34m"
    Y = "\033[1;33m"; C = "\033[1;36m"; M = "\033[1;35m"
    W = "\033[1;37m"; NC = "\033[0m"
    BG = "\033[40m"          # پس‌زمینه مشکی
    DIM = "\033[2m"
    BOLD = "\033[1m"

MATRIX_CHARS = "01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ#$%&@*+=<>"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def cprint(text="", color=C.NC, end="\n"):
    print(f"{color}{text}{C.NC}", end=end)
    sys.stdout.flush()

# ---------- Cyber Background (Matrix rain) ----------
def matrix_rain(duration=2.0, width=None, height=12):
    """یک پس‌زمینه ماتریکسی برای چند لحظه رندر می‌کند."""
    try:
        width = width or shutil.get_terminal_size((80, 20)).columns
    except Exception:
        width = 80
    cols = [random.randint(0, height) for _ in range(width)]
    end = time.time() + duration
    while time.time() < end:
        line = ""
        for x in range(width):
            if random.random() < 0.08:
                line += f"{C.G}{random.choice(MATRIX_CHARS)}{C.NC}"
            elif cols[x] > 0:
                line += f"{C.DIM}{C.G}{random.choice(MATRIX_CHARS)}{C.NC}"
            else:
                line += " "
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        for x in range(width):
            if random.random() < 0.15:
                cols[x] = max(0, cols[x] - 1)
            elif random.random() < 0.05:
                cols[x] = random.randint(0, height)
        time.sleep(0.05)
    print()

# ---------- Typing effect ----------
def type_text(text, color=C.G, delay=0.012, end="\n"):
    for ch in text:
        sys.stdout.write(f"{color}{ch}{C.NC}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)

# ---------- Neon frame ----------
def neon_frame(lines, color=C.C, pad=1):
    width = max(len(l) for l in lines) + pad * 2 + 2
    top = f"{color}╔{'═' * (width - 2)}╗{C.NC}"
    bot = f"{color}╚{'═' * (width - 2)}╝{C.NC}"
    print(top)
    for l in lines:
        pad_r = width - 2 - pad - len(l)
        print(f"{color}║{C.NC}{' ' * pad}{l}{' ' * pad_r}{color}║{C.NC}")
    print(bot)

# ---------- Loading bar ----------
def loading_bar(text, delay=0.02):
    cprint(f"[*] {text}", C.C)
    total = 100
    step = 4
    for i in range(0, total + 1, step):
        filled = i // step
        empty = (total // step) - filled
        bar = "█" * filled + "░" * empty
        sys.stdout.write(f"\r{C.G}▕{bar}▏ {i:3d}%{C.NC}")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

# ---------- Run command ----------
def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def install_packages(pkgs):
    failed = []
    for pkg in pkgs:
        cprint(f"[+] Installing {pkg} ...", C.C)
        ok, out = run(f"pkg install -y {pkg}")
        if not ok:
            cprint(f"[!] Failed: {pkg} (skipped)", C.Y)
            failed.append(pkg)
        else:
            cprint(f"[✔] {pkg} installed", C.G)
    return failed

# ---------- Cyber Banner ----------
def banner():
    clear()
    matrix_rain(duration=1.2, height=10)
    cprint()
    neon_frame([
        f"{C.M}{C.BOLD}        █████╗ ███╗   ███╗██╗██████╗{C.NC}",
        f"{C.M}{C.BOLD}       ██╔══██╗████╗ ████║██║██╔══██╗{C.NC}",
        f"{C.M}{C.BOLD}       ███████║██╔████╔██║██║██████╔╝{C.NC}",
        f"{C.M}{C.BOLD}       ██╔══██║██║╚██╔╝██║██║██╔══██╗{C.NC}",
        f"{C.M}{C.BOLD}       ██║  ██║██║ ╚═╝ ██║██║██║  ██║{C.NC}",
        f"{C.M}{C.BOLD}       ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝{C.NC}",
        f"{C.C}     T E R R O R I S T   •   C Y B E R   C O R E{C.NC}",
    ], color=C.C)
    cprint()
    type_text("   >> SYSTEM CREATOR : Amir Terrorist", C.Y, 0.01)
    type_text("   >> STATUS         : ONLINE  •  ENCRYPTED", C.G, 0.01)
    cprint()
    neon_frame([
        f"{C.W}  Select Package Level Installation:{C.NC}",
        f"{C.G}  [1]  Ordinary pkg          (Essential Tools){C.NC}",
        f"{C.B}  [2]  Professional pkg      (Networking & Dev){C.NC}",
        f"{C.M}  [3]  Very professional pkg (Heavy Cyber Tools){C.NC}",
    ], color=C.M)
    cprint()

# ---------- Package sets ----------
PKG_SETS = {
    "1": {"title": "Ordinary", "color": C.G,
          "pkgs": ["git", "python", "curl", "wget", "nano",
                   "tar", "zip", "unzip", "htop", "fastfetch"]},
    "2": {"title": "Professional", "color": C.B,
          "pkgs": ["git", "python", "nodejs", "clang", "make", "cmake",
                   "golang", "rust", "openssl", "libffi", "libxml2",
                   "libxslt", "sqlite", "nmap", "netcat-openbsd"]},
    "3": {"title": "Very Professional / Cyber", "color": C.M,
          "pkgs": ["git", "python", "clang", "make", "cmake", "nmap",
                   "tcpdump", "torsocks", "perl", "ruby", "libpcap"]},
}

def main():
    if shutil.which("pkg") is None:
        cprint("[✖] 'pkg' command not found. This script is for Termux only.", C.R)
        sys.exit(1)

    clear()
    matrix_rain(duration=1.5, height=14)
    cprint("=" * 60, C.R)
    type_text("      INITIALIZING CYBERNETIC CORE...", C.M, 0.015)
    cprint("=" * 60 + "\n", C.R)

    loading_bar("Loading System Modules & Dependencies")
    loading_bar("Bypassing Security Firewalls & Encryption")
    loading_bar("Establishing Secure Terminal Connection")

    banner()
    try:
        choice = input(f"{C.G}┌─[{C.R}root@AmirTerrorist{C.G}]─[{C.C}~{C.G}]\n└──╼ {C.W}${C.NC} ").strip()
    except (KeyboardInterrupt, EOFError):
        print(); cprint("[✖] Aborted.", C.R); sys.exit(1)

    if choice not in PKG_SETS:
        cprint("[✖] Invalid Option Selected! Exiting...", C.R)
        sys.exit(1)

    cprint("\n[+] Updating Termux Repository...", C.C)
    ok, out = run("pkg update -y && pkg upgrade -y")
    if not ok:
        cprint("[✖] Failed to update repositories.", C.R)
        print(out); sys.exit(1)
    cprint("[✔] Repository updated.", C.G)

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
        print(); cprint("\n[✖] Interrupted by user.", C.R); sys.exit(130)