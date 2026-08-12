#!/usr/bin/env python
"""
Тест подключения к Cloudinary
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("ПРОВЕРКА CLOUDINARY CREDENTIALS")
print("=" * 60)

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

print(f"CLOUDINARY_CLOUD_NAME: {cloud_name if cloud_name else '❌ НЕ УСТАНОВЛЕН'}")
print(f"CLOUDINARY_API_KEY: {api_key if api_key else '❌ НЕ УСТАНОВЛЕН'}")
print(f"CLOUDINARY_API_SECRET: {'✅ установлен' if api_secret else '❌ НЕ УСТАНОВЛЕН'}")
print()

if not all([cloud_name, api_key, api_secret]):
    print("❌ ОШИБКА: Не все переменные установлены!")
    exit(1)

print("Попытка подключения к Cloudinary...")
try:
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )

    # Тест подключения
    result = cloudinary.api.ping()
    print(f"✅ Подключение успешно! Status: {result.get('status')}")

except ImportError as e:
    print(f"❌ ОШИБКА: Модуль cloudinary не установлен")
    print(f"   Выполните: pip install cloudinary django-cloudinary-storage")

except Exception as e:
    print(f"❌ ОШИБКА подключения к Cloudinary:")
    print(f"   {type(e).__name__}: {e}")
    exit(1)

print()
print("=" * 60)
print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
print("=" * 60)
