import subprocess
import sys
import importlib

required_packages = [
    "requests",
    "beautifulsoup4",
    "phonenumbers",
    "python-whois",
    "dnspython"
]

def install_package(package):
    print(f"تثبيت الحزمة: {package} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages():
    for package in required_packages:
        try:
            # اسم الحزمة في pip قد يختلف عن اسم الموديول في import
            # لذلك نستخدم mapping بسيط:
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

def main():
    print("أداة جمع المعلومات المتكاملة")
    inp = input("أدخل رقم هاتف أو رابط حساب اجتماعي (تويتر فقط حالياً) أو دومين: ").strip()

    import re
    import json

    phone_pattern = re.compile(r'^\+?\d{7,15}$')
    if phone_pattern.match(inp):
        print("جمع معلومات عن رقم الهاتف...")
        info = phone_info(inp)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    twitter_match = re.match(r'https?://(www\.)?twitter\.com/([A-Za-z0-9_]+)', inp)
    if twitter_match:
        username = twitter_match.group(2)
        print(f"جمع معلومات عن حساب تويتر: {username}")
        info = twitter_info(username)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    domain = inp.lower()
    print(f"جمع معلومات WHOIS عن: {domain}")
    whois_data = get_whois(domain)
    print(whois_data)

    print(f"\nجمع سجلات DNS عن: {domain}")
    dns_data = get_dns(domain)
    print(json.dumps(dns_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    check_and_install_packages()
    main()
