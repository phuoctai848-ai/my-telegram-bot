import os
import sys
import subprocess

# --- TỰ ĐỘNG CÀI ĐẶT THƯ VIỆN NẾU CHƯA CÓ ---
def install_requirements():
    required_packages = ['pyTelegramBotAPI', 'Flask']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Đang cài đặt thư viện: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Chạy kiểm tra trước khi import các thư viện
install_requirements()

import telebot
from flask import Flask
import threading

# --- CẤU HÌNH BOT ---
TOKEN = '8888049748:AAH451cHABvBJaGaIYxWIF9iVDaVEnHjC0I'
bot = telebot.TeleBot(TOKEN)

# --- PHẦN 1: CHỨC NĂNG CỦA BOT ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bot đã sẵn sàng! Bạn đang dùng bản gộp 1 file.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Bạn nói: {message.text}")

# --- PHẦN 2: MÁY CHỦ WEB (ĐỂ TREO TRÊN RENDER) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy 24/7."

def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- KHỞI CHẠY ---
if __name__ == "__main__":
    # Chạy Web Server ngầm
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    print("Bot đã khởi động thành công!")
    bot.infinity_polling()

# --- LƯU Ý KHI ĐƯA LÊN RENDER ---
# Dù bạn dùng 1 file .py này, Render vẫn cần bạn tạo thêm 1 file text tên là 'requirements.txt' 
# với nội dung như sau để nó biết cần cài gì:
#
# pyTelegramBotAPI
# Flask