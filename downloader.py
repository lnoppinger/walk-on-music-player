import json
from pytube import YouTube
import subprocess
import os
import time

# workaround for age restriction
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

errorFile = open("error.txt", "a")

file = open('data.json')
data_str = file.read()
file.close()
data = json.loads(data_str)

for d in data:
    try:
        yt = YouTube(d["video"])
        yt.streams.filter(only_audio=True).first().download(filename=d["name"] + ".mp4")
        subprocess.run(
            'ffmpeg -y -i ' + d["name"] + '.mp4 -ss ' + d["start"] + ' -af "afade=t=in:st=' + d["start"] + ':d=2" -filter:a loudnorm ' + d["name"] + '.mp3',
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
    except Exception as e:
        print(d["name"] + " failed to download.")
        errorFile.write(str(e) + "\n\n")

errorFile.close()
time.sleep(10)
for file in os.listdir("./"):
    if file.endswith(".mp4"):
        os.remove(file)