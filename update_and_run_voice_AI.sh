rsync -avzhe ssh root@freenas.lianowarlegion.com:/mnt/mainpool/nas/windows/Git/deepspeech/mic_vad_streaming.py ~/dspeech/DeepSpeech-examples/mic_vad_streaming
cd dspeech/
python3 DeepSpeech-examples/mic_vad_streaming/mic_vad_streaming.py -m deepspeech-0.9.3-models.tflite -s deepspeech-0.9.3-models.scorer -r 44100
