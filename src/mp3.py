"""
Functions for downloading and playing mp3 files that read jokes out loud
"""

# import time
import os
import pyglet
# import pygame
import urllib2
import urllib
# from multiprocessing import Pool

# Constants
MP3_FILE_NAME = "joke.mp3"
URL_BASE = "http://tts-api.com/tts.mp3?"

## Make an api call to get an mp3 file of a computer voice reading the input text
## @param input_text: string of the joke to be read out loud
def getMp3(input_text):
    encode = urllib.urlencode({"q":input_text})
    req = urllib2.Request(URL_BASE + encode)
    audio = urllib2.urlopen(req) # This line has the most latency
    data = audio.read()

    with open(MP3_FILE_NAME,"wb") as f:
        f.write(data)

def unlinkMp3():
    if os.path.exists(MP3_FILE_NAME):
        os.remove(MP3_FILE_NAME)

def exiter(dt):
    pyglet.app.exit()

## Synchronously play the mp3 file
def playMp3():
    sound = pyglet.resource.media(MP3_FILE_NAME, streaming=False)
    sound.play()
    pyglet.clock.schedule_once(exiter, sound.duration+1)
    pyglet.app.run()

    print "Finished" # DEBUG
    return

## Wrapper that encapsulates all these methods
def read_joke(input_text):
    getMp3(input_text)
    playMp3()
    unlinkMp3()
    return

if __name__ == '__main__':
    getMp3("Hello world")
    playMp3()
    unlinkMp3()
