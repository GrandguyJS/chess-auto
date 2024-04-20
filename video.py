from moviepy.editor import *
import os 

image_folder = "./Boards/"
output_folder = "./Output/"
music = "./Music/"

def create_video():

    imgs = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)] 
    imgs.sort()
    clips = [ImageClip(img).set_duration(2) for img in imgs]


    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(f"{output_folder}chessvideo.mp4", fps=24)

def add_audio():
    videoclip = VideoFileClip(f"{output_folder}chessvideo.mp4")
    audioclip = AudioFileClip(f"{music}music.mp3")
    audioclip = audioclip.set_duration(videoclip.duration)

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(f"{output_folder}chessmusic.mp4")

create_video()
add_audio()