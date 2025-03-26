from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl

# توکن ربات تلگرام خود را در اینجا وارد کنید
TOKEN = '7871082638:AAHRGRu1gC5ZwD6aBVEuTrMb5-MRtVomrH8'

# تابع شروع
def start(update, context):
    update.message.reply_text("سلام! برای دانلود موزیک، فقط لینک یوتیوب موزیک مورد نظر را ارسال کن.")

# تابع دانلود موزیک از یوتیوب
def download_music(update, context):
    url = update.message.text  # لینک یوتیوب
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # فقط صوت استخراج شود
        'audioquality': 1,  # کیفیت بالاتر
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # محل ذخیره فایل
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        audio_file = f"downloads/{title}.mp3"
        
        # ارسال فایل موزیک به کاربر
        update.message.reply_audio(open(audio_file, 'rb'))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # دستور start برای خوش‌آمدگویی
    dp.add_handler(CommandHandler("start", start))
    
    # دریافت لینک و دانلود موزیک
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_music))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
