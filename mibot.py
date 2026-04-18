import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ================= CONFIGURACIÓN =================
# Asegúrate de que tus llaves estén bien escritas aquí dentro
TELEGRAM_TOKEN = '8524587945:AAF1DwrZuzBhn-EoVBn3Cs-nF66Zx-v7774'
GEMINI_API_KEY = 'AIzaSyAJ_X6H5RCY0LDmh60NycJ76AOQAihxpnY'
# =================================================

# --- PARCHE PARA RENDER (Servidor Web Falso) ---
app = Flask('')

@app.route('/')
def home():
    return "¡Chef IA en línea y cocinando!"

def run():
    # Render usa el puerto que asigne el sistema
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURACIÓN DE LA IA ---
genai.configure(api_key=GEMINI_API_KEY)

# Usamos gemini-1.5-flash porque es el más compatible actualmente
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Eres un chef experto y amable. Solo hablas en español. Tu objetivo es dar recetas detalladas y consejos de cocina."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Manejo del comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu chef personal IA. 👨‍🍳 ¿Qué receta deliciosa te gustaría preparar hoy?")

# Manejo de los mensajes de texto
@bot.message_handler(func=lambda message: True)
def chat_with_ia(message):
    try:
        print(f"Pregunta recibida: {message.text}")
        # Generar respuesta con la IA
        response = model.generate_content(message.text)
        # Responder al usuario
        bot.reply_to(message, response.text)
    except Exception as e:
        # Si falla, nos dirá el error exacto en el chat para arreglarlo
        error_detallado = str(e)
        bot.reply_to(message, f"¡Uy! Se me quemó algo. Error: {error_detallado[:100]}")
        print(f"Error: {e}")

# --- INICIO DEL BOT ---
if __name__ == "__main__":
    keep_alive() # Arranca el servidor web para Render
    print("Bot Chef encendido...")
    bot.infinity_polling()
    
