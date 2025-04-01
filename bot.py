from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # Get token from environment variable
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Telegram bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your bot. How can I assist you?")

if __name__ == "__main__":
    WEBHOOK_URL = "https://your-koyeb-app-url/webhook"  # Replace with your Koyeb app URL
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=8000)
