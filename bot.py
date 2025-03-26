import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def download_music(update: Update, context: CallbackContext):
    query = " ".join(context.args)  # دریافت نام موزیک از کاربر
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
        info = ydl.extract_info(search_query, download=True)
        if 'entries' in info:
            info = info['entries'][0]  # گرفتن اولین نتیجه

    filename = f"{info['title']}.mp3"
    update.message.reply_text(f"✅ دانلود شد: {filename}")
    update.message.reply_audio(audio=open(filename, "rb"))

updater = Updater("YOUR_BOT_TOKEN", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("music", download_music))

updater.start_polling()
updater.idle()
