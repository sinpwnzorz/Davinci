#!/usr/bin/python3
import pyttsx3

def say(say):
    engine = pyttsx3.init()
    engine.say(say)
    engine.runAndWait()













































# Uncomment to enable gTTS
# class ttsEngine:
#     def say(self, say):
#         tts = gTTS(text='You can say things like:', lang='en')
#         tts.save("ttstemp.wav")
#         os.system("mpg321 -q ttstemp.wav")
#         os.system("rm ttstemp.wav")

# This would not go in ttsEngine:
# class shortConvo:
#     def maintainConvo(self, callsign, memory, endofmsg):
#         self.c = callsign
#         self.m = memory
#         self.e = endofmsg
