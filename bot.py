import telebot
from telebot import types
import json
import os
import time
from flask import Flask, request

#BOT_TOKEN = "8888049748:AAFE1Nd2vAYBgOb82OEbar8QsAckMrt7Obk"
ADMIN_ID = 6280771464
CONFIG_FILE = "menu_config.json"
SETTINGS_FILE = "settings.json"
# Thay URL này bằng link Render của bạn (VD: https://ten-bot.onrender.com)
WEBHOOK_URL = "https://my-telegram-bot-u55q.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

#def load_json(file_path, default):
    if not os.path.exists(file_path): return default
    with open(file_path, 'r', encoding='utf-8') as f: return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

menu_data = load_json(CONFIG_FILE, {
    "welcome": {"type": "text", "content": "👋 Chào bạn! Tôi là Trợ lý AI tự động của tài khoản này.\n\nHiện tại Admin đang tạm thời không online trực tiếp. Để lại [ số điện thoại ] tại đây, tôi sẽ thông báo trực tiếp cho Admin và trả lời bạn ngay khi trực tuyến trở lại!"}
})
settings = load_json(SETTINGS_FILE, {"active": True, "cooldown": 5})

last_replied_time = {}

#@bot.business_message_handler(func=lambda message: True)
def handle_business(message):
    print(f"[DEBUG] Nhận tin nhắn từ khách ID: {message.chat.id}")

    if not settings["active"]: return
    
    # Kiểm tra Cooldown
    now = time.time()
    if message.chat.id in last_replied_time:
        if (now - last_replied_time[message.chat.id]) < (settings["cooldown"] * 60):
            return

    # Không tự trả lời Admin
    if message.from_user.id == ADMIN_ID: return

    # Gửi lời chào
    last_replied_time[message.chat.id] = now
    welcome = menu_data["welcome"]

    try:
        # Quan trọng: Phải truyền business_connection_id để trả lời thay mặt tài khoản
        bot.send_message(
            chat_id=message.chat.id, 
            text=welcome["content"], 
            business_connection_id=message.business_connection_id, 
            parse_mode="HTML"
        )
        print("[DEBUG] Đã gửi lời chào thành công.")
    except Exception as e:
        print(f"[DEBUG] Lỗi: {e}")

#@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def home():
    return "Bot is running via Webhook!"

if __name__ == '__main__':
    # Xóa webhook cũ và đặt mới
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
