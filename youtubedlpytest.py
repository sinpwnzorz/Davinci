#/usr/bin/python3
from googlesearch import search
import youtube_dl
import ttsEngine as tts

def ydlSong(query):
    # Sets the option parameters 
    ydl_opts = {
        'format': 'bestaudio/best',
        'cachedir': False,
        'outtmpl': '~/Music/youtube-downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Google's the query value and picks the top URL to download
    for returnedURL in search(query, tld="co.in", num=1, stop=1, pause=2):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #sttCommands.tts.say("Downloading song...")
            tts.say("Downloading song...")
            ydl.download([returnedURL])
            tts.say("Download complete.")