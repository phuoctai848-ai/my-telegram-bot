import os
import telebot
from flask import Flask, request

# CẤU HÌNH
TOKEN = "8888049748:AAHwbBBGSpUcw0GiiPej63wbWNXMxIU3aWk"
# LƯU Ý: Thay đường dẫn bên dưới bằng link Render của BẠN (Ví dụ: https://my-bot-xyz.onrender.com)
WEBHOOK_URL = "https://my-telegram-bot-u55q.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- XỬ LÝ BUSINESS MESSAGES ---
@bot.business_message_handler(func=lambda message: True)
def handle_business(message):
    try:
        # Trả lời tin nhắn của khách
        bot.send_message(
            chat_id=message.chat.id,
            text="👋 Chào bạn! Tôi là Trợ lý AI. Admin hiện đang bận, tôi đã ghi nhận tin nhắn của bạn!",
            business_connection_id=message.business_connection_id
        )
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

# --- WEBHOOK ENDPOINT ---
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# --- THIẾT LẬP WEBHOOK ---
@app.route('/')
def index():
    return "Bot đang chạy ổn định qua Webhook!"

# Gỡ bỏ Webhook cũ và thiết lập mới mỗi khi khởi động
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == '__main__':
    # Chạy Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
