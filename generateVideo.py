import os
import random
from moviepy.editor import *

path = '/kaggle/input/clips'
clips = os.listdir(path)
videoClips = [ VideoFileClip(os.path.join(path, clip)).without_audio() for clip in clips ]
maxDuration = max(map(lambda video: video.duration, videoClips))
videoClips = [clip.loop(duration=maxDuration) for clip in videoClips]
video = concatenate_videoclips(videoClips, method='compose')
video = video.resize(width=1920,height=1080)

minutes = random.randint(60, 151)
print(minutes)
reqDuration = minutes * 60
finalVideo = video.loop(duration=reqDuration)

music = AudioFileClip('/kaggle/input/audio/relaxing.mp3')
audio = afx.audio_loop(music, duration=reqDuration)
finalVideo = finalVideo.set_audio(audio)

finalVideo.write_videofile('video.mp4', codec='libx264')