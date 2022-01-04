import colorsys
import easygui
import random
import wave
import cv2
import os
import pygame.freetype
import moviepy.editor as mpe
from tqdm import tqdm
from os.path import isfile, join
from shutil import copyfile
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageFilter, ImageEnhance
from AudioAnalyzer import *
print("Initialising...")

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
print("Select a .wav file")
particles = []


def rnd_color():
    h, s, l = random.random(), 0.5 + random.random() / \
        2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]


def update_particles():
    for particle in particles:
        try:
            particle[0][0] += particle[1][0]*(24/renderfps)
            particle[0][1] += particle[1][1]*(24/renderfps)
            particle[2] -= 0.01*(24/renderfps)
            pygame.draw.circle(screen, particle[3], [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)
        except ValueError:
            particle[0][0] += particle[1][0]*(24/renderfps)
            particle[0][1] += particle[1][1]*(24/renderfps)
            particle[2] -= 0.01*(24/renderfps)
            pygame.draw.circle(screen, (255, 255, 255), [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)


def scale_image(image):
    w, h = image.get_width(), image.get_height()
    scale_factor = abs(radius - min_radius)/600 + 1
    if w/16 > h/9:
        size = (int(w*(1080/h)*scale_factor), int(h*(1080/h)*scale_factor))
    elif w/16 < h/9:
        size = (int(w*(1920/w)*scale_factor), int(h*(1920/w)*scale_factor))
    else:
        size = (int(1920*scale_factor), int(1080*scale_factor))
    position = (int(960-size[0]/2), int(540-size[1]/2))
    return size, position


def convert_pictures_to_video(pathIn, pathOut, fps):
    pbar = tqdm(
        total=frames, bar_format='Processing {r_bar} |{bar}| {percentage:3.0f}%', colour='GREEN')
    ''' this function converts images to video'''
    files = [f"{pathIn}/{i+1}.bmp" for i in range(frames-1)]
    out = cv2.VideoWriter(
        pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1920, 1080))
    for filename in files:
        out.write(cv2.imread(filename))
        pbar.update(n=1)
    out.release()


def combine_audio(vidname, audname, outname, fps=25):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)


filename = easygui.fileopenbox(msg="Select File to Generate Video",
                               default=f"{os.getenv('HOMEPATH')}/desktop/desktop", filetypes=["*.wav"])
title = input("Bottom Text: ")

print("Select Output Directory")
output = easygui.diropenbox(msg="Select Output Directory",
                            default=f"{os.getenv('HOMEPATH')}/desktop/desktop")

while True:
    try:
        renderfps = int(input("Output FPS (integer): "))
        break
    except ValueError:
        print("Please enter an integer")

print("Analysing audio...")

analyzer = AudioAnalyzer()
analyzer.load(filename)

with wave.open(filename) as mywav:
    duration_seconds = mywav.getnframes() / mywav.getframerate()
    samplerate = mywav.getframerate()

clock = pygame.time.Clock()
pygame.display.set_caption("Rendering Visualiser")
pygame.init()

infoObject = pygame.display.Info()

# screen_w = int(infoObject.current_w/2.2)
# screen_h = int(infoObject.current_w/2.2)

screen_w, screen_h = 1920, 1080

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

t = pygame.time.get_ticks()
getTicksLastFrame = t

timeCount = 0

avg_bass = 0
bass_trigger = -30
bass_trigger_started = 0

min_decibel = -80
max_decibel = 80

circle_color = (255, 255, 255)
polygon_default_color = [255, 255, 255]
polygon_bass_color = polygon_default_color.copy()
polygon_color_vel = [0, 0, 0]

poly = []
poly_color = polygon_default_color.copy()

circleX = int(screen_w / 2)
circleY = int(screen_h/2)

min_radius = 100
max_radius = 150
radius = min_radius
radius_vel = 0

bass = {"start": 50, "stop": 100, "count": 12}
heavy_area = {"start": 120, "stop": 250, "count": 40}
low_mids = {"start": 251, "stop": 2000, "count": 50}
high_mids = {"start": 2001, "stop": 6000, "count": 20}

freq_groups = [bass, heavy_area, low_mids, high_mids]
bars = []
tmp_bars = []

length = 0

for group in freq_groups:
    g = []
    s = group["stop"] - group["start"]
    count = group["count"]
    reminder = s % count
    step = int(s/count)
    rng = group["start"]

    for i in range(count):
        arr = None
        if reminder > 0:
            reminder -= 1
            arr = np.arange(start=rng, stop=rng + step + 2)
            rng += step + 3
        else:
            arr = np.arange(start=rng, stop=rng + step + 1)
            rng += step + 2

        g.append(arr)
        length += 1

    tmp_bars.append(g)

angle_dt = 360/length

ang = 0

for g in tmp_bars:
    gr = []
    for c in g:
        gr.append(
            RotatedAverageAudioBar(circleX+radius*math.cos(math.radians(ang - 90)), circleY+radius*math.sin(math.radians(ang - 90)), c, (255, 0, 255), angle=ang, width=8, max_height=370))
        ang += angle_dt
    bars.append(gr)

print("Preparing media...")

# font = pygame.freetype.Font(f'./assets/fonts/{random.choice(os.listdir("./assets/fonts/"))}', 60)
font = pygame.freetype.Font(
    f'./assets/fonts/FontsFree-Net-SFProDisplay-Bold.ttf', 60)
textsurface = font.get_rect(title)

ImageEnhance.Contrast(Image.open(f'assets/backgrounds/{random.choice(os.listdir("./assets/backgrounds"))}').filter(
    ImageFilter.GaussianBlur(10))).enhance(0.4).save('./assets/backgrounds/background_image.png')
background = pygame.image.load(
    f'assets/backgrounds/background_image.png').convert_alpha()

logo = pygame.image.load('assets/logo.png').convert_alpha()
value_hsv = [1, 0.5, 220]

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

counter = 0
running = False
frames = int(duration_seconds*renderfps)
pbar = tqdm(total=frames,
            bar_format='Rendering {r_bar} |{bar}| {percentage:3.0f}%', colour='GREEN')

while running:

    particles.append([[screen_w/2, screen_h/2], [random.randint(0, 1000)/100 - 5,
                     random.randint(0, 1000)/100 - 5], random.randint(0, 10), (255, 255, 255)])

    counter += 1

    avg_bass = 0
    poly = []

    deltaTime = 1/renderfps

    timeCount += deltaTime

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(background, scale_image(
        background)[0]), scale_image(background)[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for b1 in bars:
        for b in b1:
            b.update_all(
                deltaTime, timeCount, analyzer)

    for b in bars[0]:
        avg_bass += b.avg

    avg_bass /= len(bars[0])

    if avg_bass > bass_trigger:
        if bass_trigger_started == 0:
            bass_trigger_started = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - bass_trigger_started)/1000.0 > 2:
            polygon_bass_color = rnd_color()
            bass_trigger_started = 0
        if polygon_bass_color is None:
            polygon_bass_color = rnd_color()
        newr = min_radius + int(avg_bass * ((max_radius - min_radius) /
                                (max_decibel - min_decibel)) + (max_radius - min_radius))
        radius_vel = (newr - radius) / 0.15

        polygon_color_vel = [
            (polygon_bass_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]
        for i in range(10):
            particles.append([[screen_w/2, screen_h/2], [random.randint(0, 1000)/100 - 5,
                             random.randint(0, 1000)/100 - 5], random.randint(0, 10), poly_color])
        update_particles()
        update_particles()
        update_particles()

    elif radius > min_radius:
        bass_trigger_started = 0
        polygon_bass_color = None
        radius_vel = (min_radius - radius) / 0.15
        polygon_color_vel = [
            (polygon_default_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]

    else:
        bass_trigger_started = 0
        poly_color = polygon_default_color.copy()
        polygon_bass_color = None
        polygon_color_vel = [0, 0, 0]

        radius_vel = 0
        radius = min_radius

    radius += radius_vel * deltaTime

    for x in range(len(polygon_color_vel)):
        value = polygon_color_vel[x]*deltaTime + poly_color[x]
        poly_color[x] = value

    for b1 in bars:
        for b in b1:
            b.x, b.y = circleX+radius * \
                math.cos(math.radians(b.angle - 90)), circleY + \
                radius*math.sin(math.radians(b.angle - 90))
            b.update_rect()

            poly.append(b.rect.points[3])
            poly.append(b.rect.points[2])

    update_particles()
    value_hsv[0] = (value_hsv[0]+0.005) % 1
    ring_color = colorsys.hsv_to_rgb(value_hsv[0], value_hsv[1], value_hsv[2])
    try:
        pygame.draw.polygon(screen, poly_color, poly)
    except ValueError:
        pygame.draw.polygon(screen, (255, 255, 255), poly)
    pygame.draw.circle(screen, ring_color, (circleX, circleY), int(radius))
    pygame.draw.circle(screen, circle_color, (circleX, circleY), int(radius-8))
    screen.blit(pygame.transform.scale(logo, (abs(int(radius*1.5)), abs(int(radius*1.5)))),
                (circleX-0.5*radius*1.5, circleY-0.5*radius*1.5))
    font.render_to(screen, (40, 1000), title, (255, 255, 255))
    pygame.display.flip()
    pygame.image.save(screen, f"./assets/output/{counter}.bmp")
    pbar.update(n=1)
    if counter == frames:
        running = False

pygame.quit()

convert_pictures_to_video(
    "./assets/output", "./assets/output/video.mp4", renderfps)
combine_audio("./assets/output/video.mp4", filename,
              f"{output}/{title}.mp4", renderfps)

print("Cleaning up...")

for f in os.listdir("./assets/output"):
    os.remove(os.path.join("./assets/output", f))

print("Render Successful!")
