#install googler
cd Downloads
wget -c https://github.com/jarun/googler/archive/v4.3.1.tar.gz #downloading  "googler"
tar -xvf v4.3.1.tar.gz #un-tarballing
cd googler-4.3.1
sudo make install #i still dont know what this does
cd auto-completion/bash/
sudo cp googler-completion.bash /etc/bash_completion.d/
cd

#install ffmpeg and lame to convert .mkv, .webm, .mp4 into .mp3 https://computingforgeeks.com/how-to-convert-mp4-to-mp3-on-linux/
sudo apt -y install ffmpeg lame

#install youtube-dl for downloading youtube videos locally
sudo pip install youtube-dl --upgrade
#but it's in /usr/local/bin/youtube-dl
#everything thinks it should be in /usr/bin/youtube-dl

#install json query for parsing youtube-dl queries
sudo apt-get install jq

https://vitux.com/how-to-replace-spaces-in-filenames-with-underscores-on-the-linux-shell/

pip install speedtest-cli










ls -Artc | tail -n 1



