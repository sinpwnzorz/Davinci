#!/bin/bash
UNnumber="$1"

# If UN# is missing, errors
if [[ -z "$UNnumber" ]]
then
        # To prevent this make sure a valid UN # goes after ./erg.sh [valid UN#]
        echo "Failed. Please type a UN # after the script."
else
        # Redundancy for specific UN# and displays the materials this guide is effective for
        if more ERG_Material_Blue_pages_English.csv | grep "${UNnumber}" | tr ',0-9' ' ';
        then
                # Calculates which guide # to use corresponding to the UN # and the following guide #
                ergGuideNo=$(cat ERG_Material_Blue_pages_English.csv | grep "${UNnumber}", | cut -d ',' -f 2 | head -n 1)
                ergNextGuideNo=$(expr "${ergGuideNo}" + 1)
                printf "\n"
                echo The following information is to ERG Guide "${ergGuideNo}"

                # Formatting text nicely to pass in GUIDE # as one variable
                appendGuide=$(echo GUIDE "${ergGuideNo}")
                appendNextGuide=$(echo GUIDE "${ergNextGuideNo}")

                # Effectively this calculates which line the guide and the following guide starts on
                ergGuideStartLine=$(cat erg.txt | tr '[:blank:]' ' ' | grep "${appendGuide}" | cut -d ' ' -f 1)
                ergNextGuideStartLine=$(cat erg.txt | tr '[:blank:]' ' ' | grep "${appendNextGuide}" | cut -d ' ' -f 1)

                # 4126 is max doc length, measured from the bottom (subtracting) where the guide begins
                inverseGuideStart=$(expr 4126 - "${ergGuideStartLine}")

                # next guide start line subtracted this guides start line equals number of lines apart to shore up the document by
                endLine=$(expr "${ergNextGuideStartLine}" - "${ergGuideStartLine}" - 1)

                # tail starts from bottom up to the inverse start location, for a number of lines equal to the difference of the line number between the next guide and this
                tail -"${inverseGuideStart}" erg.txt | head -n "${endLine}"
                echo End
        else
                echo The UN \# you provided does not exist, or the characters after the script are incorrectly formatted.
        fi
fi
