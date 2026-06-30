import os
import telebot
from flask import Flask, request

# --- CẤU HÌNH ---
# DÁN TOKEN MỚI NHẤT VÀO ĐÂY
TOKEN = "8888049748:AAEamVRLb_uo9hjbiG2CidxGk2Z6-VGDuro" 
# THAY BẰNG LINK RENDER THỰC TẾ CỦA BẠN (VD: https://ten-bot-cua-ban.onrender.com)
WEBHOOK_URL = "https://my-telegram-bot-u55q.onrender.com" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- XỬ LÝ TIN NHẮN ---
@bot.business_message_handler(func=lambda message: True)
def handle_business(message):
    try:
        bot.send_message(
            chat_id=message.chat.id,
            text="👋 Chào bạn! Tôi là Trợ lý AI. Admin đang bận, tôi sẽ phản hồi sớm nhất!",
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

# --- KHỞI CHẠY ---
if __name__ == '__main__':
    # Xóa webhook cũ và đặt mới để tránh lỗi 409
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    
    # Render yêu cầu dùng port 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
