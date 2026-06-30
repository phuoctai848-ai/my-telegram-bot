import os
import telebot
from flask import Flask, request

# --- CẤU HÌNH ---
# Sử dụng Token mới nhất của bạn
TOKEN = "8888049748:AAEamVRLb_uo9hjbiG2CidxGk2Z6-VGDuro"
# THAY BẰNG LINK RENDER CỦA BẠN (VD: https://my-bot.onrender.com)
WEBHOOK_URL = "https://my-telegram-bot-u55q.onrender.com" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- XỬ LÝ TIN NHẮN BUSINESS ---
@bot.business_message_handler(func=lambda message: True)
def handle_business(message):
    try:
        # Gửi tin nhắn trả lời tự động cho khách
        bot.send_message(
            chat_id=message.chat.id,
            text="👋 Chào bạn! Tôi là Trợ lý AI tự động. Admin hiện đang bận, tôi đã ghi nhận tin nhắn của bạn!",
            business_connection_id=message.business_connection_id
        )
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

# --- WEBHOOK ENDPOINT (Cổng nhận tin từ Telegram) ---
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

# --- KIỂM TRA BOT ---
@app.route('/')
def index():
    return "Bot đang chạy ổn định qua Webhook!"

if __name__ == '__main__':
    # THIẾT LẬP WEBHOOK (Xóa polling cũ, đặt webhook mới)
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    
    # Chạy server Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
