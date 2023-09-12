import json
import os
from pathlib import Path

from moviepy.editor import VideoFileClip

DIRNAME = Path(os.path.dirname(__file__))
intro_video = VideoFileClip(str(DIRNAME/ "data/intro/intro_video.mp4"))

def play_intro(video):
    with open (DIRNAME / "data/settings.json", "r") as stream:
        settings = json.load(stream)
    size = settings["resolution"]
    video = video.resize(size)
    video.preview()
    video.reader.close()
    video.audio.reader.close_proc()

play_intro(intro_video)
