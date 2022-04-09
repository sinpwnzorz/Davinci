#!/usr/bin/python3
import commands as stt
import mic_vad_streaming

# Simulated audio data stream, currently text input
# heardSpeech = input("\"Say\" something...\n")

heardSpeech = mic_vad_streaming.main(textVar)

#heardSpeech = ds.main(text=())

saidCommand = stt()

authList = open("authList.txt").read().splitlines()
authString = ' '.join([str(item) for item in authList])

def activatePrefix(suffix):
    saidCommand.inputCommand(suffix)

if heardSpeech.find(authString) != -1:
    utterance = heardSpeech.split(authString,2)
    suffix = utterance[1] # above list is start at 0 index
    activatePrefix(suffix)
else:
    print("No activation word present")
