import os
from gtts import gTTS
import time
import speech_recognition as sr
import datetime
import openai
from playsound import playsound as play

openai.api_key = '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'

messages = [
	{"role": "system", "content": "You are a kind helpful assistant."},
]

def speak(audio):
	tts = gTTS(audio)
	tts.save("temp.mp3")
	time.sleep(2)
	play("temp.mp3")
	os.remove("temp.mp3")

def listen():
	r = sr.Recognizer()
	with sr.Microphone() as mic:
		print("Listening...")
		#r.adjust_for_ambient_noise(mic, duration=0.5
		r.pause_threshold = 1
		audio = r.listen(mic)

	try:
		print("Recognizing...")    
		query = r.recognize_google(audio, language='en-in')
		print(f"User: {query}")

	except Exception as e:
		print("Say that again please...")  
		return "None"
	return query

def greet():
	hour = int(datetime.datetime.now().hour)
	
	if hour >= 0 and hour < 12:
		speak("Good Morning!")
	
	elif hour >= 12 and hour < 18:
		speak("Good Afternoon!")
		
	else:
		speak("Good Evening!")
				
def main():
	  greet()
	  
if __name__ == "__main__":
	main()
	  
	while True:
		query = listen()
		if query != "None":
			message = query
			if message:
				messages.append(
					{"role": "user", "content": message},
				)
				chat = openai.ChatCompletion.create(
					model="gpt-3.5-turbo", messages=messages
				)
			reply = chat.choices[0].message.content
			print(f"ChatGPT: {reply}")
			speak(reply)
			messages.append({"role": "assistant", "content": reply})