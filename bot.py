import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv("7871082638:AAHRGRu1gC5ZwD6aBVEuTrMb5-MRtVomrH8")

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
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("music", download_music))

updater.start_polling()
updater.idle()
