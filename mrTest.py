#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Package Installer — CYBER UI EDITION v3 (GRAPHIC / HACKER)
Creator: Amir Terrorist
Palette: neon green, cyan, white, red, yellow  (NO purple / NO pink)
Features: full-screen matrix rain, HUD status bar, double neon frames,
          glitch typing, two-layer progress bar, result panel.
"""

import os
import re
import sys
import time
import shutil
import random
import argparse
import subprocess
from datetime import datetime

if sys.version_info < (3, 6):
    sys.stderr.write("Python 3.6+ required.\n")
    sys.exit(1)

# ---------- Colors (green / cyan / white / red / yellow only) ----------
class C:
    G  = "\033[1;32m"      # neon green
    G2 = "\033[0;32m"      # dim green
    C  = "\033[1;36m"      # cyan
    C2 = "\033[0;36m"      # dim cyan
    W  = "\033[1;37m"      # white
    Y  = "\033[1;33m"      # yellow
    R  = "\033[1;31m"      # red
    D  = "\033[2m"         # dim
    B  = "\033[1m"         # bold
    NC = "\033[0m"

ANSI_RE = re.compile(r"\033\[[0-9;]*m")
def vlen(s: str) -> int:
    return len(ANSI_RE.sub("", s))

MATRIX_CHARS = "01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ#$%&@*+=<>/\\|"

ANIMATE = True

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def term_width(default=80):
    try:
        return shutil.get_terminal_size((default, 24)).columns
    except Exception:
        return default

def term_height(default=24):
    try:
        return shutil.get_terminal_size((80, default)).lines
    except Exception:
        return default

# ---------- Low-level ----------
def cprint(text="", color=C.NC, end="\n"):
    sys.stdout.write(f"{color}{text}{C.NC}{end}")
    sys.stdout.flush()

# ---------- Full-screen matrix rain (persistent during whole run) ----------
def _make_drops(width):
    return [random.randint(-20, 0) for _ in range(width)]

def matrix_strip(height=6, color=C.G2, density=0.10):
    """یک نوار ماتریکس با ارتفاع مشخص چاپ می‌کند و برمی‌گردد."""
    if not ANIMATE:
        return
    width = term_width() - 1
    drops = _make_drops(width)
    for _ in range(height):
        line = []
        for x in range(width):
            if drops[x] > 0 and random.random() < density:
                line.append(f"{C.G}{random.choice(MATRIX_CHARS)}{C.NC}")
            elif drops[x] > 0:
                line.append(f"{color}{random.choice(MATRIX_CHARS)}{C.NC}")
            else:
                line.append(" ")
        sys.stdout.write("".join(line) + "\n")
        sys.stdout.flush()
        for x in range(width):
            if drops[x] > 0:
                drops[x] -= 1
            elif random.random() < 0.03:
                drops[x] = random.randint(3, 10)
        time.sleep(0.04)

# ---------- HUD status bar ----------
def hud_bar(status="ONLINE", enc="AES-256"):
    w = term_width()
    now = datetime.now().strftime("%H:%M:%S")
    left  = f" {C.G}●{C.NC} {C.W}AMIR-TERMINAL{C.NC}"
    mid   = f"{C.C}◆{C.NC} {C.G2}STATUS:{C.NC} {C.G}{status}{C.NC}  {C.C}◆{C.NC} {C.G2}ENC:{C.NC} {C.G}{enc}{C.NC}"
    right = f"{C.G2}{now}{C.NC} {C.G}●{C.NC} "
    raw_left  = vlen(left)
    raw_mid   = vlen(mid)
    raw_right = vlen(right)
    fill = max(0, w - raw_left - raw_mid - raw_right - 4)
    line = f"{C.G2}┌{'─'*(w-2)}┐{C.NC}\n"
    inner = f"{left}{' ' * fill}{mid}  {right}"
    # pad بر اساس vlen
    pad = max(0, (w - 2) - vlen(inner))
    line += f"{C.G2}│{C.NC}{inner}{' ' * pad}{C.G2}│{C.NC}\n"
    line += f"{C.G2}└{'─'*(w-2)}┘{C.NC}"
    sys.stdout.write(line + "\n")
    sys.stdout.flush()

def hud_progress(label, pct, color=C.G):
    """HUD خط پایین با نوار پیشرفت."""
    w = max(30, term_width())
    bar_w = max(10, w - 40)
    filled = int(bar_w * pct / 100)
    bar = f"{color}{'█'*filled}{C.D}{'░'*(bar_w-filled)}{C.NC}"
    sys.stdout.write(f"\r{C.G2}▸{C.NC} {C.W}{label:<22}{C.NC} {C.G2}[{C.NC}{bar}{C.G2}]{C.NC} {color}{pct:3d}%{C.NC}")
    sys.stdout.flush()

# ---------- Glitch typing ----------
GLITCH = "!@#$%&*<>/\\|01"

def glitch_type(text, color=C.G, delay=0.008, scramble=True):
    if not ANIMATE:
        cprint(text, color)
        return
    out = ""
    for ch in text:
        if scramble and ch != " " and random.random() < 0.25:
            sys.stdout.write(f"{C.D}{random.choice(GLITCH)}{C.NC}")
            sys.stdout.flush()
            time.sleep(delay * 0.5)
            sys.stdout.write("\b")
        sys.stdout.write(f"{color}{ch}{C.NC}")
        sys.stdout.flush()
        out += ch
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

# ---------- Double neon frame ----------
def frame(lines, color=C.G, title=None):
    inner_w = max(vlen(l) for l in lines) + 4
    if title:
        inner_w = max(inner_w, vlen(title) + 4)
    top  = f"{color}╔{'═'*inner_w}╗{C.NC}"
    bot  = f"{color}╚{'═'*inner_w}╝{C.NC}"
    print(top)
    if title:
        t = f" {C.W}{title}{C.NC} "
        pad = inner_w - vlen(t)
        lp = pad // 2
        rp = pad - lp
        print(f"{color}║{C.NC}{' '*lp}{t}{' '*rp}{color}║{C.NC}")
        print(f"{color}╠{'═'*inner_w}╣{C.NC}")
    for l in lines:
        pad = inner_w - 2 - vlen(l)
        print(f"{color}║{C.NC} {l}{' '*pad}{color}║{C.NC}")
    print(bot)

# ---------- Banner ----------
BANNER = [
    r"  █████╗ ███╗   ███╗██╗██████╗ ",
    r" ██╔══██╗████╗ ████║██║██╔══██╗",
    r" ███████║██╔████╔██║██║██████╔╝",
    r" ██╔══██║██║╚██╔╝██║██║██╔══██╗",
    r" ██║  ██║██║ ╚═╝ ██║██║██║  ██║",
    r" ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝",
]

def colorize_banner():
    """گرادیان سبز → سایان روی بنر."""
    cols = [C.G, C.G, C.C, C.C, C.C2, C.G2]
    out = []
    for i, line in enumerate(BANNER):
        out.append(f"{cols[i % len(cols)]}{C.B}{line}{C.NC}")
    return out

def draw_banner():
    clear()
    # خط اسکن بالا
    w = term_width()
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    sys.stdout.flush()
    # ماتریکس پس‌زمینه (کوتاه)
    matrix_strip(height=3)
    cprint()
    frame(
        colorize_banner() + [
            f"{C.C}    ── T E R R O R I S T  •  C Y B E R  C O R E ──{C.NC}",
            f"{C.G2}    [ SYSTEM CREATOR : {C.G}Amir Terrorist{C.G2} ]{C.NC}",
            f"{C.G2}    [ STATUS : {C.G}ONLINE{C.G2}  •  ENC : {C.G}AES-256{C.G2} ]{C.NC}",
        ],
        color=C.G, title="CYBERNETIC CORE // v3.0"
    )
    # خط اسکن پایین
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n\n")
    sys.stdout.flush()

def draw_menu():
    w = term_width()
    frame([
        f"{C.W}  ╭─[ SELECT PACKAGE LEVEL ]─────────────────╮{C.NC}",
        f"{C.G}  │ {C.W}[1]{C.G}  ORDINARY PKG      {C.G2}· essential tools{C.NC}",
        f"{C.C}  │ {C.W}[2]{C.C}  PROFESSIONAL PKG  {C.G2}· networking + dev{C.NC}",
        f"{C.G2}  │ {C.W}[3]{C.G2}  CYBER PKG         {C.G2}· heavy security tools{C.NC}",
        f"{C.R}  │ {C.W}[4]{C.R}  EXIT{C.NC}",
        f"{C.W}  ╰──────────────────────────────────────────╯{C.NC}",
    ], color=C.G)
    sys.stdout.write(f"{C.G}{'─'*w}{C.NC}\n")
    sys.stdout.flush()

# ---------- Glitch full-screen wipe before menu ----------
def wipe_effect():
    if not ANIMATE:
        return
    w = term_width()
    for _ in range(3):
        sys.stdout.write("\r" + "".join(
            f"{random.choice([C.G, C.C, C.G2])}{random.choice(MATRIX_CHARS)}{C.NC}"
            for _ in range(w)
        ))
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\r" + " " * w + "\r")
    sys.stdout.flush()

# ---------- Loading sequence ----------
def boot_sequence():
    steps = [
        ("Loading kernel modules", C.G),
        ("Mounting encrypted volume", C.G),
        ("Bypassing firewall layer 7", C.C),
        ("Establishing secure tunnel", C.G),
        ("Synchronizing clock (NTP)", C.G2),
        ("Injecting package manifest", C.C),
    ]
    for label, color in steps:
        for pct in range(0, 101, 10):
            hud_progress(label, pct, color)
            if ANIMATE:
                time.sleep(0.008)
        sys.stdout.write("\n")
        sys.stdout.flush()
    cprint(f"{C.G}●{C.NC} {C.W}All modules loaded.{C.NC}")

# ---------- Run command ----------
def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        return r.returncode == 0, r.stdout or ""
    except Exception as e:
        return False, str(e)

# ---------- Install with progress ----------
def install_packages(pkgs):
    failed = []
    total = len(pkgs)
    for i, pkg in enumerate(pkgs, 1):
        pct = int(100 * (i - 1) / total)
        hud_progress(f"installing {pkg}", pct, C.G)
        sys.stdout.write("\n"); sys.stdout.flush()
        cprint(f" {C.G}▶{C.NC} {C.W}{pkg}{C.NC}", C.NC, end="  ")
        ok, out = run(f"pkg install -y {pkg}")
        if ok:
            cprint(f"{C.G}[✔ OK]{C.NC}")
        else:
            last = (out.strip().splitlines() or ["unknown"])[-1][:90]
            cprint(f"{C.R}[✖ FAIL]{C.NC} {C.D}{last}{C.NC}")
            failed.append(pkg)
    hud_progress("finalizing", 100, C.G)
    sys.stdout.write("\n"); sys.stdout.flush()
    return failed

# ---------- Result panel ----------
def result_panel(sel_title, total, failed):
    ok = total - len(failed)
    w = term_width()
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    cprint()
    lines = [
        f"{C.W}  LEVEL : {C.G}{sel_title}{C.NC}",
        f"{C.W}  TOTAL : {C.NC}{total}",
        f"{C.G}  OK    : {ok}{C.NC}",
        f"{C.R}  FAIL  : {len(failed)}{C.NC}",
    ]
    if failed:
        lines.append(f"{C.Y}  FAILED: {', '.join(failed)}{C.NC}")
        frame(lines, color=C.Y, title="⚠  COMPLETED WITH WARNINGS")
    else:
        frame(lines, color=C.G, title="✔  MISSION ACCOMPLISHED")
    cprint()
    glitch_type(f"  [★] Operations by Amir Terrorist — Stay Secure.",
                color=C.G, delay=0.006, scramble=False)
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    sys.stdout.flush()

# ---------- Package sets ----------
PKG_SETS = {
    "1": {"title": "Ordinary", "color": C.G,
          "pkgs": ["git", "python", "curl", "wget", "nano",
                   "tar", "zip", "unzip", "htop", "fastfetch"]},
    "2": {"title": "Professional", "color": C.C,
          "pkgs": ["git", "python", "nodejs", "clang", "make", "cmake",
                   "golang", "rust", "openssl", "libffi",
                   "sqlite", "nmap", "netcat-openbsd"]},
    "3": {"title": "Cyber / Heavy", "color": C.G,
          "pkgs": ["git", "python", "clang", "make", "cmake", "nmap",
                   "tcpdump", "torsocks", "perl", "ruby", "libpcap"]},
}

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="Termux Package Installer — CYBER UI v3")
    p.add_argument("--no-anim", action="store_true", help="disable animations")
    p.add_argument("--yes", "-y", action="store_true", help="install level 1 non-interactively")
    p.add_argument("--level", choices=list(PKG_SETS.keys()), help="package level")
    return p.parse_args()

# ---------- Main ----------
def main():
    global ANIMATE
    args = parse_args()
    if args.no_anim:
        ANIMATE = False

    if shutil.which("pkg") is None:
        cprint("[✖] 'pkg' not found. This script is for Termux only.", C.R)
        return 1

    hud_bar()
    wipe_effect()
    boot_sequence()
    draw_banner()
    hud_bar()
    draw_menu()

    if args.level:
        choice = args.level
    elif args.yes:
        choice = "1"
    else:
        try:
            sys.stdout.write(
                f"{C.G}┌─[{C.R}root@AmirTerrorist{C.G}]─[{C.C}~{C.G}]\n"
                f"└──╼ {C.W}${C.NC} "
            )
            sys.stdout.flush()
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            print(); cprint("[✖] Aborted.", C.R); return 130

    if choice == "4":
        cprint("[*] Connection closed.", C.C); return 0
    if choice not in PKG_SETS:
        cprint("[✖] Invalid option.", C.R); return 1

    # Update repos
    cprint(f"\n{C.G2}[>>]{C.NC} {C.W}Updating repository index...{C.NC}")
    ok, out = run(
        'pkg update -y && '
        'pkg upgrade -y -o Dpkg::Options::="--force-confdef" '
        '-o Dpkg::Options::="--force-confold"'
    )
    if not ok:
        cprint(f"{C.R}[!!] Update failed.{C.NC}")
        print("\n".join(out.strip().splitlines()[-5:]))
        cprint(f"{C.Y}[i] Hint: run 'termux-change-repo'{C.NC}")
        return 1
    cprint(f"{C.G}[OK]{C.NC} {C.W}Repository updated.{C.NC}")

    sel = PKG_SETS[choice]
    cprint(f"\n{C.G2}[>>]{C.NC} {C.W}Deploying {sel['title']} stack...{C.NC}\n")
    failed = install_packages(sel["pkgs"])

    result_panel(sel["title"], len(sel["pkgs"]), failed)
    return 0 if not failed else 1

# ---------- Entry ----------
if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(); cprint("\n[✖] Interrupted.", C.R); sys.exit(130)