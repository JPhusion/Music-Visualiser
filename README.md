# JPhusion's Music Visualiser
## What is it?
The music visualiser takes in an audio file as input and analyses the decibel level of multiple frequency bands and produces a visual representation of each frequency band using a circle with extending bars. The visualiser is capable of visualizing live as well as rendering a video output.

## Screenshots
![alt tag](https://cdn.discordapp.com/attachments/925547447487447081/927855243935490088/unknown.png "Sample screenshot 1")

![alt tag](https://media.discordapp.net/attachments/925547447487447081/927786085050880010/unknown.png?width=1197&height=673 "Sample screenshot 2")

![alt tag](https://media.discordapp.net/attachments/925547447487447081/927787261821607967/unknown.png?width=1197&height=673 "Particles accellerating due to high base decibel level")

## Functionality
- Visualise an audio file live.

- Render a video file given an audio file.

- Randomly generates a background image. (Images can be changed by the user by placing files in the `./assets/backgrounds` directory)

- Add text (titles of songs or artists)

- Changes color with the music

- Has randomly generated particles with accelleration based on base decibel levels.

## Installation*
### Using an Environment with Python Installed
1. Download the zip file of the latest release.

2. Unzip folder to desired location

4. Navigate to the directory `Visualiser`

5. Enter the following command:
```
# Windows:
pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
# or
sudo pip3 install -r requirements.txt
```
6. Run `player.py` or `renderer.py` depending if you want to play music live or render files

##### *Installers/packages are not yet supported. Feel free to contact me if you have any questions or have a method to package this software for cross platform.

## Setup
- When the software is first run, you will be promted to enter the location of the .wav audio file.

- You will then be promoted to enter title text. Just pressing [ENTER] will skip this and not place any title text on your render.

- You can also choose the ouput directory and framerate if you are rendering, else the video playback will start after analysis of the audio has concluded.
