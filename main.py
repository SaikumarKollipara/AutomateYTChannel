import os
from moviepy.editor import *

clips = os.listdir('./clips/')
video = concatenate_videoclips([ VideoFileClip(os.path.join('./clips', clip)).without_audio() for clip in clips ], method='compose')
video = video.resize(width=1920,height=1080)

hours = 0
minutes = 1
reqDuration = (hours * 60 + minutes) * 60
# reqDuration = 50
finalVideo = video.loop(duration=reqDuration)

# music = AudioFileClip('./audio_clip.mp3')
# audio = afx.audio_loop(music, duration=reqDuration)
# finalVideo = finalVideo.set_audio(audio)


finalVideo.write_videofile('merged.mp4', codec='libx264')