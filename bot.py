import telebot
from flask import Flask
import threading
import os

# --- CẤU HÌNH ---
# Hãy thay 'TOKEN_CUA_BAN' bằng Token thật của bạn
TOKEN = 'TOKEN_CUA_BAN' 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- PHẦN 1: TỰ ĐỘNG PHẢN HỒI ---
# Hàm xử lý lệnh /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào! Tôi là trợ lý ảo. Mọi tin nhắn của bạn sẽ được tôi ghi nhận và phản hồi sớm nhất.")

# Hàm tự động trả lời mọi tin nhắn (Cần tắt Privacy Mode trong BotFather)
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    # Logic trả lời: Bạn có thể thay nội dung câu trả lời tại đây
    # bot.reply_to sẽ trích dẫn tin nhắn của khách và trả lời
    bot.reply_to(message, "Cảm ơn bạn đã nhắn tin! Hiện tại tôi đang bận (không online). Tôi sẽ phản hồi lại bạn sớm nhất nhé.")

# --- PHẦN 2: WEB SERVER (ĐỂ CHẠY TRÊN RENDER) ---
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web_server():
    # Render sẽ cung cấp cổng qua biến môi trường PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- PHẦN 3: KÍCH HOẠT ---
if __name__ == "__main__":
    # Chạy Web Server trong một luồng riêng
    threading.Thread(target=run_web_server).start()
    
    # Chạy Bot Polling
    print("Bot đang chạy...")
    bot.infinity_polling()
