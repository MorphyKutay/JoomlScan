import requests
from urllib.parse import urljoin
from colorama import Fore, Style

def find_admin_panel(url):

    admin_paths = [
        '/administrator/',
        '/admin/',
        '/joomla/administrator/',
        '/joomla/admin/',
        '/wp-admin/',
        '/wp-login.php',
        '/administrator/index.php',
        '/admin/index.php'
    ]
    
    found_paths = []
    
    for path in admin_paths:
        full_url = urljoin(url, path)
        try:
            response = requests.get(full_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                if any(keyword in response.text.lower() for keyword in ['joomla', 'administrator', 'login', 'username', 'password']):
                    found_paths.append(full_url)
        except requests.RequestException:
            continue
    
    return found_paths

def print_admin_panels(admin_panels):

    if admin_panels:
        print(f"\n{Fore.GREEN}[+] Available Admin Panels:{Style.RESET_ALL}")
        for panel in admin_panels:
            print(f"{Fore.YELLOW}[*] {panel}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[-] Admin panel not found{Style.RESET_ALL}") 