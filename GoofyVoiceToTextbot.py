import os
import telebot
import speech_recognition
from pydub import AudioSegment

token = 'YOUT TOKEN HERE'

bot = telebot.TeleBot(token) 

def ogg2wav(filename):
    """
    Перевод голосового сообщения из формата ogg в wav
    """
    new_filename = filename.replace('.ogg', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename

def recognize_speech(ogg_filename):
    """
    Перевод голоса в текст + удаление использованных файлов, чтобы память не засорять бллин
    """
    wav_filename = ogg2wav(ogg_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)
    
    text = recognizer.recognize_google(wav_audio, language='ru')
    
    if os.path.exists(ogg_filename):
        os.remove(ogg_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)
    
    return text 

def download_file(bot, file_id):
    """
    Скачивание файла, который прислал пользователь
    """
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path

    filename = filename.replace('/','_') #Чтобы ошибок с косой чертой не было бллин

    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    
    return filename

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, 'Привет! Отправь мне голосовое, чтобы я его расшифровал в текст йоооу')

@bot.message_handler(content_types=['voice'])
def transcript(message):
    """
    Основная функция как раз по транскрибации голоса в текст 
    """
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    response = f"🎤 Вот расшифровка вашего голосового сообщения:\n\n{text}"
    bot.send_message(message.chat.id, response) 

bot.polling()
