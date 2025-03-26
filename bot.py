import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")

# راه‌اندازی سرور فیک برای جلوگیری از توقف در Koyeb
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def download_music(update: Update, context: CallbackContext):
    query = " ".join(context.args)  # دریافت نام موزیک
    if not query:
        update.message.reply_text("❌ لطفاً نام موزیک را وارد کنید.")
        return
    
    search_query = f"ytsearch:{query}"  # جستجو در یوتیوب
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        if 'entries' in info:
            info = info['entries'][0]  # اولین نتیجه
        else:
            update.message.reply_text("❌ موزیک موردنظر پیدا نشد!")
            return
    
    filename = f"{info['title']}.mp3"
    ydl.download([info['webpage_url']])  # دانلود از لینک ویدیو

    with open(filename, "rb") as audio:
        update.message.reply_audio(audio)
    
    os.remove(filename)  # حذف فایل بعد از ارسال

# راه‌اندازی ربات
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("music", download_music))

# اجرای ربات
if __name__ == '__main__':
    import threading

    # اجرای Flask در یک ترد جداگانه
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()

    # شروع به کار ربات
    application.run_polling()
