cat << 'EOF' > termux_pkg_Terrorist.sh
#!/bin/bash

# Colors
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
Y='\033[1;33m'
C='\033[1;36m'
M='\033[1;35m'
W='\033[1;37m'
NC='\033[0m'

clear

# Function for futuristic loading bar
loading_bar() {
    local text="$1"
    echo -e "${C}[*] $text${NC}"
    for i in {0..100..4}; do
        printf "\r${G}["
        for ((j=0; j<=i; j+=4)); do printf "#"; done
        for ((j=i; j<100; j+=4)); do printf " "; done
        printf "] %3d%%${NC}" "$i"
        sleep 0.03
    done
    echo -e "\n"
}

# 3 Successive loading bars
echo -e "${R}==================================================${NC}"
echo -e "${M}         INITIALIZING CYBERNETIC CORE...          ${NC}"
echo -e "${R}==================================================${NC}\n"

loading_bar "Loading System Modules & Dependencies"
loading_bar "Bypassing Security Firewalls & Encryption"
loading_bar "Establishing Secure Terminal Connection"

clear

# Banner with AMIR design
echo -e "${R}==================================================${NC}"
echo -e "${R}     _    __  __ ___ ____                         ${NC}"
echo -e "${R}    / \  |  \/  |_ _|  _ \                        ${NC}"
echo -e "${R}   / _ \ | |\/| || || |_) |                       ${NC}"
echo -e "${R}  / ___ \| |  | || ||  _ <                        ${NC}"
echo -e "${R} /_/   \_\_|  |_|___|_| \_\                       ${NC}"
echo -e "${C}==================================================${NC}"
echo -e "${Y}        SYSTEM CREATOR: Amir Terrorist           ${NC}"
echo -e "${C}==================================================${NC}"
echo -e "${W} Select Package Level Installation:${NC}"
echo -e "${G}   [1] Ordinary pkg         ${NC}(Essential Tools)"
echo -e "${B}   [2] Professional pkg     ${NC}(Networking & Dev)"
echo -e "${M}   [3] Very professional pkg ${NC}(Heavy Cyber Tools)"
echo -e "${C}==================================================${NC}"
read -p "root@AmirTerrorist:~# " choice

# Update package manager first
echo -e "\n${C}[+] Updating Termux Repository...${NC}"
pkg update -y && pkg upgrade -y

case $choice in
    1)
        echo -e "\n${G}[+] Installing Ordinary Packages...${NC}"
        pkg install -y git python python3 curl wget nano tar zip unzip neofetch htop
        echo -e "\n${G}[✔] Ordinary Packages Installed Successfully!${NC}"
        ;;
    2)
        echo -e "\n${B}[+] Installing Professional Packages...${NC}"
        pkg install -y git python python3 nodejs clang make cmake golang rust openssl libffi libxml2 libxslt sqlite nmap netcat
        echo -e "\n${G}[✔] Professional Packages Installed Successfully!${NC}"
        ;;
    3)
        echo -e "\n${M}[+] Installing Very Professional & Cyber Packages...${NC}"
        pkg install -y git python python3 clang make cmake nmap hydra sqlmap metasploit-framework torsocks wireshark tcpdump john perl ruby libpcap
        echo -e "\n${G}[✔] Very Professional Packages Installed Successfully!${NC}"
        ;;
    *)
        echo -e "\n${R}[✖] Invalid Option Selected! Exiting...${NC}"
        exit 1
        ;;
esac

echo -e "\n${Y}[★] All operations completed by Amir Terrorist. Stay Secure!${NC}"
EOF		