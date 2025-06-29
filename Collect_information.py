import subprocess
import sys
import importlib
import os

required_packages = [
    "requests",
    "beautifulsoup4",
    "phonenumbers",
    "python-whois",
    "dnspython",
    "rich"
]

def install_package(package):
    print(f"تثبيت الحزمة: {package} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages():
    for package in required_packages:
        try:
            module_name = package
            if package == "beautifulsoup4":
                module_name = "bs4"
            elif package == "python-whois":
                module_name = "whois"
            try:
                importlib.import_module(module_name)
            except ImportError:
                install_package(package)
        except Exception as e:
            print(f"خطأ أثناء التحقق أو التثبيت للحزمة {package}: {e}")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    console = Console()
    banner_text = Text()
    banner_text.append("أداة جمع المعلومات المتكاملة\n", style="bold magenta")
    banner_text.append("Termux & Kali Linux\n", style="bold cyan")
    banner_text.append("بواسطة PentestGPT\n", style="bold green")
    panel = Panel(banner_text, border_style="bright_blue", expand=False)
    console.print(panel)

def get_whois(domain):
    import whois
    try:
        w = whois.whois(domain)
        return w.text if hasattr(w, 'text') else str(w)
    except Exception as e:
        return f"خطأ في استعلام WHOIS: {e}"

def get_dns(domain):
    import dns.resolver
    records = {}
    try:
        for rtype in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
            answers = dns.resolver.resolve(domain, rtype, raise_on_no_answer=False)
            records[rtype] = [r.to_text() for r in answers] if answers else []
    except Exception as e:
        records['error'] = str(e)
    return records

def phone_info(number):
    import phonenumbers
    try:
        parsed = phonenumbers.parse(number)
        from phonenumbers import geocoder, carrier
        country = geocoder.description_for_number(parsed, "en")
        service = carrier.name_for_number(parsed, "en")
        valid = phonenumbers.is_valid_number(parsed)
        return {
            "number": number,
            "valid": valid,
            "country": country,
            "carrier": service
        }
    except Exception as e:
        return {"error": str(e)}

def twitter_info(username):
    import requests
    from bs4 import BeautifulSoup
    url = f"https://twitter.com/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return {"error": f"لم يتم العثور على الحساب أو مشكلة في الوصول (رمز الحالة {r.status_code})"}
        soup = BeautifulSoup(r.text, 'html.parser')
        data = {}
        title = soup.find('title')
        data['title'] = title.text if title else "غير متوفر"
        description = soup.find('meta', attrs={'name':'description'})
        data['description'] = description['content'] if description else "غير متوفر"
        return data
    except Exception as e:
        return {"error": str(e)}

def print_boxed(title, content, style="green"):
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    console = Console()
    if isinstance(content, dict):
        import json
        content_str = json.dumps(content, ensure_ascii=False, indent=2)
    else:
        content_str = str(content)
    panel = Panel(content_str, title=title, border_style=style, expand=False)
    console.print(panel)

def main():
    clear_screen()
    print_banner()

    inp = input("أدخل رقم هاتف أو رابط حساب اجتماعي (تويتر فقط حالياً) أو دومين: ").strip()

    import re

    phone_pattern = re.compile(r'^\+?\d{7,15}$')
    if phone_pattern.match(inp):
        print_boxed("معلومات رقم الهاتف", phone_info(inp), style="cyan")
        return

    twitter_match = re.match(r'https?://(www\.)?twitter\.com/([A-Za-z0-9_]+)', inp)
    if twitter_match:
        username = twitter_match.group(2)
        print_boxed(f"معلومات حساب تويتر: {username}", twitter_info(username), style="magenta")
        return

    domain = inp.lower()
    print_boxed(f"معلومات WHOIS عن: {domain}", get_whois(domain), style="yellow")
    print_boxed(f"سجلات DNS عن: {domain}", get_dns(domain), style="green")

if __name__ == "__main__":
    check_and_install_packages()
    clear_screen()
    print_banner()
    main()
                  
