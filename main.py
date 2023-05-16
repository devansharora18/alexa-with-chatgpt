from io import BytesIO
from gtts import gTTS
import speech_recognition as sr
import datetime
import openai
from pygame import mixer

openai.api_key = '' # insert your api key here

#messages = [
#	{"role": "system", "content": "You are a kind helpful assistant like a copilot while i am coding and your name is Gideon. Act like gideon from the flash and help me code."},
#]

messages = [
	{"role": "system", "content": "You are a kind helpful assistant like alexa and your name is alexa and you are created by Devansh Arora."}
]

def speak(audio):
	tts = gTTS(audio, lang='en', tld='co.uk', slow=False)
	fp = BytesIO()
	tts.write_to_fp(fp)
	fp.seek(0)

	mixer.init()
	mixer.music.load(fp)
	mixer.music.play()
	
	while mixer.music.get_busy():
		pass
	mixer.music.unload()
	
def listen():
	r = sr.Recognizer()
	with sr.Microphone() as mic:
		print("Listening")
		r.adjust_for_ambient_noise(mic, 0.5)
		audio = r.listen(mic)

	try:
		print("Recognizing")    
		query = r.recognize_google(audio, language='en-in')
		print(f"User: {query}")

	except Exception as e:
		print("Say again")
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

	while True:
		query = listen().lower()
		if query == "quit":
			speak('Sure, feel free to reach out to me if you need any assistance in the future. Have a good day!')
			break
		if query != "none":
			message = query
			if message:
				messages.append(
					{"role": "user", "content": message},
				)
				chat = openai.ChatCompletion.create(
					model="gpt-3.5-turbo", messages=messages
				)
			reply = chat.choices[0].message.content
			while '`' in reply:
				reply = reply.replace('`', '')
			print(f"Alexa: {reply}")
			speak(reply)
			messages.append({"role": "assistant", "content": reply})
	  
if __name__ == "__main__":
	main()