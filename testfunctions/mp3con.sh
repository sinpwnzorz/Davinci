#!/usr/bin/env bash

# My bash Script to convert mp4 to mp3
# By NerdJK23
# web: www.computingforgeeks.com
# email: kiplangatmtai@gmail.com

# Requires
# ffmpeg installed
# lame installed
# Check https://computingforgeeks.com/how-to-convert-mp4-to-mp3-on-linux/
# for original, this has been modified by Sinpwnzorz for this project

current_dir=`pwd`
base_name=` basename "$current_dir"`

if [[ ! -d "$base_name"-mp3 ]]; then

echo "$base_name" | xargs  -d "\n" -I {} mkdir {}-mp3
    echo ""
fi
echo ""

# Bigin to covert videos to mp3 audio files
# -d "\n" > Change delimiter from any whitespace to end of line character

find . -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" | xargs  -d "\n"  -I {} ffmpeg -i {} -b:a 320K -vn "$base_name"-mp3/{}.mp3

# remove video extensions

cd "${base_name}"-mp3

for file_name in *; do
    mv "$file_name" "`echo $file_name | sed  "s/.mp4//g;s/.mkv//g;s/.webm//g"`";
done

# Move audio directory to ~/Music

if [[ ! -d ~/Music ]]; then
    mkdir ~/Music
fi
cd ..

mv  "$base_name"-mp3 ~/Music/

# Check if conversion successfull

echo ""

if [[ $? -eq "0" ]];then
    echo " All files converted successfully"
else
    echo "Conversation failed"
    exit 1
fi

# Renames converted files to replace spaces with underscores
