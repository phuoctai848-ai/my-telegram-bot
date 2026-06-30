import os
import telebot
import json
import time
from flask import Flask, request

# CẤU HÌNH
BOT_TOKEN = "8888049748:AAH451cHABvBJaGaIYxWIF9iVDaVEnHjC0I"
# QUAN TRỌNG: Thay link dưới đây bằng link Web Service của bạn trên Render
WEBHOOK_URL = "https://my-telegram-bot-u55q.onrender.com" 

ADMIN_ID = 6280771464
CONFIG_FILE = "menu_config.json"
SETTINGS_FILE = "settings.json"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- HÀM HỖ TRỢ ---
def load_json(file_path, default):
    if not os.path.exists(file_path): return default
    try:
        with open(file_path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return default

# Tải dữ liệu cấu hình
menu_data = load_json(CONFIG_FILE, {
    "welcome": {"type": "text", "content": "👋 Chào bạn! Tôi là Trợ lý AI tự động. Hiện tại Admin đang bận, tôi đã ghi nhận tin nhắn của bạn và sẽ báo cho Admin ngay!"}
})
settings = load_json(SETTINGS_FILE, {"active": True, "cooldown": 5})
last_replied_time = {}

# --- XỬ LÝ TIN NHẮN BUSINESS ---
@bot.business_message_handler(func=lambda message: True)
def handle_business(message):
    print(f"[DEBUG] Nhận tin nhắn khách ID: {message.chat.id}")

    if not settings.get("active", True): return
    
    # Kiểm tra Cooldown (tránh spam)
    now = time.time()
    if message.chat.id in last_replied_time:
        if (now - last_replied_time[message.chat.id]) < (settings.get("cooldown", 5) * 60):
            return

    # Không tự trả lời Admin
    if message.from_user.id == ADMIN_ID: return

    last_replied_time[message.chat.id] = now
    
    try:
        # Gửi tin nhắn trả lời thay mặt tài khoản
        bot.send_message(
            chat_id=message.chat.id, 
            text=menu_data["welcome"]["content"], 
            business_connection_id=message.business_connection_id, 
            parse_mode="HTML"
        )
        print("[DEBUG] Đã gửi tin nhắn tự động.")
    except Exception as e:
        print(f"[DEBUG] Lỗi gửi tin: {e}")

# --- CẤU HÌNH WEBHOOK (TRÁNH LỖI 409) ---
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Forbidden', 403

@app.route('/')
def home():
    return "Bot is running via Webhook!"

if __name__ == '__main__':
    # Xóa webhook cũ và đặt webhook mới
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    
    # Chạy Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
