import telebot
import os
import random
import urllib.parse
from flask import Flask
from threading import Thread
from groq import Groq
from supabase import create_client, Client

# 1. API Keys & Connections (Chaabiyan)
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# 2. Engines Initialize Karna
bot = telebot.TeleBot(BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Naya System Prompt (bot ka character update)
SYSTEM_PROMPT = """Tu TrendVault ka Master AI Agent hai. Tera boss Ansh hai. Tu Hinglish mein baat karega. Tera kaam digital products (e.g., Comics, Reels, Posters), SaaS, aur marketing mein Ansh ki help karna hai. Tera tone smart, helpful, aur wafadaar hona chahiye. Point par baat karna. Tera vision 'Trend Hijacking' karke content aur product factory chalana hai."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello Boss! Mera Groq AI dimaag poori tarah activate ho chuka hai. Boliye, aaj kaunsa naya trend hijack karna hai ya kaunsa product banayen?")

# ========================================================
# 🛒 NAYA DUKAN MODULE: GITHUB SE PEHLE TELEGRAM SE TEST
# ========================================================
@bot.message_handler(commands=['makeproduct'])
def make_new_product(message):
    bot.reply_to(message, "⏳ Boss, Manager dukan ke liye live trend dhoondh raha hai (Groq API)...")

    try:
        # 1. Groq se Idea aur Content Generate karwana
        groq_prompt = "Act as a digital product creator. Give me 1 trending digital product idea. Reply STRICTLY in this exact format without any extra text: Title | Catchy Sales Description (2 sentences max) | Price (a random number between 15.99 and 65.99)"
        
        completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": groq_prompt}],
            model="llama-3.1-8b-instant",
        )
        # Groq ke answer ko 3 hisson mein todna
        groq_response = completion.choices[0].message.content.split('|')
        
        product_title = groq_response[0].strip()
        product_desc = groq_response[1].strip()
        price_str = groq_response[2].strip().replace('$', '')
        product_price = float(price_str)

        bot.reply_to(message, f"🧠 Trend pakad liya!\nTitle: {product_title}\n🎨 Ab design bana raha hoon...")

        # 2. Image Generation (Pollinations - No API Key Needed)
        safe_prompt = urllib.parse.quote(f"High quality cover art for {product_title}, featuring yah wala character, dynamic lighting, 4k resolution, trending on artstation")
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true"

        # 3. Upload to Supabase (Dukan Par Live)
        # Zaruri Note: Supabase mein 'products' naam ka table hona chahiye!
        data, count = supabase.table('products').insert({
            "title": product_title,
            "description": product_desc,
            "price": product_price,
            "image_url": image_url
        }).execute()

        # 4. Boss ko report
        bot.reply_to(message, 
            f"✅ **BOSS, NAYA MAAL LIVE HO GAYA!** 🎉\n\n"
            f"📦 **Name:** {product_title}\n"
            f"💰 **Price:** ${product_price}\n"
            f"📝 **Desc:** {product_desc}\n\n"
            f"🔗 **Image Check Karein:** {image_url}\n\n"
            f"🛒 Apni Vercel website refresh kariye!"
        )

    except Exception as e:
        bot.reply_to(message, f"❌ Boss, Product banane mein error aa gaya: {str(e)}\n\n(Check kariye 'products' table Supabase mein hai ya nahi)")


# ========================================================
# 🤖 PURANA AI CHAT MODULE (SABSE NICHE RAKHNA ZARURI HAI)
# ========================================================
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
            model="llama-3.1-8b-instant", 
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
    print("Engine with Groq Brain & Supabase Started!")
    bot.infinity_polling()
