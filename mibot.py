import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ================= CONFIGURACIÓN =================
# Asegúrate de que no haya espacios extra dentro de las comillas
TELEGRAM_TOKEN = '8524587945:AAF1DwrZuzBhn-EoVBn3Cs-nF66Zx-v7774'
GEMINI_API_KEY = 'AIzaSyAJ_X6H5RCY0LDmh60NycJ76AOQAihxpnY'
# =================================================

# --- PARCHE PARA RENDER (Mantiene el bot vivo gratis) ---
app = Flask('')

@app.route('/')
def home():
    return "¡Chef IA en línea y cocinando!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURACIÓN DE LA IA ---
genai.configure(api_key=GEMINI_API_KEY)

# Usamos el nombre de modelo exacto que Google pide
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction="Eres un chef experto y amable. Solo hablas en español. Tu objetivo es dar recetas detalladas y consejos de cocina."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu chef personal IA. 👨‍🍳 ¿Qué receta deliciosa te gustaría preparar hoy?")

# Manejo de mensajes
@bot.message_handler(func=lambda message: True)
def chat_with_ia(message):
    try:
        # Generar respuesta
        response = model.generate_content(message.text)
        # Enviar respuesta al usuario
        bot.reply_to(message, response.text)
    except Exception as e:
        # Si falla, nos dirá por qué en el chat
        bot.reply_to(message, f"¡Uy! Se me quemó algo. Error: {str(e)[:100]}")
        print(f"Error: {e}")

# --- INICIO ---
if __name__ == "__main__":
    keep_alive() # Inicia el servidor falso para Render
    print("Bot Chef encendido...")
    bot.infinity_polling()
    
    
