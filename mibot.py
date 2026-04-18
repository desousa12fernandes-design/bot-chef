import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ================= CONFIGURATION =================
TELEGRAM_TOKEN = '8524587945:AAF1DwrZuzBhn-EoVBn3Cs-nF66Zx-v7774'
GEMINI_API_KEY = 'AIzaSyAJ_X6H5RCY0LDmh60NycJ76AOQAihxpnY'
# =================================================

# --- RENDER PATCH ---
app = Flask('')
@app.route('/')
def home(): return "AI Chef is online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run, daemon=True).start()

# --- AI CONFIGURATION WITH AUTO-DETECTION ---
genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    # This list has the most likely names to work now
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    # First, try to list the ones that Google allows you to use
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        pass
    
    # If the list fails, return the most basic one by default
    return 'models/gemini-1.5-flash'

ACTIVE_MODEL = get_model()
model = genai.GenerativeModel(
    model_name=ACTIVE_MODEL,
    system_instruction="You are an expert chef. You only speak in Spanish."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your personal AI chef. 👨‍🍳 What are we cooking?")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # If the error persists, the bot will tell you the name of the model that failed
        bot.reply_to(message, f"Error with {ACTIVE_MODEL}: {str(e)[:50]}")

if __name__ == "__main__":
    keep_alive()
    print(f"Bot started with: {ACTIVE_MODEL}")
    bot.infinity_polling()
    
