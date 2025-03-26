import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ خطا: متغیر محیطی BOT_TOKEN تنظیم نشده است!")

async def download_music(update: Update, context: CallbackContext):
    query = " ".join(context.args)  # دریافت نام موزیک
    if not query:
        await update.message.reply_text("❌ لطفاً نام موزیک را وارد کنید.")
        return
    
    search_query = f"ytsearch:{query}"  # جستجو در یوتیوب
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=True)
        if 'entries' in info:
            info = info['entries'][0]  # اولین نتیجه
        else:
            await update.message.reply_text("❌ موزیک موردنظر پیدا نشد!")
            return
    
    filename = f"{info['title']}.mp3"

    with open(filename, "rb") as audio:
        await update.message.reply_audio(audio)
    
    os.remove(filename)  # حذف فایل بعد از ارسال

# راه‌اندازی ربات
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("music", download_music))

# اجرای polling در یک Thread جداگانه
import threading
def run_bot():
    app.run_polling()

threading.Thread(target=run_bot).start()

# ایجاد یک سرور Flask برای Koyeb
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
