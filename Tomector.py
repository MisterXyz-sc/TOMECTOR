import requests
import socket
from urllib.parse import urlparse
import time
from colorama import Fore, Style, init
import os
import sys
import signal

# Inisialisasi colorama
init(autoreset=True)

# Banner
def print_banner():
    banner = f"""
    {Fore.RED}╔╦╗╔═╗╔╦╗╔═╗╔═╗╔╦╗╔═╗╦═╗
    {Fore.RED} ║ ║ ║║║║║╣ ║   ║ ║ ║╠╦╝
    {Fore.RED} ╩ ╚═╝╩ ╩╚═╝╚═╝ ╩ ╚═╝╩╚═
    {Fore.GREEN}By: {Fore.YELLOW}MisterXyz
    {Fore.CYAN}===========================
    """
    print(banner)

def autoketik(teks):
  for karakter in teks + "\n":
    sys.stdout.write(karakter)
    sys.stdout.flush()
    time.sleep(0.050)

def tangani_ctrl_c(sig, frame):
  autoketik(f"{Fore.RED}Program Telah Di Berhentikan")
  time.sleep(0.2)
  os.system("clear")
  exit()

# Animasi loading sederhana
def loading_animation(message):
    for _ in range(3):
        for char in "|/-\\":
            print(f"\r{Fore.YELLOW}{message} {char}", end="", flush=True)
            time.sleep(0.1)
    print("\r" + " " * (len(message) + 2) + "\r", end="", flush=True)

# Fungsi untuk memindai port
def scan_ports(domain, ports):
    print(f"{Fore.CYAN}Memindai port pada {Fore.GREEN}{domain}...")
    for port in ports:
        loading_animation(f"Memindai port {port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            print(f"{Fore.GREEN}Port {port} terbuka")
        else:
            print(f"{Fore.RED}Port {port} tertutup")
        sock.close()

# Fungsi untuk mencari direktori
def find_directories(base_url, directories):
    print(f"{Fore.CYAN}Mencari direktori pada {Fore.GREEN}{base_url}...")
    for directory in directories:
        url = base_url + "/" + directory
        loading_animation(f"Mencari direktori {directory}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{Fore.GREEN}Direktori ditemukan: {url}")
            else:
                print(f"{Fore.RED}Direktori tidak ditemukan: {url}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Gagal mengakses {url}: {e}")

# Fungsi untuk deteksi SQL Injection sederhana
def check_sql_injection(url):
    print(f"{Fore.CYAN}Memeriksa SQL Injection pada {Fore.GREEN}{url}...")
    test_payload = "' OR '1'='1"
    loading_animation("Memeriksa SQL Injection")
    try:
        response = requests.get(url + test_payload)
        if "error" in response.text.lower() or "syntax" in response.text.lower():
            print(f"{Fore.RED}Kemungkinan SQL Injection terdeteksi di {url}")
        else:
            print(f"{Fore.GREEN}Tidak ditemukan indikasi SQL Injection di {url}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Gagal memeriksa SQL Injection: {e}")

# Fungsi untuk mencari subdomain
def enumerate_subdomains(domain):
    print(f"{Fore.CYAN}Mencari subdomain untuk {Fore.GREEN}{domain}...")
    # Wordlist sederhana untuk subdomain
    wordlist = ["www", "mail", "ftp", "test", "dev", "admin", "web", "api", "blog", "shop"]
    for subdomain in wordlist:
        full_domain = f"{subdomain}.{domain}"
        loading_animation(f"Mencari subdomain {full_domain}")
        try:
            # Cek apakah subdomain memiliki IP
            ip = socket.gethostbyname(full_domain)
            print(f"{Fore.GREEN}Subdomain ditemukan: {full_domain} -> {ip}")
        except socket.error:
            print(f"{Fore.RED}Subdomain tidak ditemukan: {full_domain}")

# Main function
def main():
    os.system("clear")  # Membersihkan layar
    print_banner()
    target = input(f"{Fore.CYAN}Masukkan URL target (contoh: http://example.com): {Fore.GREEN}").strip()
    parsed_url = urlparse(target)
    domain = parsed_url.hostname  # Ambil hostname (tanpa port)
    port = parsed_url.port  # Ambil port jika ada

    # Jika port tidak ada dalam URL, gunakan port default
    if not port:
        if parsed_url.scheme == "http":
            port = 80
        elif parsed_url.scheme == "https":
            port = 443

    # Daftar port yang akan dipindai
    ports_to_scan = [port]  # Fokus pada port yang diberikan

    # Daftar direktori yang akan dicari
    directories_to_check = ["admin", "login", "wp-admin", "test", "backup"]

    while True:
        print(f"\n{Fore.CYAN}Menu:")
        print(f"{Fore.YELLOW}1. {Fore.CYAN}Pindai Port")
        print(f"{Fore.YELLOW}2. {Fore.CYAN}Cari Direktori")
        print(f"{Fore.YELLOW}3. {Fore.CYAN}Periksa SQL Injection")
        print(f"{Fore.YELLOW}4. {Fore.CYAN}Enumerasi Subdomain")
        print(f"{Fore.YELLOW}5. {Fore.RED}Keluar")
        choice = input(f"{Fore.CYAN}Pilih opsi (1-5): {Fore.GREEN}")

        if choice == "1":
            os.system("clear")
            print_banner()
            scan_ports(domain, ports_to_scan)
        elif choice == "2":
            os.system("clear")
            print_banner()
            find_directories(target, directories_to_check)
        elif choice == "3":
            os.system("clear")
            print_banner()
            check_sql_injection(target)
        elif choice == "4":
            os.system("clear")
            print_banner()
            enumerate_subdomains(domain)
        elif choice == "5":
            print(f"{Fore.RED}Keluar...")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Silakan coba lagi.")

signal.signal(signal.SIGINT, tangani_ctrl_c)

if __name__ == "__main__":
    main
