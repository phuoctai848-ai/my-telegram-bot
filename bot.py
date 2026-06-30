import os
import telebot
from flask import Flask
from telebot import types

# 1. Cấu hình Bot
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE' # Thay bằng Token của bạn từ BotFather
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 2. Xử lý lệnh /start với Menu nút bấm
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    # Tạo các nút bấm
    btn1 = types.InlineKeyboardButton("Xem Bảng Giá", callback_data='price')
    btn2 = types.InlineKeyboardButton("Liên Hệ Admin", callback_data='contact')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "Chào bạn! Tôi là trợ lý ảo. Bạn cần hỗ trợ gì ạ?", reply_markup=markup)

# 3. Xử lý khi khách bấm nút
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'price':
        bot.answer_callback_query(call.id, "Đang tải bảng giá...")
        bot.send_message(call.message.chat.id, "Bảng giá của chúng tôi:\n- Sản phẩm A: 500k\n- Sản phẩm B: 800k")
    elif call.data == 'contact':
        bot.send_message(call.message.chat.id, "Bạn có thể liên hệ Admin qua: @username_cua_ban")

# 4. Phần Flask để Render giữ Bot "sống"
@app.route('/')
def home():
    return "Bot is running!"

# 5. Khởi chạy Bot
if __name__ == "__main__":
    # Để bot chạy trên Render (Web Service), cần chạy Flask và Polling
    import threading
    
    # Chạy polling của bot trong một thread riêng
    def run_bot():
        bot.infinity_polling()
        
    threading.Thread(target=run_bot).start()
    
    # Chạy flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
