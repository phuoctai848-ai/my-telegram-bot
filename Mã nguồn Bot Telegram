import telebot
from flask import Flask
import threading
import os

# --- CẤU HÌNH TOKEN ---
TOKEN = '8888049748:AAH451cHABvBJaGaIYxWIF9iVDaVEnHjC0I'
bot = telebot.TeleBot(TOKEN)

# --- PHẦN 1: TÍNH NĂNG ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Bot đang chạy 24/7 trên Render.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Bạn vừa nói: {message.text}")

# --- PHẦN 2: MÁY CHỦ WEB (GIỮ BOT THỨC) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running..."

def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- PHẦN 3: KÍCH HOẠT ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    bot.infinity_polling()
