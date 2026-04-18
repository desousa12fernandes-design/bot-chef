import telebot
import google.generativeai as genai
import os

# ================= CONFIGURACIÓN =================
# 1. Pega aquí el Token de Telegram que te dio BotFather
TELEGRAM_TOKEN = '8694998458:AAHHYzX5qz60EVWKhcnP7Q5Dvp70i4MJx80'

# 2. Pega aquí la API Key que sacaste de Google AI Studio
GEMINI_API_KEY = 'AIzaSyB0cj2r5be8iQYQtedXDr63tuOsDxjsUiU'
# =================================================

# Configuración de la IA
genai.configure(api_key=GEMINI_API_KEY)

# Buscador automático de modelo disponible
def buscar_modelo():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        return 'gemini-pro'
    return 'gemini-pro'

MODELO_ACTIVO = buscar_modelo()

# Configuramos la personalidad del Chef
model = genai.GenerativeModel(
    model_name=MODELO_ACTIVO,
    system_instruction="Eres un chef experto y amable. Solo hablas en español. Tu objetivo es dar recetas paso a paso. Siempre respondes en español."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Comando de inicio
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu chef personal IA. 👨‍🍳 ¿Qué receta deliciosa te gustaría preparar hoy?")

# Manejo de mensajes de texto
@bot.message_handler(func=lambda message: True)
def chat_with_ia(message):
    try:
        print(f"Usuario pregunta por: {message.text}")
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "¡Uy! Se me quemó algo en la cocina. ¿Podrías repetir la pregunta?")
        print(f"Error: {e}")

# Esto es para que Render sepa que el bot debe quedarse encendido
if __name__ == "__main__":
    print(f"Bot encendido con el modelo: {MODELO_ACTIVO}")
    bot.infinity_polling()
  
