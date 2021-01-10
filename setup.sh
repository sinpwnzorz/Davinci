#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cat <<EOF
██╗███╗░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░░░░██╗███╗░░██╗░██████╗░
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░██║████╗░██║██╔════╝░
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░░░░██║░░░░░██║██╔██╗██║██║░░██╗░
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██║░░░░░██║██║╚████║██║░░╚██╗
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║███████╗███████╗██║██║░╚███║╚██████╔╝
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░

██████╗░░█████╗░██╗░░░██╗██╗███╗░░██╗░█████╗░██╗
██╔══██╗██╔══██╗██║░░░██║██║████╗░██║██╔══██╗██║
██║░░██║███████║╚██╗░██╔╝██║██╔██╗██║██║░░╚═╝██║
██║░░██║██╔══██║░╚████╔╝░██║██║╚████║██║░░██╗██║
██████╔╝██║░░██║░░╚██╔╝░░██║██║░╚███║╚█████╔╝██║
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚════╝░╚═╝
--------------------------------------------------------------------
Digital Analog Virtual Independent Networked Computational Interface
EOF

pip install --upgrade pip #makes sure we're ready for pip3 I think

for aptToolName in $(cat aptPackages.txt)
do
    if ! { apt install $aptToolName -y 2>&1 || echo E: update failed; } | grep -q '^[WE]:'; then
        echo [  ${GREEN}OK${NC}  ] Installed $aptToolName.
    else
        echo [${RED}FAILED${NC}] Install of $aptToolName, try a manual install.
    fi
done

# Same cool shit for above, but with pip3
# for pipToolName in $(cat pipPackages.txt)
# do
#     if ! { sudo pip3 install $pipToolName 2>&1 || echo E: update failed; } | grep -q '^Successfully installed:'; then
#         echo [ ${GREEN}SAME${NC} ] $pipToolName is already installed.
#     elif ! { sudo pip3 install $pipToolName 2>&1 || echo E: update failed; } | grep -q '^[WE]:'; then
#         echo [${RED}FAILED${NC}] Install of $pipToolName, try a manual install.
#     else
#         echo [  ${GREEN}OK${NC}  ] Installed $pipToolName.
#     fi
# done

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

#install googler
cd Downloads
wget -c https://github.com/jarun/googler/archive/v4.3.1.tar.gz #downloading  "googler"
tar -xvf v4.3.1.tar.gz #un-tarballing
cd googler-4.3.1
make install #i still dont know what this does
cd auto-completion/bash/
cp googler-completion.bash /etc/bash_completion.d/
cd #remove wget file?

#create and chmod run script to executable
touch ~/runDeepSpeech.sh
cat > ~/runDeepSpeech.sh <<EOF
cd ~/dspeech/
python3 DeepSpeech-examples/mic_vad_streaming/mic_vad_streaming.py -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer -r 44100
EOF
chmod +x runDeepSpeech.sh
