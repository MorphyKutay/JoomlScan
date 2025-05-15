import requests
import argparse
from version import *
from cve_search import search_cve_for_joomla, print_vulnerabilities
from admin_finder import find_admin_panel, print_admin_panels
import re
import os
from colorama import init, Fore, Style
from pyfiglet import Figlet

# Colorama'yı başlat
init()

def print_banner():
    f = Figlet(font='slant')
    banner = f.renderText('JoomlScan')
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Joomla Vulnerability Scanner{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Author: MorphyKutay{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Description: A tool to scan Joomla sites for vulnerabilities and detect their versions.{Style.RESET_ALL}")
    print("=" * 50)

def main():    
    
    if os.name == 'nt':
        os.system('cls')
    else:   
        os.system('clear') 
    
    # Banner'ı göster
    print_banner()
    
    parser = argparse.ArgumentParser(description='Joomla Scan Tool')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    
    args = parser.parse_args()
    
    # Argümanları kullan
    target_url = args.url
    output_file = args.output
    
    if target_url:
        # Admin panelini ara
        print(f"\n{Fore.CYAN}[*] Searching for admin panel...{Style.RESET_ALL}")
        admin_panels = find_admin_panel(target_url)
        print_admin_panels(admin_panels)
        
        # Tüm versiyon tespiti yöntemlerini dene
        version = None
        
        # 1. X-Meta-Generator ile dene
        version = detect_joomla_version_x_meta_generator(target_url)
        
        # 2. XML dosyaları ile dene
        if not version:
            version = detect_joomla_version_joomla_xml(target_url)
        
        # 3. Diğer dosyalar ile dene
        if not version:
            version = detect_joomla_version_from_files(target_url)
        
        # 4. README.txt ile dene
        if not version:
            version = detect_joomla_version_from_readme(target_url)
        
        # Versiyon string'ini temizle
        if version:
            version = clean_version_string(version)
            print(f"\n{Fore.RED}Joomla Version Found:{Style.RESET_ALL}\n"+"*"*20+f"\nJoomla {version}\n"+"*"*20)
            
            version_number = re.search(r'\d+\.\d+(\.\d+)?', version)
            if version_number:
                version_number = version_number.group()
                vulnerabilities = search_cve_for_joomla(version_number)
                print_vulnerabilities(vulnerabilities)
        else:
            print("*"*20+"\nJoomla version not detected\n"+"*"*20)
        
if __name__ == "__main__":
    main()
