from moviepy.editor import *
import os 



image_folder = "./static/Boards/"
output_folder = "../Output/"
music = "./Music/"

output_name = "chessvideo"

class Video():
    def __init__(self, image_folder=image_folder, music_folder=music, output_folder=output_folder, output_name=output_name):
        self.image_folder = image_folder
        self.music_folder = music
        self.output_folder = output_folder
        self.output_name = output_name

    def create_video(self, duration=2):

        imgs = [os.path.join(self.image_folder, filename) for filename in os.listdir(self.image_folder)] 
        imgs.sort()
        clips = [ImageClip(img).set_duration(duration) for img in imgs]


        video = concatenate_videoclips(clips, method="compose")
        video.write_videofile(f"{self.output_folder}{self.output_name}.mp4", fps=24)

    def add_audio(self):
        videoclip = VideoFileClip(f"{self.output_folder}chessvideo.mp4")
        audioclip = AudioFileClip(f"{self.music_folder}music.mp3")
        audioclip = audioclip.set_duration(videoclip.duration)

        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile(f"{self.output_folderoutput_folder}{self.output_name}.mp4")

