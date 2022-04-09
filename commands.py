#!/usr/bin/python3
import ttsEngine as tts
import youtubedlpytest as ytdl
import subprocess


def ttsReply(self, reply):
    tts.say(reply)
    print("reply: ", reply)

def comSpeedTest():
        tts.say("Checking")
        bruh = subprocess.check_output("speedtest-cli --csv | awk -F',' '{print $7, \"M S Ping\", $8/1000000, \"Megabits Down\", $9/1000000, \"Megabits Up\"}'", shell=True);
        tts.say(bruh)

def inputCommand(self, utterance):
    # Example: if "this text"
    if utterance.find("whats up") != -1:
        # Example: do "this"
        tts.say("not much you")
    
    if utterance.find("run speed test") != -1:
        comSpeedTest()

    if utterance.find("download song")!= -1:
        cmd = utterance.split("download song",2)
        ytdl.ydlSong(cmd[1])











#100% usable Voice recognition without internet or network connectivity, excluding additions (207)
# print("Recognized voice: %s" % text)

# Help menu? "what can i say"
# def whatCanISay():
#     tts = gTTS(text='You can say things like:', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     tts = gTTS(text='Download Media followed by a song name', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     tts = gTTS(text='Play song-name', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("update dashboard")
#     os.system("rm ttstemp.wav")
#     tts = gTTS(text='run speed test', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     tts = gTTS(text='Download Media followed by a song name', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
# if text.find("computer what can i say") != -1:
#     x = threading.Thread(target=whatCanISay)
#     x.start()

# Voice recognition check, "do you understand (blank)"
# def understandThis(understandMe):
#     playitem1 = cmd[1].split()
#     playstring1 = ""+Playitem1[0]+""
#     player1 = vlc.MediaPlayer(playstring1)
#     player1.play()
# trigger_u_8 = text.find("do you understand")
# if trigger_u_8 != -1:
#     cmd = text.split("do you understand",2)
#     understandMe = cmd[1]
#     x = threading.Thread(target=understandThis, args=(understandMe,))
#     x.start()   

# Typical Alexa / Google Assistant / Siri / Echo features (Will add those later)

# Calendar + reminder + notes automation.

# HASSIO home automation integration.

# Bablefish Realtime Translator - With secret code to translate a localized reply like "Can I speak to your manager" in that language

# Android SDK to pull/push notifications, texts, and calls.

# AI to be able to put phone into tether mode if asked.

# FreePBX integration in place of Android SDK for calls.

# Operate 3D printer(s) via Octoprint with voice.

# Potentially including automatic searching, downloading, slicing, and printing.

# Remotely execute commands to/from networked computers.¹
# See updateDashboard and enter the matrix for functionality
# def updateDashboard():
#     tts = gTTS(text='Updating Dashboard Configuration', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     os.system("ssh pi@192.168.1.131 'bash -s' < /home/pi/voicecommands/refresh.sh")
# if text.find("update dashboard") != -1:
#     x = threading.Thread(target=updateDashboard)
#     x.start()

# SSH-Agent configured for pass-wordless communication between Linux boxes.¹
# see above

# Linux / Operating system level voice controlled commands.¹
# os.system()
# def updateDavinci():
#     tts = gTTS(text='Attempting to preform quick self restart.', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     #engine = pyttsx3.init()
#     #engine.say("Attempting to preform quick self restart.")
#     #engine.runAndWait()
#     os.system("/home/pi/restartVadStream.sh")
# if text.find("update yourself") != -1:
#     x = threading.Thread(target=updateDavinci)
#     x.start()

# def restartDavinci():
#     engine = pyttsx3.init()
#     engine.say("Attempting to preform soft reboot on myself.")
#     engine.runAndWait()
#     os.system("reboot -t 0")

# Virtual DJ:

# Add playlists, and add songs to playlists. Delete songs or playlists.

# Customize voice playlists.

# Play music by voice request.¹
# def playsong(playsongvar):
#     playitem = cmd[1].split()
#     playstring = "vlc $(find /home/pi/Music/ -type f -iname \"*"+playitem[0]+"*\" "
#     for i in range(len(playitem)-1):
#         playstring = playstring+"-a -iname \"*"+playitem[i+1]+"*\" "
#     playstring = playstring+")"
#     os.system(playstring)       
#     logging.info(playstring)

# if text.find("computer play") != -1:
#     cmd = text.split("computer play",2)
#     playsongvar = cmd[1]
#     x = threading.Thread(target=playsong, args=(playsongvar,))
#     x.start()

    #playitem = cmd[1].split()
    #playstring = "vlc $(find /home/pi/Music/ -type f -iname \"*"+playitem[0]+"*\" "
    #for i in range(len(playitem)-1):
    #    playstring = playstring+"-a -iname \"*"+playitem[i+1]+"*\" "
    #playstring = playstring+")"
    #os.system(playstring)
    
#if trigger_u_4 != -1:
    #cmd = text.split("computer play ",2,3,4,5,6)
    #os.system("vlc $(find /home/pi/Music/ -type f -iname \"*"+first_word+"*\" -a -iname \"*"+second_word+"*\" -a -iname \"*"+third_word+"*\" -a -iname \"*"+fourth_word+"*\" -a -iname \"*"+fifth_word+"*\""))
    #first_word = cmd[1]
    #### playstring = ("vlc $(find /home/pi/Music/ -type f -iname \"*"+playitem[0]+"*\" -a -iname \"*"+playitem[i+1]+"*\" ")
    #second_word = cmd[2]
    #third_word = cmd[3]
    #fourth_word = cmd[4]
    #fifth_word = cmd[5]
    #x = threading.Thread(target=playsong, args=(first_word,second_word,third_word,fourth_word,fifth_word,))
    #x.start()
    #video2mp3url = cmd[1]
    #os.system("/usr/local/bin/youtube-dl $(googler -w youtube.com --json "+video2mp3url+" | jq -r '.[].url' | head -1)")
    #thing = os.system("/usr/local/bin/youtube-dl -q $(googler -w youtube.com --json "+video2mp3url+" | jq -r '.[].url' | head -1)")
    #x = threading.Thread(target=playsong, args=(video2mp3url,))
    #x.start()
#trigger_u_3 = text.find("computer download the song")
#if trigger_u_3 != -1:
    #cmd = text.split("computer download the song",2)
    #video2mp3url = cmd[1]
    #os.system("/usr/local/bin/youtube-dl $(googler -w youtube.com --json "+video2mp3url+" | jq -r '.[].url' | head -1)")
    #thing = os.system("/usr/local/bin/youtube-dl -q $(googler -w youtube.com --json "+video2mp3url+" | jq -r '.[].url' | head -1)")
    #x = threading.Thread(target=youtubedl)
    #x.start()      
    
# If no song present, compare perhaps 66% of the words for hits and attempt to play that song, or ask if that's the right song
# https://www.datacamp.com/community/tutorials/fuzzy-string-python

# If requested song isn't available attempt to download it with prompt

# Stop / Pause music
# def stopSong():
#     os.system("killall vlc")
# if text.find("stop") != -1:
#     x = threading.Thread(target=stopSong)
#     x.start()

# Web / Online interaction:

# Web crawler / search engine results
# googler - see download songs for reference

# Discord bot integration.

# Network Tools:

# Discover SSID's

# Voice connect to open networks

# Auto connect to saved networks

# Voice password additions for networks

# Deauthentication Packet detection + announcement

# Network security audit

# Record local devices

# automated pentesting (Aircrack-ng suite):

# Don't booo me. 
# If you have WEP encryption you probably have default router login... 
# I wanna know things like this. 
# Automatically...

# #Voice automated internet speed tests¹
# def speedtest():
#     tts = gTTS(text='Checking.', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
#     bruh = subprocess.check_output("speedtest-cli --csv | awk -F',' '{print $7, \"M S Ping\", $8/1000000, \"Megabits Down\", $9/1000000, \"Megabits Up\"}'", shell=True);
#     ttsa = gTTS(text=str(bruh), lang='en')
#     ttsa.save("ttstemp1.wav")
#     os.system("mpg321 -q ttstemp1.wav")
#     os.system("rm ttstemp1.wav")
#     logging.info(bruh)
# if text.find("computer run speed test") != -1:
#     x = threading.Thread(target=speedtest)
#     x.start()

# Security:

# * Welcome Home door lock automation.

# * Intruder detection (Pixy2 / cell phone MAC address query)

# * Voice Memo Shadowplay - What did you just say? Find out! Play back the past.

# * codename CASPER

# * Emergency Responder Guide UN# Query and response

# * Voice activated emulators!           
# * Maybe brings up QR codes somewhere to scan with phones to go to web ui for controllers?

# * For fun:

# * Enter the matrix (launches cmatrix on all possible computers on network for 60 seconds)
# trigger_u_0 = text.find("enter the matrix")
#if trigger_u_0 != -1:
    #print("The Matrix is busy, please try again later...") 
    #os.system("ssh -t pi@192.168.1.138 "/home/pi/cmatrix && bash"")
#trigger_u_1 = text.find("update dashboard")

# * chopper plays get to the chopper
# def chopper():
#     os.system("play /home/pi/soundfiles/get2dachoppa.wav")
# trigger_u_2 = text.find("go to the helicopter")
# if trigger_u_2 != -1:
#     x = threading.Thread(target=chopper)
#     x.start()

# # * Self confidence booster, but it has a hard time recognizing the trigger word lol
# smile = text.find("i'm retarded")
# if smile != -1:
#     tts = gTTS(text='No you aren\'t', lang='en')
#     tts.save("ttstemp.wav")
#     os.system("mpg321 -q ttstemp.wav")
#     os.system("rm ttstemp.wav")
