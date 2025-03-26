# استفاده از ایمیج رسمی پایتون
FROM python:3.9

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه
COPY . .

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای ربات تلگرام
CMD ["python", "bot.py"]
