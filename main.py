import speech_recognition as sr
import pywhatkit as pwk
import datetime
import pygame
import wikipedia
# import PyDictionary (goslate dependency bein' weird)
import os, sys

def pygame_init():
	pygame.init()
	pygame.mixer.init()

class VA:
	def __init__(self, name: str, voice: str):
		self.name = name.lower()
		self.voice = voice
		self.listener = sr.Recognizer()
		self.iteration = 0
 
	def get_instruction(self):
		++self.iteration
		try:
			with sr.Microphone() as mic:
				print(f"{self.iteration}: Listening...")
				
				# input from mic
				speech = self.listener.listen(mic)
				
				# google thing tries to identify message (then making the instruction all lower-case)
				instruction = self.listener.recognize_google(speech)
				instruction = instruction.lower()

				if self.name in instruction:
					return instruction.replace(self.name, "")
				return None
		except:
			pass

	def say(self, msg: str):
		# Creating the command that edge-tts will execute
		cmd = f"edge-tts.exe --voice \"{self.voice}\" --text \"{msg}\" --write-media msg.mp3"
		os.system(cmd)

		# Playing the message
		pygame.mixer.music.load("msg.mp3")

		try:
			pygame.mixer.music.play()

			while pygame.mixer.music.get_busy():
				pass
				# pygame.time.Clock.tick(60)
			pygame.mixer.music.unload()

		except Exception as e:
			print(f"Error!: {e}")

	def execute_instruction(self, instruction: str):
		if instruction == None:
			return

		# Determine instruction to exec
		# I need a way to clean this all up...
		if "play" in instruction:
			song = instruction.replace("play", "")
			self.say("Playing " + song)
			pwk.playonyt(song)

		elif "how do you spell" in instruction:
			pass

		elif "calculate" in instruction:
			pass

		elif "what time is it" in instruction:
			time = datetime.datetime.now()
			self.say(f"Time is {time}")

		elif "what day is it" in instruction:
			day = datetime.datetime.date()
			self.say(f"Day is {day}")

		elif "what is" in instruction or "what are" in instruction:
			try:
				thing_in_question = instruction.replace("what is", "")
				answer = wikipedia.summary(thing_in_question, 1)
				self.say(answer)
			except wikipedia.exceptions.PageError:
				self.say("Sorry, I couldn't find a valid wikipedia article on that!")
			except wikipedia.exceptions.DisambiguationError:
				# Choose first option
				pass

		elif "see ya" in instruction or "goodbye" in instruction:
			self.say("Goodbye!")
			sys.quit()

		else:
			self.say("Sorry! I wasn't able to understand you!")

	def run(self):
		while True:
			instruction = self.get_instruction()
			self.execute_instruction(instruction)

name = "Steve"
voice = "en-US-SteffanNeural"
va = VA(name, voice)

if __name__ == "__main__":
	pygame_init()
	va.run()