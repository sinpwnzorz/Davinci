import os
from gtts import gTTS
import subprocess

tts = gTTS(text='Checking.', lang='en')
tts.save("ttstemp.wav")
os.system("mpg321 -q ttstemp.wav")
os.system("rm ttstemp.wav")

bruh = subprocess.check_output("speedtest-cli --csv | awk -F',' '{print $7, \"M S Ping\", $8/1000000, \"Megabits Down\", $9/1000000, \"Megabits Up\"}'", shell=True);
ttsa = gTTS(text=str(bruh), lang='en')
ttsa.save("ttstemp1.wav")
os.system("mpg321 -q ttstemp1.wav")
os.system("rm ttstemp1.wav")
