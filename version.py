import re
import requests
import xml.etree.ElementTree as ET

vers = [
    'administrator/manifests/files/joomla.xml',
    'language/en-GB/en-GB.xml',
    'administrator/components/com_content/content.xml',
    'administrator/components/com_plugins/plugins.xml',
    'administrator/components/com_media/media.xml',
    'mambots/content/moscode.xml'
]

version_files = [
    'language/en-GB/en-GB.xml',
    'templates/system/css/system.css',
    'media/system/js/mootools-more.js',
    'language/en-GB/en-GB.ini',
    'htaccess.txt',
    'language/en-GB/en-GB.com_media.ini'
]

def detect_joomla_version_x_meta_generator(url):
    try:
        response = requests.get(url)
        if 'X-Meta-Generator' in response.headers:
            meta_generator = response.headers['X-Meta-Generator']
            version_match = re.search(r'[0-9]+(\.[0-9]+)+', meta_generator)
            if version_match:
                return f"Joomla {version_match.group()}"
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

def detect_joomla_version_joomla_xml(url):
    for ver in vers:
        try:
            response = requests.get(url + ver)
            if response.status_code == 200:
                try:
                    # XML içeriğini parse et
                    root = ET.fromstring(response.text)
                    # version tag'ini bul
                    version = root.find('.//version')
                    if version is not None and version.text:
                        return f"{version.text}"
                except ET.ParseError:
                    # XML parse edilemezse regex ile dene
                    version_match = re.search(r'<version>(.*?)</version>', response.text)
                    if version_match:
                        return f"Joomla {version_match.group(1)}"
        except Exception as e:
            print(f"Hata oluştu: {e}")
    return None

def detect_joomla_version_from_files(url):
    for ver_file in version_files:
        try:
            response = requests.get(url + ver_file)
            if response.status_code == 200:
                content = response.text
                
                # Joomla 1.6 kontrolleri
                if (re.search(r'system\.css 20196 2011\-01\-09 02\:40\:25Z ian', content) or
                    re.search(r'MooTools\.More\=\{version\:\"1\.3\.0\.1\"', content) or
                    re.search(r'en-GB\.ini 20196 2011\-01\-09 02\:40\:25Z ian', content) or
                    re.search(r'en-GB\.ini 20990 2011\-03\-18 16\:42\:30Z infograf768', content) or
                    re.search(r'20196 2011\-01\-09 02\:40\:25Z ian', content)):
                    return "Joomla 1.6"
                
                # Joomla 1.7 kontrolleri
                elif (re.search(r'system\.css 21322 2011\-05\-11 01\:10\:29Z dextercowley', content) or
                      re.search(r'MooTools\.More\=\{version\:\"1\.3\.2\.1\"', content) or
                      re.search(r'22183 2011\-09\-30 09\:04\:32Z infograf768', content) or
                      re.search(r'21660 2011\-06\-23 13\:25\:32Z infograf768', content)):
                    return "Joomla 1.7"
                
                # Joomla 1.5 kontrolleri
                elif (re.search(r'Joomla! 1.5', content) or
                      re.search(r'MooTools\=\{version\:\'1\.12\'\}', content) or
                      re.search(r'11391 2009\-01\-04 13\:35\:50Z ian', content)):
                    return "Joomla 1.5"
                
                # Joomla 2.5 kontrolleri
                elif (re.search(r'Copyright \(C\) 2005 \- 2012 Open Source Matters', content) or
                      re.search(r'MooTools.More\=\{version\:\"1\.4\.0\.1\"', content)):
                    return "Joomla 2.5"
                
                # Meta Keywords kontrolü
                elif re.search(r'<meta name=\"Keywords\" content=\"(.*?)\">\s+<meta name', content):
                    match = re.search(r'<meta name=\"Keywords\" content=\"(.*?)\">\s+<meta name', content)
                    return f"Joomla {match.group(1)}"
                
                # Joomla 1.0 kontrolleri
                elif (re.search(r'Copyright \(C\) 2005 - 200(6|7)', content) or
                      re.search(r'47 2005\-09\-15 02\:55\:27Z rhuk', content) or
                      re.search(r'423 2005\-10\-09 18\:23\:50Z stingrey', content) or
                      re.search(r'1005 2005\-11\-13 17\:33\:59Z stingrey', content) or
                      re.search(r'1570 2005\-12\-29 05\:53\:33Z eddieajau', content) or
                      re.search(r'2368 2006\-02\-14 17\:40\:02Z stingrey', content) or
                      re.search(r'4085 2006\-06\-21 16\:03\:54Z stingrey', content) or
                      re.search(r'4756 2006\-08\-25 16\:07\:11Z stingrey', content) or
                      re.search(r'5973 2006\-12\-11 01\:26\:33Z robs', content) or
                      re.search(r'5975 2006\-12\-11 01\:26\:33Z robs', content)):
                    return "Joomla 1.0"
                
        except Exception as e:
            print(f"Hata oluştu: {e}")
    return None

def detect_joomla_version_from_readme(url):
    try:
        response = requests.get(url + "README.txt")
        if response.status_code == 200:
            match = re.search(r'package to version (.*?)\n', response.text)
            if match:
                return f"Joomla {match.group(1)}"
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

def clean_version_string(version):
    if version:
        # Sadece sayılar, harfler, nokta ve boşluk karakterlerini tut
        cleaned = re.sub(r'[^0-9a-zA-Z\.\s]', '', version)
        return cleaned
    return None
