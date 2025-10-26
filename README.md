# 🎤 Goofy ahh Voice2Text Telegram Bot

Это мой самый первый телеграмм бот, сделанный на языке Python. Очень надеюсь, что многим он поможет понять, как работают Telegram-боты для распознавания речи. Также, с недавнего времени благодаря пользователю **combx**, у бота появилась возможность расшифровывать видео-кружочки! :)

## Объяснение кода
Если вдруг вам стало интересно как всё работает, но вы чего-то не понимаете, то я опубликовала статью на Хабр, где объясняются все функции в коде и что вообще использовалось при создании.
Прочитать можно по [этой ссылке](https://habr.com/ru/articles/938492/)

## Перед началом работы (важно!)

Для работы библиотеки pydub ОБЯЗАТЕЛЬНО нужен скачанный ffmpeg. Без него чуть ли не все функции pydub не будут работать (увы). Поэтому, пожалуйста, убедитесь, что он установлен в вашей системе.

> **Ubuntu/Debian:** sudo apt-get install ffmpeg
> 
> **macOS (через Homebrew):** brew install ffmpeg
> 
> **Windows:** Скачайте с [официального сайта](https://ffmpeg.org/download.html) и добавьте путь к ffmpeg.exe в системную переменную PATH.


## Демонстрация работы

![Гуфи ах бот Демонстрация](https://github.com/user-attachments/assets/509dde2f-15cf-46f2-bb73-66f628af957a)

## 🔧 Локальный запуск (без Docker)

```bash
# Установка
git clone https://github.com/ваш-логин/Goofy-ahh-Voice-To-Text-bot.git
cd Goofy-ahh-Voice-To-Text-bot
pip install -r requirements.txt

# Не забудьте сделать файл окружения .env, из которого бот будет брать токен :)

# Запуск
python GoofyVoiceToTextbot.py
```

## 🐳 Запуск через Docker (ооо китовое..)

### 1. Собрать Docker образ
```bash
docker build -t my-telegram-bot .
```

### 2. Запустить контейнер
```bash
docker run -d --name telegram-bot -e BOT_TOKEN="YOUR_BOT_TOKEN_HERE" my-telegram-bot
```

## Стек технологий, использованный в работе
- Python 3.9+
- pyTelegramBotAPI
- SpeechRecognition
- pydub

## Как помочь
Открыта для pull requests! Нашли ошибку? Создайте issue. Буду только рада как-то доработать и улучшить проект :)

## Лицензия
MIT © [goldencaregiver] - [Мой Telegram](https://t.me/vikakotleta)
