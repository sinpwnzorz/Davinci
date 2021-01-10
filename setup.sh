pip install --upgrade pip #makes sure we're ready for pip3 I think

#install DeepSpeech 0.9.3 (Or most recent) https://github.com/touchgadget/DeepSpeech
apt install git python3-pip python3-scipy python3-numpy python3-pyaudio libatlas3-base -y
pip3 install deepspeech --upgrade
mkdir ~/dspeech
cd ~/dspeech
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz
tar xvf audio-0.9.3.tar.gz
source ~/.profile

deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio audio/2830-3980-0043.wav
deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio audio/4507-16021-0012.wav
deepspeech --model deepspeech-0.9.3-models.tflite --scorer deepspeech-0.9.3-models.scorer --audio audio/8455-210777-0068.wav

git clone https://github.com/mozilla/DeepSpeech-examples

#If microphone won't work
#Edit these values
#sudo nano /usr/share/alsa/alsa.conf
#defaults.ctl.card 3
#defaults.pcm.card 3

#install googler
cd Downloads
wget -c https://github.com/jarun/googler/archive/v4.3.1.tar.gz #downloading  "googler"
tar -xvf v4.3.1.tar.gz #un-tarballing
cd googler-4.3.1
make install #i still dont know what this does
cd auto-completion/bash/
cp googler-completion.bash /etc/bash_completion.d/
cd
#remove wget file?

#pip3 installs
#text to speech clients: https://pythonprogramminglanguage.com/text-to-speech/
#https://github.com/wiseman/py-webrtcvad
#https://pypi.org/project/halo/
#speedtest-cli speedtests from cli
#MAKE DAMN SURE you're on the updated one or it wont work, its really fucky
#but it's in /usr/local/bin/youtube-dl
#everything thinks it should be in /usr/bin/youtube-dl
pip3 install gTTS pyttsx3 halo webrtcvad speedtest-cli youtube-dl --upgrade

#apt installs
#install ffmpeg && lame to convert .mkv, .webm, .mp4 into .mp3 https://computingforgeeks.com/how-to-convert-mp4-to-mp3-on-linux/
#install json query for parsing youtube-dl queries
#espeak tts client
apt install ffmpeg lame jq espeak -y

#shell replace spaces https://vitux.com/how-to-replace-spaces-in-filenames-with-underscores-on-the-linux-shell/

#create and chmod run script to executable
cd
touch runDeepSpeech.sh
cat > runDeepSpeech.sh <<EOF
cd dspeech/
python3 DeepSpeech-examples/mic_vad_streaming/mic_vad_streaming.py -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer -r 44100
EOF
chmod +x runDeepSpeech.sh
