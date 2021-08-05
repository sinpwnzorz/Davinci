# Digital Analog Virtual Independent Networked Computational Interface - D.A.V.I.N.C.I.
This project features a multifaceted bridge between nearly any device you've ever spoken to any any button you've ever pressed, ambitious sure, but achievable none the less. The project is currently in it's home in a Raspberry Pi 4 though may work it's way into a different platform.

## Motivation
The inspiration for this project comes from always needing another hand working on my projects. I can only ask for so many favors back to back from my better half before getting the stink eye, so I'm making this helper that is always ready, waiting, happy, and excited to help.
At it's core is the 100% offline speech recognition software, currently Mozilla's DeepSpeech written in Python3 to offer the modern services all the other online home assistants have.
However it's destiny is to Phase 1 of the Phase 2 project as the brains behind a 6-axis UR arm to help me out around the shop. Remember when Tony gets sprayed with a fire extinguisher? Yeah, like that one.
We have roombas, and lawn..bas? Why not a shopba? Or everythinba?

## Hardware:
* Raspberry Pi 4 - Mainframe (https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* ReSpeaker Mic Array v2.0 - Microphone (https://www.seeedstudio.com/ReSpeaker-USB-Mic-Array-p-4247.html)

## Top level features
- [x] 100% usable Voice recognition without internet or network connectivity, excluding additions.
- [x] Text-To-Speech OR Prerecorded voice library engine for replies.
  - [ ] Mute AI Speech recognition while it's talking back to me to prevent it from commanding itself.
- [ ] Threading / Subprocesses due to limited CPU strength on the Raspberry Pi 4's 4 threads:
  - [x] Subprocesses for running processes while other processes run.
  - [x] Threading for running processes while other processes run.
  - [ ] Mesh Threading/node clusters??? for threading processes to other Raspberry Pi 4's on the network if possible?
  - [ ] Data Sync for all Pi's mass distribution of modified files. Could include automatic updates / update commits?
- [ ] G-code programmable 6-axis arm .
  * https://github.com/RorschachUK/meArmPi
  - [ ] Literally a million features I'm too lazy to write out right now.

## Roadmap for fun additional features / to-do list
- [ ] Help menu? "What can I say"
  - [x] Basic functionality.
  - [ ] Adaptive.
- [ ] Voice recognition check, "do you understand (blank)"
  - [x] Basic functionality.
  - [ ] Adaptive.
- [ ] Digital Secretary. Typical Alexa / Google Assistant / Siri / Echo features (Will add those later)
  - [ ] Calculator / Math
    * https://github.com/jarun/bcal
  - [ ] Schedule confliction notifier, automatically listens and checks calendar if it hears "I can", or "I will", or "I could", etc.
  - [ ] Calendar + reminder + notes automation.
    * https://github.com/jarun/pdd
  - [ ] Errand Reminders when I say "I should go to the store soon" - Also stars car preemptively when too cold.
  * Various AI based githubs:
    * https://github.com/synesthesiam/rhasspy
    * https://github.com/the-raspberry-pi-guy/Artificial-Intelligence-Pi
    * http://fhem.de/fhem.html
- [ ] HASSIO home automation integration.
  * https://www.home-assistant.io/getting-started/
- [ ] Bablefish Realtime Translator - With secret code to translate a localized reply like "Can I speak to your manager" in that language
  * https://github.com/formiel/speech-translation
- [ ] Voice control other devices: 
  - [ ] Android SDK to pull/push notifications, texts, and calls.
    - [ ] AI to be able to put phone into tether mode if asked.
    - [ ] And vice versa
      * https://github.com/LorenzoRogai/RaspberryRemoteControl
    - [ ] Order food (hard coded menu options until voice is smoothed out) from subway app.
  - [ ] FreePBX integration in place of Android SDK for calls.
    * https://github.com/climberhunt/PiPhone
  - [ ] Operate 3D printer(s) via Octoprint with voice.
    - [ ] Potentially including automatic searching, downloading, slicing, and printing.
      * https://github.com/Ultimaker/Cura
  - [ ] Remotely execute commands to/from networked computers.
  - [ ] Operating IoT devices such as lights and outlets
    * https://www.electronicsforu.com/electronics-projects/multi-language-voice-control-iot-home-automation-system-using-google-assistant-and-raspberry-pi
    * https://github.com/xkonni/raspberry-remote
    * https://github.com/penguintutor/pi-power
  - [ ] Thermostat and Air conditioner controls.
    * https://github.com/Willseph/RaspberryPiThermostat
  - [ ] SSH-Agent configured for pass-wordless communication between Linux boxes.
    - [x] Basic functionality.
    - [ ] PowerShell to Windows machines too.
    - [ ] Network wide operability.
  - [ ] Linux / Operating system level voice controlled commands.
- [ ] Automotive Assistant:
  - [ ] Active noise contol
    * https://www.raspberrypi.org/forums/viewtopic.php?t=8766
    * https://github.com/psykulsk/RpiANC
- [ ] Virtual DJ:
  - [ ] Add playlists, and add songs to playlists. Delete songs or playlists.
  - [ ] Customize voice playlists.
  - [x] Download music by voice request using youtube-dl.
    * https://github.com/ytdl-org/youtube-dl/
  - [ ] Play music by voice request.
    - [x] Basic functionality.
      * https://github.com/popcornmix/omxplayer
    - [ ] If no song present, compare perhaps 66% of the words for hits and attempt to play that song, or ask if that's the right song
    - [ ] If requested song isn't available attempt to download it with prompt
  - [x] Stop / Pause music
- [ ] Web / Online interaction:
  - [ ] Web crawler / search engine results.
    - [ ] https://github.com/jarun/ddgr
    - [ ] https://github.com/jarun/googler/
  - [ ] Discord bot integration.
- [ ] Network Tools:
  - [ ] Discover SSID's
  - [ ] Voice connect to open networks
  - [ ] Auto connect to saved networks
  - [ ] Voice password additions for networks
  - [ ] Deauthentication Packet detection + announcement
  - [ ] Network security audit
    - [ ] Record local devices
    - [ ] automated pentesting (Aircrack-ng suite):
  - [x] Voice automated internet speed tests
- [ ] Security:
  - [ ] Welcome Home door lock automation.
  - [ ] Visitor detection 
    - [ ] Pixy2 
    - [ ] Cell Phone MAC Identity
    - [ ] Voice Identification
      * https://github.com/CorentinJ/Real-Time-Voice-Cloning
- [ ] Voice Memo Shadowplay - What did you just say? Find out! Play back the past.
- [ ] codename CASPER
  * https://github.com/jakubczaplicki/face-recognition-server
  * https://github.com/jivoi/awesome-osint
  * https://github.com/lockfale/OSINT-Framework
  * https://github.com/s0md3v/Photon
  * https://github.com/milo2012/osintstalker
  * https://github.com/sinwindie/OSINT
  * https://github.com/blaCCkHatHacEEkr/OSINT_TIPS
  * https://github.com/SharadKumar97/OSINT-SPY
  * https://github.com/sc1341/InstagramOSINT
  * https://github.com/twelvesec/gasmask
  * https://github.com/Datalux/Osintgram
  * https://github.com/nikharris0/probemon
- [ ] Emergency Responder Guide UN# Query and response
  - [x] Basic functionality.
    * https://github.com/sinpwnzorz/Davinci/tree/main/features/erg
    * https://www.phmsa.dot.gov/hazmat/erg/erg-data-files
  - [ ] Incorporate the ERG into the voice control.
  - [ ] Filter by types of incidents / hazards for more specific readout of response procedure.
  - [ ] Remove unneccessarily present line numbers.
- [ ] Voice activated emulators!
  - [ ] Maybe brings up QR codes somewhere to scan with phones to go to web ui for controllers?
- [x] For fun:
  - [x] Enter the matrix (launches cmatrix on all possible computers on network for 60 seconds)
  - [x] chopper plays get to the chopper
  - [x] self confidence booster


## Installation
I'm super lazy, so I'm going to attempt to make an extremely easy single line setup that kicks everything off. In theory run this from the home directory. It should make folders and what not for stuff:
```
sudo ./setup.sh
```

## Contribute
If you'd like to help out in any way reach out to me (discord) and check out the (contributing guidelines) hyperlink sauce

## Credits

## Links
Main Links
* [DeepSpeech on github](https://github.com/mozilla/STT)
* [DeepSpeech docs](https://deepspeech.readthedocs.io/en/latest/)
* [DeepSpeech forum](https://discourse.mozilla.org/c/mozilla-voice-stt/247)
* [DeepSpeech examples](https://github.com/mozilla/DeepSpeech-examples)
* [Wiseman Voice Activity Detector (VAD)](https://github.com/wiseman/py-webrtcvad)
* [Halo](https://pypi.org/project/halo/)
Cool Other Stuff Links
* [Googler, CLI Google](https://github.com/jarun/googler/)
* [eDEX-UI on RPi4](https://github.com/GitSquared/edex-ui)
* [eDEX-UI on RPi4 Youtube tutorial](https://www.youtube.com/watch?v=DJOAmYlDQuM)
* [pyttsx3 Python3 Text-to-Speech engine](https://pyttsx3.readthedocs.io/en/latest/engine.html)
