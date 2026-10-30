#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Package Installer — CYBER UI EDITION v5 (ULTIMATE SAFE)
Creator: Amir Terrorist
Palette: neon green, cyan, white, red, yellow
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

# ---------- Colors ----------
class C:
    G  = "\033[1;32m"
    G2 = "\033[0;32m"
    C  = "\033[1;36m"
    C2 = "\033[0;36m"
    W  = "\033[1;37m"
    Y  = "\033[1;33m"
    R  = "\033[1;31m"
    D  = "\033[2m"
    B  = "\033[1m"
    NC = "\033[0m"

ANSI_RE = re.compile(r"\033\[[0-9;]*m")

def vlen(s: str) -> int:
    """محاسبه طول رشته بدون احتساب کدهای رنگی ANSI"""
    return len(ANSI_RE.sub("", s))

MATRIX_CHARS = "01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ#$%&@*+=<>/\\|"

ANIMATE = True
_TERM_WIDTH_CACHE = 80

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def term_width(default=60):
    """گرفتن عرض ترمینال با محافظت کامل از مقادیر منفی"""
    global _TERM_WIDTH_CACHE
    try:
        w = shutil.get_terminal_size((default, 24)).columns
        _TERM_WIDTH_CACHE = max(40, w) # حداقل 40 کاراکتر برای جلوگیری از کرش
        return _TERM_WIDTH_CACHE
    except Exception:
        return default

def cprint(text="", color=C.NC, end="\n"):
    sys.stdout.write(f"{color}{text}{C.NC}{end}")
    sys.stdout.flush()

# ---------- Full-screen Matrix rain ----------
def matrix_strip(height=3, color=C.G2, density=0.10):
    if not ANIMATE:
        return
    width = term_width() - 1
    drops = [random.randint(-20, 0) for _ in range(width)]
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

# ---------- HUD ----------
def hud_bar(status="ONLINE", enc="AES-256"):
    w = term_width()
    now = datetime.now().strftime("%H:%M:%S")
    
    left  = f" {C.G}◉{C.NC} {C.W}AMIR{C.NC}"
    mid   = f"{C.C}◆{C.NC} {C.G2}STATUS:{C.NC} {C.G}{status}{C.NC}  {C.C}◆{C.NC} {C.G2}ENC:{C.NC} {C.G}{enc}{C.NC}"
    right = f"{C.G2}{now}{C.NC} {C.G}◉{C.NC} "
    
    # جلوگیری از منفی شدن fill
    fill = max(1, w - vlen(left) - vlen(mid) - vlen(right) - 4)
    inner = f"{left}{' ' * fill}{mid}  {right}"
    
    sys.stdout.write(f"{C.G2}┌{'─'*(w-2)}┐{C.NC}\n")
    sys.stdout.write(f"{C.G2}│{C.NC}{inner[:w-2]}{C.G2}│{C.NC}\n")
    sys.stdout.write(f"{C.G2}└{'─'*(w-2)}┘{C.NC}\n")
    sys.stdout.flush()

def hud_progress(label, pct, color=C.G):
    w = term_width()
    bar_w = max(10, w - 40)
    filled = int(bar_w * (pct / 100.0))
    # محافظت از منفی شدن filled
    filled = max(0, min(filled, bar_w))
    
    bar = f"{color}{'█'*filled}{C.D}{'░'*(bar_w-filled)}{C.NC}"
    lbl = label[:15].ljust(15)
    sys.stdout.write(f"\r{C.G2}▸{C.NC} {C.W}{lbl}{C.NC} {C.G2}[{C.NC}{bar}{C.G2}]{C.NC} {color}{pct:3d}%{C.NC}")
    sys.stdout.flush()

# ---------- Glitch Typing ----------
GLITCH = "!@#$%&*<>/\\|01"

def glitch_type(text, color=C.G, delay=0.008, scramble=True):
    if not ANIMATE:
        cprint(text, color)
        return
    for ch in text:
        if scramble and ch != " " and random.random() < 0.25:
            sys.stdout.write(f"{C.D}{random.choice(GLITCH)}{C.NC}")
            sys.stdout.flush()
            time.sleep(delay * 0.5)
            sys.stdout.write("\b")
        sys.stdout.write(f"{color}{ch}{C.NC}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

# ---------- Frame (Safe-Padding) ----------
def frame(lines, color=C.G, title=None):
    if not lines:
        return
    
    # پیدا کردن بزرگترین خط بدون در نظر گرفتن رنگ‌ها
    inner_w = max(vlen(l) for l in lines) + 4
    if title:
        inner_w = max(inner_w, vlen(title) + 4)

    print(f"{color}╔{'═'*inner_w}╗{C.NC}")
    
    if title:
        t = f" {C.W}{title}{C.NC} "
        pad = inner_w - vlen(t)
        # محافظت: اگر عنوان بزرگتر از کادر بود
        lp = max(0, pad // 2)
        rp = max(0, pad - lp)
        print(f"{color}║{C.NC}{' '*lp}{t}{' '*rp}{color}║{C.NC}")
        print(f"{color}╠{'═'*inner_w}╣{C.NC}")
    
    for l in lines:
        pad = max(0, inner_w - 2 - vlen(l)) # محافظت: هرگز منفی نشود
        print(f"{color}║{C.NC} {l}{' '*pad}{color}║{C.NC}")
    print(f"{color}╚{'═'*inner_w}╝{C.NC}")

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
    cols = [C.G, C.G, C.C, C.C, C.C2, C.G2]
    return [f"{cols[i % len(cols)]}{C.B}{line}{C.NC}" for i, line in enumerate(BANNER)]

def draw_banner():
    clear()
    w = term_width()
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    matrix_strip(height=2)
    cprint()
    
    frame(
        colorize_banner() + [
            f"{C.C} ── T E R R O R I S T  •  C Y B E R  C O R E ──{C.NC}",
            f"{C.G2} [ {C.R}Maker By{C.G2} : {C.R}Amir Terrorist{C.G2} ]{C.NC}",
            f"{C.G2} [ STATUS : {C.G}ONLINE{C.G2} • ENC : {C.G}AES-256{C.G2} ]{C.NC}",
        ],
        color=C.G, title="Terrorist Script v1.0"
    )
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n\n")
    sys.stdout.flush()

def draw_menu():
    w = term_width()
    frame([
        f"{C.W} ╭─[ SELECT PACKAGE LEVEL ]────────╮{C.NC}",
        f"{C.G} │ {C.W}[1]{C.G} ORDINARY PKG     {C.G2}· essential tools{C.NC}",
        f"{C.C} │ {C.W}[2]{C.C} PROFESSIONAL PKG {C.G2}· networking + dev{C.NC}",
        f"{C.G2} │ {C.W}[3]{C.G2} CYBER PKG        {C.G2}· heavy security{C.NC}",
        f"{C.Y} │ {C.W}[4]{C.Y} UPDATE / REFRESH {C.G2}· reload interface{C.NC}",
        f"{C.R} │ {C.W}[5]{C.R} EXIT{C.NC}",
        f"{C.W} ╰─────────────────────────────────╯{C.NC}",
    ], color=C.G)
    sys.stdout.write(f"{C.G}{'─'*w}{C.NC}\n")
    sys.stdout.flush()

# ---------- Wipe & Boot ----------
def wipe_effect():
    if not ANIMATE: return
    w = term_width()
    for _ in range(2):
        sys.stdout.write("\r" + "".join(
            f"{random.choice([C.G, C.C, C.G2])}{random.choice(MATRIX_CHARS)}{C.NC}" for _ in range(w)
        ))
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\r" + " " * w + "\r")
    sys.stdout.flush()

def boot_sequence():
    steps = [
        ("Loading modules", C.G),
        ("Mounting volume", C.G),
        ("Bypassing firewall", C.C),
        ("Secure tunnel", C.G),
        ("Sync clock", C.G2),
        ("Inject manifest", C.C),
    ]
    for label, color in steps:
        for pct in range(0, 101, 20):
            hud_progress(label, pct, color)
            time.sleep(0.01)
        sys.stdout.write("\n")
        sys.stdout.flush()
    cprint(f"{C.G}◉{C.NC} {C.W}All modules loaded.{C.NC}")

# ---------- Run & Install ----------
def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, timeout=300)
        return r.returncode == 0, r.stdout or ""
    except subprocess.TimeoutExpired:
        return False, "Operation Timed Out."
    except Exception as e:
        return False, str(e)

def check_internet():
    cprint(f"\n{C.G2}[>>]{C.NC} {C.W}Checking connection...{C.NC}")
    ok, _ = run("ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1")
    if not ok:
        ok, _ = run("curl -s --max-time 5 https://www.google.com > /dev/null 2>&1")
    
    if ok:
        cprint(f"{C.G}[✔]{C.NC} {C.W}Internet OK.{C.NC}")
    else:
        cprint(f"{C.Y}[!]{C.NC} {C.W}No internet — install may fail.{C.NC}")
    return ok

def install_packages(pkgs):
    failed = []
    total = len(pkgs)
    for i, pkg in enumerate(pkgs, 1):
        pct = int(100 * (i - 1) / total)
        hud_progress(f"pkg: {pkg}", pct, C.G)
        sys.stdout.write("\n"); sys.stdout.flush()

        cprint(f"  {C.G2}┌─{C.NC} {C.W}{pkg}{C.NC}")
        sys.stdout.write(f"  {C.G2}└─>{C.NC} {C.G}Wait...{C.NC} ")
        sys.stdout.flush()
        
        ok, out = run(f"pkg install -y {pkg}")
        if ok:
            cprint(f"{C.G}[✔ OK]{C.NC}")
        else:
            # Safe extraction of error lines
            lines = out.strip().splitlines()
            last = lines[-1][:40] if lines else "unknown error"
            cprint(f"{C.R}[✖ FAIL]{C.NC} {C.D}{last}...{C.NC}")
            failed.append(pkg)
            
    hud_progress("finalizing", 100, C.G)
    sys.stdout.write("\n"); sys.stdout.flush()
    return failed

# ---------- Results ----------
def result_panel(sel_title, total, failed):
    ok = total - len(failed)
    w = term_width()
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    cprint()
    lines = [
        f"{C.W} LEVEL : {C.G}{sel_title}{C.NC}",
        f"{C.W} TOTAL : {C.NC}{total}",
        f"{C.G} OK    : {ok}{C.NC}",
        f"{C.R} FAIL  : {len(failed)}{C.NC}",
    ]
    
    if failed:
        lines.append(f"{C.Y} FAILED LIST:{C.NC}")
        for i in range(0, len(failed), 2):
            chunk = failed[i:i+2]
            row = "  ".join(f"{C.R}▪{C.NC} {item:<12}" for item in chunk)
            lines.append(f"   {row}")
        frame(lines, color=C.Y, title="⚠ WARNING")
    else:
        frame(lines, color=C.G, title="✔ SUCCESS")
        
    cprint()
    glitch_type(f"  [☥] By Amir Terrorist — Stay Secure.", color=C.G, delay=0.005, scramble=False)
    sys.stdout.write(f"{C.G}{'═'*w}{C.NC}\n")
    sys.stdout.flush()

# ---------- Package Sets ----------
PKG_SETS = {
    "1": {"title": "Ordinary", "pkgs": [
        "git", "python", "curl", "wget", "nano", "tar", "zip", "unzip", 
        "htop", "fastfetch", "vim", "tmux", "openssh", "rsync", "jq", 
        "tree", "bat", "fzf", "ripgrep", "fd"
    ]},
    "2": {"title": "Professional", "pkgs": [
        "git", "python", "nodejs", "clang", "make", "cmake",
        "golang", "rust", "openssl", "libffi", "sqlite", "nmap", "netcat-openbsd"
    ]},
    "3": {"title": "Cyber / Heavy", "pkgs": [
        "git", "python", "clang", "make", "cmake", "nmap", "tcpdump", "torsocks", 
        "perl", "ruby", "libpcap", "hydra", "macchanger", "net-tools", "wireshark", 
        "bmon", "proot", "openssl-tool", "libxml2", "libxslt", "w3m"
    ]},
}

# ---------- Auth ----------
CORRECT_PASSWORD = "PowerFull-Terrorist"
MAX_ATTEMPTS = 3
AUTH_ENV_KEY = "AMIR_SKIP_AUTH"

def authenticate():
    # بررسی اینکه آیا ری‌استارت انجام شده یا خیر
    if os.environ.get(AUTH_ENV_KEY) == "1":
        # پاکسازی Env Var بلافاصله بعد از خواندن، تا اجراهای بعدی تحت تأثیر قرار نگیرند
        del os.environ[AUTH_ENV_KEY]
        clear()
        cprint(f"{C.G}[✔] SESSION RESTORED{C.NC} {C.G2}— access granted.{C.NC}")
        time.sleep(0.2)
        return True

    clear()
    w = term_width()
    sys.stdout.write(f"{C.R}{'═'*w}{C.NC}\n")
    frame([
        f"{C.W} [ SECURITY GATE ]{C.NC}",
        f"{C.G2} This terminal is protected.{C.NC}",
        f"{C.G2} Enter access key to continue.{C.NC}",
    ], color=C.R, title="🔒 AUTH REQUIRED")
    sys.stdout.write(f"{C.R}{'═'*w}{C.NC}\n\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            prompt = f"{C.R}┌─[{C.W}auth{C.R}]─[{C.C}secure{C.R}]\n└──╼ {C.W}Password:{C.NC} "
            sys.stdout.write(prompt)
            sys.stdout.flush()
            entered = input().strip()
        except (KeyboardInterrupt, EOFError):
            print()
            cprint("[✖] Aborted.", C.R)
            sys.exit(130)

        if entered == CORRECT_PASSWORD:
            cprint(f"{C.G}[✔] ACCESS GRANTED{C.NC} {C.G2}— welcome, Amir.{C.NC}")
            time.sleep(0.4)
            return True

        remaining = MAX_ATTEMPTS - attempt
        cprint(f"{C.R}[✖] DENIED{C.NC} {C.Y}(attempt {attempt}/{MAX_ATTEMPTS}){C.NC}")
        if remaining > 0:
            cprint(f"{C.G2}[i] {remaining} attempts left.{C.NC}")

    cprint(f"\n{C.R}[!!] Too many failures. Locked.{C.NC}")
    return False

def update_screen():
    wipe_effect()
    clear()
    w = term_width()
    sys.stdout.write(f"{C.C}{'═'*w}{C.NC}\n")
    matrix_strip(height=2)
    cprint()
    frame([
        f"{C.W} [ SYSTEM UPDATE ]{C.NC}",
        f"{C.G2} Refreshing core...{C.NC}",
        f"{C.G2} Reloading interface...{C.NC}",
    ], color=C.C, title="⟳ UPDATE IN PROGRESS")
    cprint()
    
    steps = [
        ("Flushing cache", C.G), ("Sync packages", C.C),
        ("Rebuilding UI", C.G), ("Restarting", C.G2),
    ]
    for label, color in steps:
        for pct in range(0, 101, 20):
            hud_progress(label, pct, color)
            time.sleep(0.01)
        sys.stdout.write("\n"); sys.stdout.flush()

    cprint()
    glitch_type("  [✔] Reloading core...", color=C.G, delay=0.005, scramble=False)
    sys.stdout.write(f"{C.C}{'═'*w}{C.NC}\n")
    sys.stdout.flush()
    time.sleep(0.5)

def restart_script():
    os.environ[AUTH_ENV_KEY] = "1"
    try:
        # اجرای مجدد اسکریپت با حفظ آرگومان‌های خط فرمان
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        cprint(f"{C.R}[✖] Restart failed: {e}{C.NC}")
        sys.exit(1)

# ---------- Main ----------
def parse_args():
    p = argparse.ArgumentParser(description="Termux Package Installer — CYBER UI v5")
    p.add_argument("--no-anim", action="store_true", help="disable animations")
    p.add_argument("--yes", "-y", action="store_true", help="install level 1 non-interactively")
    p.add_argument("--level", choices=list(PKG_SETS.keys()), help="package level")
    return p.parse_args()

def main():
    global ANIMATE
    args = parse_args()
    if args.no_anim:
        ANIMATE = False

    if shutil.which("pkg") is None:
        cprint("[✖] 'pkg' not found. This script is for Termux only.", C.R)
        return 1

    if not authenticate():
        return 403

    hud_bar()
    wipe_effect()
    boot_sequence()
    draw_banner()
    hud_bar()
    draw_menu()

    # دریافت انتخاب
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

    # پردازش انتخاب
    if choice == "5":
        cprint("[*] Connection closed.", C.C); return 0
    if choice == "4":
        update_screen()
        restart_script()
        return 0
    if choice not in PKG_SETS:
        cprint("[✖] Invalid option.", C.R); return 1

    # شروع نصب
    check_internet()

    cprint(f"\n{C.G2}[>>]{C.NC} {C.W}Updating repository...{C.NC}")
    ok, out = run(
        'DEBIAN_FRONTEND=noninteractive pkg update -y && '
        'DEBIAN_FRONTEND=noninteractive pkg upgrade -y '
        '-o Dpkg::Options::="--force-confdef" '
        '-o Dpkg::Options::="--force-confold"'
    )
    
    if not ok:
        cprint(f"{C.R}[!!] Update failed.{C.NC}")
        print("\n".join(out.strip().splitlines()[-3:]))
        cprint(f"{C.Y}[i] Hint: run 'termux-change-repo'{C.NC}")
        return 1
    cprint(f"{C.G}[OK]{C.NC} {C.W}Repository updated.{C.NC}")

    sel = PKG_SETS[choice]
    cprint(f"\n{C.G2}[>>]{C.NC} {C.W}Deploying {sel['title']} stack...{C.NC}\n")
    failed = install_packages(sel["pkgs"])

    result_panel(sel["title"], len(sel["pkgs"]), failed)
    return 0 if not failed else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(); cprint("\n[✖] Interrupted.", C.R); sys.exit(130)