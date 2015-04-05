
import unirest
import time
import pyglet
import urllib2
import urllib
from multiprocessing import Pool

stats = {"Criminal":0, "Sex":0,"Animal":0,"Chuck Norris":0,"Law":0,"Marriage":0}


player = pyglet.media.Player()

def getJokes():
    for x in range(1,10):
        response = unirest.get("https://webknox-jokes.p.mashape.com/jokes/random",
                headers={
                    "X-Mashape-Key": "Dv7dJmG74lmshSyC5z2CezBN0A1Xp1OpexHjsnJDI2yWrnmYhS",
                    "Accept": "application/json"
                    }
                )
        

        try:
            print response.body
            encode = urllib.urlencode({"q":response.body["joke"]})
            result = pool.apply(getMP3,"http://tts-api.com/tts.mp3?"+encode,mp3done)

           
            try:
                stats[response.body["category"]] += 1
            except KeyError:
                try:
                    stats[response.body["category"]] = 1
                except KeyError:
                    print "KeyError"
            
        except UnicodeEncodeError:
            print "Unicode issue"


def getMP3(url):
    print "IM DOING THIS DAM JOB"
    req = urllib2.Request(url)
    song = urllib2.urlopen(req)
    data = song.read()
    f = open(mp3name,"wb")
    f.write(data)
    f.close()

def mp3done():
    mp3name = "song.mp3"
    sound = pyglet.media.load(mp3name,streaming=False)
    sound.play()
#    player.queue(sound)
#    player.play()
    print "Finished"
    return

if __name__ == '__main__':
    pool = Pool(processes=1)
    getJokes()
    pool.close()
    pool.join()
