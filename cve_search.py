import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style

def search_cve_for_joomla(version):
    vulnerabilities = []
    
    # MITRE CVE'lerini al
    try:
        mitre_url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=Joomla+{version}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(mitre_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # TableWithRules div'ini bul
            table_div = soup.find('div', {'id': 'TableWithRules'})
            if table_div:
                # Tablo içindeki tüm satırları bul
                rows = table_div.find_all('tr')
                for row in rows:
                    # Başlık satırını atla
                    if row.find('th'):
                        continue
                        
                    # CVE ID ve açıklama hücrelerini bul
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        cve_id = cells[0].text.strip()
                        description = cells[1].text.strip()
                        
                        # Eğer bu CVE daha önce eklenmediyse ekle
                        if not any(v['id'] == cve_id for v in vulnerabilities):
                            vulnerabilities.append({
                                'id': cve_id,
                                'description': description,
                                'cvss_score': 'N/A',
                                'published': 'N/A',
                                'source': 'MITRE'
                            })
    except Exception as e:
        print(f"MITRE search error: {e}")

    return vulnerabilities

def print_vulnerabilities(vulnerabilities):
    if not vulnerabilities:
        print("\nNo CVEs found for this version.")
        return
    
    print(f"\n{Fore.BLUE}Vulnerabilities Found:{Style.RESET_ALL}")
    print("=" * 80)
    
    mitre_vulns = [v for v in vulnerabilities if v['source'] == 'MITRE']
    
    if mitre_vulns:
        print(f"\n{Fore.GREEN}CVEs from the MITRE CVE Database:{Style.RESET_ALL}")
        print("-" * 80)
        for vuln in mitre_vulns:
            print(f"\nCVE ID: {vuln['id']}")
            print(f"Description: {vuln['description']}")
            print("-" * 80) 