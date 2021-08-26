#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot
from config_bot import token
import speech_recognition as sr
import subprocess


bot = telebot.TeleBot(token)

def text_from_audio(audio):
	try:
		r = sr.Recognizer()
		voice_file = sr.AudioFile(audio)
		with voice_file as audio_file:
			r.adjust_for_ambient_noise(audio_file)
			content = r.record(audio_file)

		text = r.recognize_google(content, language="ru-RU")
		print("Text audio: ", text)
		return text
			
	except sr.UnknownValueError as e:
		print("Google Speech Recognition could not understand audio; {0}".format(e))
		return "Не сумел распознать"
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))	
		return "Проблемы с запросом к Google"

@bot.message_handler(content_types=['voice'])
def voicer(message):
	try:
		VOICE_FILE = 'sounds/voice.ogg'
		AUDIO_FILE = 'sounds/voice.wav'
		voice_info = bot.get_file(message.voice.file_id)
		file_voice = bot.download_file(voice_info.file_path)
		with open(VOICE_FILE, 'wb') as file:
			file.write(file_voice)

		process = subprocess.run(['ffmpeg', '-i', VOICE_FILE, AUDIO_FILE, '-y'])
		
		text = text_from_audio(AUDIO_FILE)
		bot.reply_to(message, text)
	except Exception:
		print("Mistake in function voicer")			


bot.polling(none_stop=True)