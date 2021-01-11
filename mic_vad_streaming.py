import time, logging
from datetime import datetime
from gtts import gTTS
from fuzzywuzzy import fuzz
import threading, collections, queue, os, os.path
import deepspeech
import numpy as np
import pyaudio
import pyttsx3
import wave
import vlc
#import winsound
import webrtcvad
import subprocess
from halo import Halo
from scipy import signal

logging.basicConfig(level=20)

class Audio(object):
    """Streams raw audio from microphone. Data is received in a separate thread, and stored in a buffer, to be read from."""

    FORMAT = pyaudio.paInt16
    # Network/VAD rate-space
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 50

    def __init__(self, callback=None, device=None, input_rate=RATE_PROCESS, file=None):
        def proxy_callback(in_data, frame_count, time_info, status):
            #pylint: disable=unused-argument
            if self.chunk is not None:
                in_data = self.wf.readframes(self.chunk)
            callback(in_data)
            return (None, pyaudio.paContinue)
        if callback is None: callback = lambda in_data: self.buffer_queue.put(in_data)
        self.buffer_queue = queue.Queue()
        self.device = device
        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        self.pa = pyaudio.PyAudio()

        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }

        self.chunk = None
        # if not default device
        if self.device:
            kwargs['input_device_index'] = self.device
        elif file is not None:
            self.chunk = 320
            self.wf = wave.open(file, 'rb')

        self.stream = self.pa.open(**kwargs)
        self.stream.start_stream()

    def resample(self, data, input_rate):
        """
        Microphone may not support our native processing sampling rate, so
        resample from input_rate to RATE_PROCESS here for webrtcvad and
        deepspeech
        Args:
            data (binary): Input audio stream
            input_rate (int): Input audio rate to resample from
        """
        data16 = np.fromstring(string=data, dtype=np.int16)
        resample_size = int(len(data16) / self.input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = np.array(resample, dtype=np.int16)
        return resample16.tostring()

    def read_resampled(self):
        """Return a block of audio data resampled to 16000hz, blocking if necessary."""
        return self.resample(data=self.buffer_queue.get(),
                             input_rate=self.input_rate)

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        return self.buffer_queue.get()

    def destroy(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)

    def write_wav(self, filename, data):
        logging.info("write wav %s", filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        # wf.setsampwidth(self.pa.get_sample_size(FORMAT))
        assert self.FORMAT == pyaudio.paInt16
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()


class VADAudio(Audio):
    """Filter & segment audio with voice activity detection."""

    def __init__(self, aggressiveness=3, device=None, input_rate=None, file=None):
        super().__init__(device=device, input_rate=input_rate, file=file)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        if self.input_rate == self.RATE_PROCESS:
            while True:
                yield self.read()
        else:
            while True:
                yield self.read_resampled()

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames comprising each utterence, separated by yielding a single None.
            Determines voice activity by ratio of frames in padding_ms. Uses a buffer to include padding_ms prior to being triggered.
            Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                      |---utterence---|        |---utterence---|
        """
        if frames is None: frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False

        for frame in frames:
            if len(frame) < 640:
                return

            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > ratio * ring_buffer.maxlen:
                    triggered = True
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    triggered = False
                    yield None
                    ring_buffer.clear()

def main(ARGS):
    # Load DeepSpeech model
    if os.path.isdir(ARGS.model):
        model_dir = ARGS.model
        ARGS.model = os.path.join(model_dir, 'output_graph.pb')
        ARGS.scorer = os.path.join(model_dir, ARGS.scorer)

    print('Initializing model...')
    logging.info("ARGS.model: %s", ARGS.model)
    model = deepspeech.Model(ARGS.model)
    if ARGS.scorer:
        logging.info("ARGS.scorer: %s", ARGS.scorer)
        model.enableExternalScorer(ARGS.scorer)

    # Start audio with VAD
    vad_audio = VADAudio(aggressiveness=ARGS.vad_aggressiveness,
                         device=ARGS.device,
                         input_rate=ARGS.rate,
                         file=ARGS.file)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Stream from microphone to DeepSpeech using VAD
    spinner = None
    if not ARGS.nospinner:
        spinner = Halo(spinner='line')
    stream_context = model.createStream()
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            if spinner: spinner.start()
            logging.debug("streaming frame")
            stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
            if ARGS.savewav: wav_data.extend(frame)
        else:
            if spinner: spinner.stop()
            logging.debug("end utterence")
            if ARGS.savewav:
                vad_audio.write_wav(os.path.join(ARGS.savewav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav")), wav_data)
                wav_data = bytearray()
            text = stream_context.finishStream()

            #########################################
            #|  #################################  |#
            #|  | Start of "Top level features" |  |#
            #|  #################################  |#
            #########################################

            #100% usable Voice recognition without internet or network connectivity, excluding additions (207)
            print("Recognized voice: %s" % text)
            
            # Help menu? "what can i say"
            def whatCanISay():
                tts = gTTS(text='You can say things like:', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
                tts = gTTS(text='Download Media followed by a song name', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
                tts = gTTS(text='Play song-name', lang='en')
                tts.save("ttstemp.wav")
                os.system("update dashboard")
                os.system("rm ttstemp.wav")
                tts = gTTS(text='run speed test', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
                tts = gTTS(text='Download Media followed by a song name', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
            if text.find("computer what can i say") != -1:
                x = threading.Thread(target=whatCanISay)
                x.start()

            # Voice recognition check, "do you understand (blank)"
            def understandThis(understandMe):
                playitem1 = cmd[1].split()
                playstring1 = ""+Playitem1[0]+""
                player1 = vlc.MediaPlayer(playstring1)
                player1.play()
            trigger_u_8 = text.find("do you understand")
            if trigger_u_8 != -1:
                cmd = text.split("do you understand",2)
                understandMe = cmd[1]
                x = threading.Thread(target=understandThis, args=(understandMe,))
                x.start()   

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
            def updateDashboard():
                tts = gTTS(text='Updating Dashboard Configuration', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 ttstemp.wav")
                os.system("rm ttstemp.wav")
                os.system("ssh pi@192.168.1.131 'bash -s' < /home/pi/voicecommands/refresh.sh")
            if text.find("update dashboard") != -1:
                x = threading.Thread(target=updateDashboard)
                x.start()

            # SSH-Agent configured for pass-wordless communication between Linux boxes.¹
            # see above

            # Linux / Operating system level voice controlled commands.¹
            # os.system()
            def updateDavinci():
                tts = gTTS(text='Attempting to preform quick self restart.', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 ttstemp.wav")
                os.system("rm ttstemp.wav")
                #engine = pyttsx3.init()
                #engine.say("Attempting to preform quick self restart.")
                #engine.runAndWait()
                os.system("/home/pi/restartVadStream.sh")
            if text.find("update yourself") != -1:
                x = threading.Thread(target=updateDavinci)
                x.start()

            def restartDavinci():
                engine = pyttsx3.init()
                engine.say("Attempting to preform soft reboot on myself.")
                engine.runAndWait()
                os.system("reboot -t 0")

            # Virtual DJ:

            # Add playlists, and add songs to playlists. Delete songs or playlists.

            # Customize voice playlists.

            # Download music by voice request using youtube-dl.¹
            def youtubedl(target_url):
                logging.info("Downloading song...")
                engine = pyttsx3.init()
                engine.say("Downloading "+target_url)
                engine.runAndWait()
                os.system("/usr/local/bin/youtube-dl -q -x -o \"/home/pi/Music/%(title)s.%(ext)s\" $(googler -w youtube.com --json "+target_url+" | jq -r '.[].url' | head -1)")
                logging.info("Download complete.")
                engine = pyttsx3.init()
                engine.say("Download complete.")
                engine.runAndWait()
                path = '/home/pi/Music/'
                for filename in os.listdir(path):
                    #print(filename)
                    os.rename(os.path.join(path,filename),os.path.join(path, filename.replace(' ', '_').lower()))
                #logging.info("Converting song...")
                #engine = pyttsx3.init()
                #engine.say("Converting "+target_url+" to MP3 format")
                #engine.runAndWait()
                #os.system("find /home/pi/Music/ -type f -name \"* *\" | while read file; do mv \"$file\" ${file// /_}; done")
                #subprocess.run(['sh', '/home/pi/Music/mp3con.sh'])
                #engine = pyttsx3.init()
                #engine.say("Conversion complete and file name modified to read properly.")
                #engine.runAndWait()
                #logging.info("Conversion complete.")
            trigger_u_3 = text.find("computer download media")
            if trigger_u_3 != -1:
                cmd = text.split("computer download media",2)
                video2mp3url = cmd[1]
                x = threading.Thread(target=youtubedl, args=(video2mp3url,))
                x.start()

            # Play music by voice request.¹
            def playsong(playsongvar):
                playitem = cmd[1].split()
                playstring = "vlc $(find /home/pi/Music/ -type f -iname \"*"+playitem[0]+"*\" "
                for i in range(len(playitem)-1):
                    playstring = playstring+"-a -iname \"*"+playitem[i+1]+"*\" "
                playstring = playstring+")"
                os.system(playstring)       
                logging.info(playstring)
            if text.find("computer play") != -1:
                cmd = text.split("computer play",2)
                playsongvar = cmd[1]
                x = threading.Thread(target=playsong, args=(playsongvar,))
                x.start()
            if text.find("computer played") != -1:
                cmd = text.split("computer played",2)
                playsongvar = cmd[1]
                x = threading.Thread(target=playsong, args=(playsongvar,))
                x.start()
            if text.find("computer place") != -1:
                cmd = text.split("computer place",2)
                playsongvar = cmd[1]
                x = threading.Thread(target=playsong, args=(playsongvar,))
                x.start()
            if text.find("computer layed") != -1:
                cmd = text.split("computer layed",2)
                playsongvar = cmd[1]
                x = threading.Thread(target=playsong, args=(playsongvar,))
                x.start()
            if text.find("computer lay") != -1:
                cmd = text.split("computer lay",2)
                playsongvar = cmd[1]
                x = threading.Thread(target=playsong, args=(playsongvar,))
                x.start()   
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
            def stopSong():
                os.system("killall vlc")
            if text.find("stop") != -1:
                x = threading.Thread(target=stopSong)
                x.start()

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
            
            # Voice automated internet speed tests¹
            def speedtest():
                tts = gTTS(text='Checking.', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
                bruh = subprocess.check_output("speedtest-cli --csv | awk -F',' '{print $7, \"M S Ping\", $8/1000000, \"Megabits Down\", $9/1000000, \"Megabits Up\"}'", shell=True);
                ttsa = gTTS(text=str(bruh), lang='en')
                ttsa.save("ttstemp1.wav")
                os.system("mpg321 -q ttstemp1.wav")
                os.system("rm ttstemp1.wav")
                logging.info(bruh)
            if text.find("computer run speed test") != -1:
                x = threading.Thread(target=speedtest)
                x.start()

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
            trigger_u_0 = text.find("enter the matrix")
            #if trigger_u_0 != -1:
                #print("The Matrix is busy, please try again later...") 
                #os.system("ssh -t pi@192.168.1.138 "/home/pi/cmatrix && bash"")
            #trigger_u_1 = text.find("update dashboard")
            
            # * chopper plays get to the chopper
            def chopper():
                os.system("play /home/pi/soundfiles/get2dachoppa.wav")
            trigger_u_2 = text.find("go to the helicopter")
            if trigger_u_2 != -1:
                x = threading.Thread(target=chopper)
                x.start()

            # * Self confidence booster, but it has a hard time recognizing the trigger word lol
            smile = text.find("i'm retarded")
            if smile != -1:
                tts = gTTS(text='No you aren\'t', lang='en')
                tts.save("ttstemp.wav")
                os.system("mpg321 -q ttstemp.wav")
                os.system("rm ttstemp.wav")
            
            stream_context = model.createStream()

if __name__ == '__main__':
    DEFAULT_SAMPLE_RATE = 16000

    import argparse
    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
    parser.add_argument('--nospinner', action='store_true',
                        help="Disable spinner")
    parser.add_argument('-w', '--savewav',
                        help="Save .wav files of utterences to given directory")
    parser.add_argument('-f', '--file',
                        help="Read from .wav file instead of microphone")

    parser.add_argument('-m', '--model', required=True,
                        help="Path to the model (protocol buffer binary file, or entire directory containing all standard-named files for model)")
    parser.add_argument('-s', '--scorer',
                        help="Path to the external scorer file.")
    parser.add_argument('-d', '--device', type=int, default=None,
                        help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
    parser.add_argument('-r', '--rate', type=int, default=DEFAULT_SAMPLE_RATE,
                        help=f"Input device sample rate. Default: {DEFAULT_SAMPLE_RATE}. Your device may require 44100.")

    ARGS = parser.parse_args()
    if ARGS.savewav: os.makedirs(ARGS.savewav, exist_ok=True)
    main(ARGS)
