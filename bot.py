import telebot
import os
from flask import Flask
from threading import Thread

# 1. Telegram Bot (Aapka Agent)
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello Boss! Main TrendVault ka Master AI Agent zinda ho chuka hoon. 100% Free Server par!")

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    bot.reply_to(message, "Boss, main abhi sun raha hoon. Apna Groq API fit karne ka order dijiye!")

# 2. The Bypass Server (Render ko jagane ke liye)
app = Flask(__name__)
@app.route('/')
def home():
    return "TrendVault Engine is Awake!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# 3. Dono ko ek sath start karna
if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    print("Engine Started! Bot is running...")
    bot.infinity_polling()
