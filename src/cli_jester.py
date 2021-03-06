#!/usr/bin/python

"""
Commandline interface for intellijester

This file should only contain code for the command line interface. All code
necessary to base functionality should be in external files.
"""

import os
import sys
import threading
import time

import mp3
from JokeBag import JokeBag, JokeTooLong

from eeg import EEG
import intellijester

UNICODE_APOST = u"\u2019"

global eeg

def killProgram():
    # kill the subprocess
    eeg.kill_process()
    os._exit(0)

## Takes two strings and returns True if one is a substring of the other
## and begins at the first character of the string.
def matches(a, b):

    lenA = len(a)
    lenB = len(b)

    if lenA == 0 or lenB == 0:
        # empty string should return false always
        return False

    if lenA > lenB:
        # swap them so that a is shorter
        tmp = b
        b = a
        a = tmp

    # assume that lenA <= lenB
    b = b[0:lenA]

    # if a & b are a match, then return true
    return a == b

def usage():
    HELP_MSG = """
intellijester command prompt options:

quit                             This quits the application cleanly
help                             This displays this help message
clear                            Clear the screen
joke (or simply hitting enter)   Tell a joke
"""
    print HELP_MSG
    return

def print_joke(j):
    # Check if there's a title, and print it if there is
    if "title" in j:
        title = j["title"]
        if title != "":
            print title
            print "--------"

    # Print the body of the joke
    text = j["joke"]
    print text
    print len(text)

    return

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main(joke_bag):
    global eeg
    try:
        while True:
            # text = raw_input("\nPress enter to see a joke, q to quit: ")
            key = ""

            if matches(key, "quit") or key == "Q" or key == ";q" or key == "exit":
                killProgram()
            elif matches(key, "help") or key == "--help":
                usage()
            elif matches(key, "clear") or key == "cls":
                os.system('clear')
            elif matches(key, "keys"):
                print joke_bag.cat_map.keys()
            else:
                while True:
                    try:
                        next_cat, j_text = joke_bag.get_joke_wrapper()
                        # Check for ascii
                        if not is_ascii(j_text):
                            j_text = j_text.replace(UNICODE_APOST, "'")
                            if not is_ascii(j_text):
                                continue

                        os.system('clear')
                        print j_text

                        # Play mp3
                        mp3.read_joke(j_text)

                        # Get user rating
                        val = -1
                        if eeg.user_likes_joke():
                            print "\nTwo thumbs up!"
                            val = 1
                        else:
                            print "\nNot so funny"
                        # intellijester.changeImage(val)
                        time.sleep(1)
                        joke_bag.change_score(next_cat, val)
                        break
                    except KeyError as e:
                        print str(e)
                        break
                    except JokeTooLong as e:
                        continue # Try again!
                    except UnicodeEncodeError as e:
                        print "<%s>" % j_text
                        continue # This was a bad string
                    except Exception as e:
                        print "Error:", type(e), e
                        break
    except:
        try:
            eeg.kill_process()
            killProgram()
        except:
            killProgram()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            usage()
            exit(0)

    global eeg
    # execute the main function now
    print "Initializing starting variables"
    eeg = EEG()
    joke_bag = JokeBag()
    # print "Finished initialization"


    my_threads = list()
    my_threads.append(threading.Thread(target=eeg.listen_to_process))
    my_threads.append(threading.Thread(target=main, args=(joke_bag,)))
    my_threads[0].daemon = True # run this thread in the background
    my_threads[1].daemon = False
    my_threads[0].start()
    my_threads[1].start()

    try:
        for t in my_threads:
            while t.isAlive():
                t.join(1)
    except:
        killProgram()
