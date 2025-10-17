import os
import telebot
import speech_recognition
from pydub import AudioSegment

token = 'YOUR TOKEN HERE'

bot = telebot.TeleBot(token)

def ogg_to_wav(filename: str) -> str | None:
    """Конвертирует OGG аудио в WAV"""
    try:
        new_filename = filename.replace('.ogg', '.wav')
        audio = AudioSegment.from_file(filename)
        audio.export(new_filename, format='wav')
        return new_filename
    except Exception as e:
        print(f"Error converting OGG to WAV: {e}")
        return None

def mp4_to_wav(filename: str) -> str | None:
    """Извлекает аудио из MP4 видео и сохраняет в WAV"""
    try:
        new_filename = filename.replace('.mp4', '.wav')
        # Pydub автоматически извлечет аудиодорожку из mp4
        audio = AudioSegment.from_file(filename, format="mp4")
        audio.export(new_filename, format='wav')
        return new_filename
    except Exception as e:
        print(f"Error extracting audio from MP4: {e}")
        return None

def recognize_speech(wav_filename: str) -> str | None:
    """Распознает речь из WAV файла."""
    recognizer = speech_recognition.Recognizer()
    try:
        with speech_recognition.WavFile(wav_filename) as source:
            wav_audio = recognizer.record(source)
        text = recognizer.recognize_google(wav_audio, language='ru-RU')
        return text
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Не удалось распознать речь."
    except speech_recognition.RequestError as e:
        print(f"Could not request results from Google service; {e}")
        return "Произошла ошибка при обращении к сервису распознавания."

def download_file(bot: telebot.TeleBot, file_id: str) -> str | None:
    """Скачивает файл и возвращает его локальное имя с правильным расширением."""
    try:
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Создаем имя файла с правильным расширением
        file_extension = os.path.splitext(file_info.file_path)[1]
        filename = f"{file_id}{file_extension}"

        with open(filename, 'wb') as f:
            f.write(downloaded_file)
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def process_media_message(message):
    """Общая функция для обработки голосовых сообщений и видео-кружочков."""
    bot.send_message(message.chat.id, "Обрабатываю ваше сообщение... ⏳")
    
    file_id = None
    media_type = None

    if message.content_type == 'voice':
        file_id = message.voice.file_id
        media_type = 'voice'
    elif message.content_type == 'video_note':
        file_id = message.video_note.file_id
        media_type = 'video_note'

    if not file_id:
        return

    original_filename = download_file(bot, file_id)
    if not original_filename:
        bot.send_message(message.chat.id, "Не удалось скачать файл.")
        return

    wav_filename = None
    if media_type == 'voice':
        wav_filename = ogg_to_wav(original_filename)
    elif media_type == 'video_note':
        wav_filename = mp4_to_wav(original_filename)

    if not wav_filename:
        bot.send_message(message.chat.id, "Не удалось обработать медиафайл.")
        os.remove(original_filename) # Очищаем скачанный файл
        return
        
    text = recognize_speech(wav_filename)
    
    # Очистка временных файлов
    if os.path.exists(original_filename):
        os.remove(original_filename)
    if os.path.exists(wav_filename):
        os.remove(wav_filename)
        
    if text:
        response = f"🎤 Расшифровка:\n\n{text}"
        bot.send_message(message.chat.id, response)
    else:
        # Этого не должно случиться, так как recognize_speech возвращает текст ошибки,
        # но на всякий случай
        bot.send_message(message.chat.id, "Произошла неизвестная ошибка.")

@bot.message_handler(commands=['start'])
def say_hi(message):
    # Обновляем приветствие, чтобы оно включало видео-кружочки
    bot.send_message(message.chat.id, 'Привет! Отправь мне голосовое сообщение или видео-кружочек, и я превращу его в текст.')

@bot.message_handler(content_types=['voice', 'video_note'])
def transcript_media(message):
    """Единый обработчик для всех поддерживаемых медиа-типов."""
    process_media_message(message)

print("Bot is running...")
bot.polling(non_stop=True)