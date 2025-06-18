'''
 Bahasa campuran 😸 || eng/id
 Fri Jun 13 13:16:19 WIB 2025
'''

try:
    import os,time,sys,uuid,random,json,requests,shutil;from datetime import datetime; from threading import Thread, Lock; from concurrent.futures import ThreadPoolExecutor; from fake_useragent import UserAgent
except ImportError:
    print("› ada modul belum yang terinstall!")

tambah = "(\033[32m+\033[0m)";errorcuy = "(\033[31m×\033[0m)";bintang = "(\033[1m\033[32m*\033[0m)";berhasil = "(\033[32m✓\033[0m)";seru = "(\033[31m!\033[0m)";tanya = "(\033[32m?\033[0m)";bahaya = "(\033[33m⚠\033[0m)";success_count = 0;error_count = 0;rate_limit_count = 0;not_found_count = 0;other_error_count = 0;lock = Lock();running = True

def tralalili_clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_device_id():
    return str(uuid.uuid4())

def get_random_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except:
        mobile_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
        ]
        return random.choice(mobile_agents)

def load_proxies():
    try:
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
            return proxies if proxies else None
    except FileNotFoundError:
        return None

def get_random_proxy(proxies):
    if proxies:
        proxy = random.choice(proxies)
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    return None

def send_request(session, username, message, user_agent, proxy=None, retry=0):
    global success_count, error_count, rate_limit_count, not_found_count, other_error_count
    headers = {
        'Host': 'ngl.link',
        'User-Agent': user_agent,
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://ngl.link',
        'Referer': f'https://ngl.link/{username}',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
        'username': username,
        'question': message,
        'deviceId': generate_device_id(),
        'gameSlug': '',
        'referrer': '',
    }

    try:
        if proxy:
            res = session.post('https://ngl.link/api/submit', headers=headers, data=data, timeout=15, proxies=proxy)
        else:
            res = session.post('https://ngl.link/api/submit', headers=headers, data=data, timeout=15)
        current_time = datetime.now().strftime("%H:%M:%S")
        status_code = res.status_code
        with lock:
            if status_code == 200:
                success_count += 1
                proxy_status = '\033[32mYes\033[0m' if proxy else '\033[31mNo\033[0m'
                print(f"[{current_time}] {berhasil} Success: {success_count} (Proxy: {proxy_status})")
            elif status_code == 429:
                rate_limit_count += 1
                print(f"[{current_time}] {bahaya} Rate Limited (Waiting 5s)")
            elif status_code == 404:
                not_found_count += 1
                print(f"[{current_time}] {errorcuy} Error 404: Not Found")
                if retry < 3:
                    time.sleep(5)
                    return send_request(session, username, message, user_agent, proxy, retry + 1)
            else:
                other_error_count += 1
                print(f"[{current_time}] {errorcuy} Error \033[2m{status_code}\033[0m")
            error_count = rate_limit_count + not_found_count + other_error_count
    except requests.exceptions.RequestException as e:
        with lock:
            error_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] {bahaya} Connection Error: \033[2m{str(e)}\033[0m")
        if retry < 3 and isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)):
            time.sleep(2)
            return send_request(session, username, message, user_agent, proxy, retry + 1)

def tralalili_ngl_spam(username, message, user_agent, total_count, thread_count=5, use_proxies=False):
    global running
    proxies = load_proxies() if use_proxies else None
    session = requests.Session()
    def worker():
        while running and (success_count + error_count) < total_count:
            current_agent = user_agent if random.random() > 0.3 else get_random_user_agent()
            proxy = get_random_proxy(proxies) if proxies and random.random() > 0.4 else None
            send_request(session, username, message, current_agent, proxy)
            time.sleep(random.uniform(0.5, 2.5))
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(worker) for _ in range(thread_count)]
        try:
            while running and (success_count + error_count) < total_count:
                time.sleep(0.5)
        except KeyboardInterrupt:
            running = False
            print(f"\n {errorcuy} Stopping all threads... Please wait.")

    session.close()
    print_results()

def tralalili_center_text(text):
    terminal_size = shutil.get_terminal_size()
    terminal_columns = terminal_size.columns
    text_length = len(text)
    start_position = (terminal_columns - text_length) // 2
    padding = " " * start_position
    print(padding + text)

def print_results():
    print();tralalili_center_text("[ RESULTS ]");print();print(f" › Successful Requests: {success_count}");print(f" › Rate Limited Errors: {rate_limit_count}");print(f" › Not Found Errors: {not_found_count}");print(f" › Other Errors: {other_error_count}");print(f" › Total Requests: {success_count + error_count}");print("\n Press Enter to return to main menu...");input()

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_config(username, message, count, user_agent, threads, use_proxies):
    config = {
        'username': username,
        'message': message,
        'count': count,
        'user_agent': user_agent,
        'threads': threads,
        'use_proxies': use_proxies
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

def show_banner():
    tralalili_clear_screen()
    print(r"""
  ____  ____    __    __      __    __    ____  __    ____
 (_  _)(  _ \  /__\  (  )    /__\  (  )  (_  _)(  )  (_  _)
   )(   )   / /(__)\  )(__  /(__)\  )(__  _)(_  )(__  _)(_
  (__) (_)\_)(__)(__)(____)(__)(__)(____)(____)(____)(____)
  """);print(f"  NGL Tralalili 💬 - Tool bot message to \033[4mngl.link\033[0m");print(f"  Multi-thread, Proxy, UserAgent, Rate-limit \033[32m•\033[0m\n")

def main_menu():
    global success_count, error_count, rate_limit_count, not_found_count, other_error_count, running
    config = load_config()
    while True:
        running = True;success_count = 0;error_count = 0;rate_limit_count = 0;not_found_count = 0;other_error_count = 0;show_banner();print(" (\033[32m1\033[0m) Mulai Serangan Spam Baru");print(" (\033[32m2\033[0m) Muat konfigurasi terakhir");print(" (\033[32m3\033[0m) Info Tools");print(" (\033[32m4\033[0m) Exit");choice = input(f"\n {bintang} Pilih opsi: ")
        if choice == '':
            main_menu()

        if choice == '1':
            custom_ua = input(f" {bintang} Custom UserAgent? (y/t, enter: random): ").lower()
            if custom_ua == 'y':
                user_agent = input(f" {bintang} Masukkan custom UserAgent: ")
            else:
                user_agent = get_random_user_agent();print(f" {bintang} Using random UserAgent: {user_agent}")
            username = input(f" {bintang} Target Username: ")
            if username == '':
               main_menu()
            message = input(f" {bintang} Pesan: ")
            if message == '':
               main_menu()
            try:
                count = int(input(f" {bintang} Total Pesan untuk dikirim: "))
                threads = int(input(f" {bintang} Threads (1-10, recommended 3-5): "))
                threads = max(1, min(threads, 10))
                use_proxies = False
                if os.path.exists('proxies.txt'):
                    use_proxies = input(f" {tambah} Use proxies from proxies.txt? (y/n): ").lower() == 'y'
                save_config(username, message, count, user_agent, threads, use_proxies)
                print(f"\n {seru} Attack started (Press Ctrl+C to stop)\n")
                tralalili_ngl_spam(username, message, user_agent, count, threads, use_proxies)
            except ValueError:
                print(f" {errorcuy} Invalid input! Please enter numbers only.")
                time.sleep(2)

        elif choice == '2':
            if config:
                print(f"\n {tambah} Last Configuration Loaded:");print(f"  › Username: {config['username']}");print(f"  › Message: {config['message']}");print(f"  › Count: {config['count']}");print(f"  › Threads: {config['threads']}");print(f"  › Use Proxies: {'Yes' if config['use_proxies'] else 'No'}");confirm = input(f"\n {tanya} Use this configuration? (y/n): ").lower()
                if confirm == 'y':
                    print(f"\n {seru} Attack started (Press Ctrl+C to stop)\n")
                    tralalili_ngl_spam(
                        config['username'],
                        config['message'],
                        config['user_agent'],
                        config['count'],
                        config['threads'],
                        config['use_proxies']
                    )
            else:
                print(f" {seru} Tidak ada konfigurasi terakhir yang ditemukan!");time.sleep(2)
        elif choice == '3':
            tralalili_clear_screen();print();tralalili_center_text("[ Tralalili Patraluli Brokoli 🥦 ]");print("\n › Code-by : anonvict 🐬");print(" › Github  : \033[4mhttps://github.com/anonvict\033[0m");print(" › Tools   : Bot Send msg to NGL (spammer ⚠)");print(" › Program : ”Python” 🐍 sssttt…");print();tralalili_center_text("[ Dan yap, gunakan dengan bijak >.< ]");print("\n\033[3m” This tools is \033[36meducation purpose only\033[0m\033[3m, Using these tools illegally can cause uncomfortable things in others :( And I am not responsible for what your fingers do! so use it wisely bro >.< ”\033[0m\n\033[36menter…\033[0m");input()
        elif choice == '4':
            sys.exit(0)
        else:
            print(f" {errorcuy} Invalid choice!");time.sleep(1)

if __name__ == "__main__":
    try:
        try:
            from fake_useragent import UserAgent
        except ImportError:
            print(f" {seru} fake-useragent tidak ada, Menginstall...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "fake-useragent"])
            from fake_useragent import UserAgent
        main_menu()
    except KeyboardInterrupt:
        pass
        sys.exit(0)
    except Exception as e:
        print(f"\n {seru} Critical error: {str(e)}")
        sys.exit(1)
