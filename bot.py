import telebot
import os
from flask import Flask
from threading import Thread
from groq import Groq

# 1. API Keys (Chaabiyan)
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# 2. Engines Initialize Karna
bot = telebot.TeleBot(BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Naya System Prompt (bot ka character update)
SYSTEM_PROMPT = """Tu TrendVault ka Master AI Agent hai. Tera boss Ansh hai. Tu Hinglish mein baat karega. Tera kaam digital products (e.g., Comics, Reels, Posters), SaaS, aur marketing mein Ansh ki help karna hai. Tera tone smart, helpful, aur wafadaar hona chahiye. Point par baat karna. Tera vision 'Trend Hijacking' karke content aur product factory chalana hai."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello Boss! Mera Groq AI dimaag poori tarah activate ho chuka hai. Boliye, aaj kaunsa naya trend hijack karna hai ya kaunsa product banayen?")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        # Telegram par 'typing...' dikhane ke liye
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Groq se jawab mangna
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            model="llama-3.1-8b-instant", # Duniya ka sabse fast free AI model
        )
        response = chat_completion.choices[0].message.content
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"Boss, dimaag mein thoda error aa gaya: {str(e)}\n\n(Render par Groq API key theek se dali hai na?)")

# 4. The Bypass Server (Render ko jagane ke liye)
app = Flask(__name__)
@app.route('/')
def home():
    return "TrendVault Engine is Awake!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# 5. Start Everything
if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    print("Engine with Groq Brain Started!")
    bot.infinity_polling()
