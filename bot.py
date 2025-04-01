from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import yt_dlp
import os

TOKEN = os.getenv("BOT_TOKEN")

async def download_music(update: Update, context: CallbackContext):
    query = " ".join(context.args)  # دریافت نام موزیک
    if not query:
        await update.message.reply_text("❌ لطفاً نام موزیک را وارد کنید.")
        return
    
    search_query = f"ytsearch:{query}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        else:
            await update.message.reply_text("❌ موزیک موردنظر پیدا نشد!")
            return
    
    filename = f"{info['title']}.mp3"
    ydl.download([info['webpage_url']])

    with open(filename, "rb") as audio:
        await update.message.reply_audio(audio)
    
    os.remove(filename)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("music", download_music))

app.run_polling()
