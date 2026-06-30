import telebot
from flask import Flask
import threading
import os

# --- CẤU HÌNH TOKEN ---
# Đây là Token Bot của bạn
TOKEN = '8888049748:AAH451cHABvBJaGaIYxWIF9iVDaVEnHjC0I'
bot = telebot.TeleBot(TOKEN)

# --- PHẦN 1: TÍNH NĂNG CỦA BOT TELEGRAM ---

# Phản hồi khi người dùng gõ /start hoặc /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Bot của bạn đã được đưa lên mây và hoạt động 24/7 thành công 🚀\nHãy nhắn một tin bất kỳ nhé!")

# Phản hồi tất cả các tin nhắn văn bản thông thường
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Nhại lại tin nhắn của người dùng
    bot.reply_to(message, f"Bạn vừa nói: {message.text}")


# --- PHẦN 2: MÁY CHỦ WEB (GIỮ BOT LUÔN THỨC TRÊN RENDER) ---
app = Flask(__name__)

# Tạo một trang web đơn giản để UptimeRobot có thể truy cập (ping) vào
@app.route('/')
def home():
    return "Bot đang hoạt động bình thường! Máy chủ web này giúp bot không bị ngủ đông."

def run_web_server():
    # Lấy cổng (PORT) mặc định từ Render, nếu không có sẽ chạy ở cổng 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# --- PHẦN 3: KÍCH HOẠT ĐỒNG THỜI CẢ 2 HỆ THỐNG ---
if __name__ == "__main__":
    print("Bắt đầu khởi động hệ thống...")
    
    # 1. Chạy Web Server trên một luồng (thread) chạy ngầm
    web_thread = threading.Thread(target=run_web_server)
    web_thread.start()
    print("Khởi động Web server hoàn tất!")
    
    # 2. Chạy Bot Telegram (infinity_polling giúp bot không bao giờ dừng)
    print("Khởi động Bot Telegram...")
    bot.infinity_polling()