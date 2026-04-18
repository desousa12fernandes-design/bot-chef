import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ================= CONFIGURACIÓN =================
TELEGRAM_TOKEN = '8694998458:AAFUxhAUF0rttMSED__VfOvi5Zhx352MArg'
GEMINI_API_KEY = 'AIzaSyB0cj2r5be8iQYQtedXDr63tuOsDxjsUiU'
# =================================================

# --- PARCHE PARA RENDER (Servidor Web) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot de Cocina está Vivo!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu chef personal IA. 👨‍🍳 ¿Qué receta quieres preparar?")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "¡Uy! Se me quemó el arroz. ¿Repites la pregunta?")

if __name__ == "__main__":
    keep_alive() # Inicia el servidor falso
    print("Bot encendido...")
    bot.infinity_polling()
    
