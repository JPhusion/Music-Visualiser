from AudioAnalyzer import *
from PIL import Image, ImageFilter, ImageEnhance
from tkinter.filedialog import askopenfilename
from shutil import copyfile
from os.path import isfile, join
from tqdm import tqdm
import pygame.freetype
import os
import cv2
import wave
import random
import easygui
import colorsys

# def convert_pictures_to_video(pathIn, pathOut, fps):
#     pbar = tqdm(total=970, bar_format='Processing {r_bar} |{bar}| {percentage:3.0f}%', colour='GREEN')
#     ''' this function converts images to video'''
#     frame_array = []
#     files = [f for f in os.listdir(pathIn) if isfile(join(pathIn,f))]
#     for i in range (len(files)):
#         filename = pathIn+"/"+files[i]
#         '''reading images'''
#         img = cv2.imread(filename)
#         height, width, layers = img.shape
#         size = (width,height)
#         frame_array.append(img)
#         pbar.update(n=0.5)
        
#     out=cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'mp4v'), fps,size)
#     for i in range(len(frame_array)):
#         out.write(frame_array[i])
#         pbar.update(n=0.5)
#     out.release()

# convert_pictures_to_video("./assets/output", "C:/Users/joshu/Desktop/test_video.mp4", 5)

import moviepy.editor as mpe

def combine_audio(vidname, audname, outname, fps):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

combine_audio("C:/Users/joshu/Desktop/test_video.mp4", "C:/Users/joshu/Desktop/riptide.wav", "C:/Users/joshu/Desktop/test_video_with_sound.mp4", 5)
