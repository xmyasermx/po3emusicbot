import os
from flask import Flask, request
import telebot

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# دستور دریافت موزیک از یوتیوب
def download_music(message):
    query = message.text.replace("/music", "").strip()
    if not query:
        bot.reply_to(message, "❌ لطفاً نام موزیک را وارد کنید.")
        return
    
    search_query = f"ytsearch:{query}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            else:
                bot.reply_to(message, "❌ موزیک موردنظر پیدا نشد!")
                return
        
        filename = f"{info['title']}.mp3"
        ydl.download([info['webpage_url']])
        
        with open(filename, "rb") as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ خطایی رخ داد: {e}")

# ثبت دستور در بات
@bot.message_handler(commands=['music'])
def handle_music(message):
    download_music(message)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://your-koyeb-app-url/webhook")  # لینک Koyeb را جایگزین کن
    app.run(host="0.0.0.0", port=8000)
