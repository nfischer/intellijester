#!/usr/bin/python

"""
Commandline interface for intellijester

This file should only contain code for the command line interface. All code
necessary to base functionality should be in external files.
"""

import os
import sys
import api
from JokeBag import JokeBag, JokeTooLong
from eeg import EEG
import threading

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
    HELP_MSG="""
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

def main(joke_bag, eeg):
    try:
        prev_cat = ""
        while True:
            text = raw_input("\nPress enter to see a joke, q to quit: ")
            key_list = []
            key = ""
            if text != "":
                key_list = text.split()
                key = key_list[0]

            if matches(key,"quit") or key == "Q" or key == ";q" or key == "exit":
                os._exit(0)
            elif matches(key,"help") or key == "--help":
                usage()
            elif matches(key,"clear") or key == "cls":
                os.system('clear')
            elif matches(key,"keys"):
                print joke_bag.cat_map.keys()
            else:
                while True:
                    try:
                        j = api.get_rand_joke()
                        my_cat = j["category"]
                        joke_bag.add_joke(j)
                        next_cat = joke_bag.get_next_cat()
                        j_text = joke_bag.retrieve_joke(next_cat)
                        print j_text
                        # assume every joke goes over well
                        if prev_cat != "":
                            val = -1
                            if eeg.user_likes_joke():
                                print "He likes it!"
                                val = 1
                            else:
                                print "He doesn't like it"
                            joke_bag.change_score(prev_cat, val)
                        prev_cat = next_cat
                        break
                    except JokeTooLong as e:
                        continue # Try again!
                    except Exception as e:
                        print "Error:", e
    except:
        try:
            eeg.kill_process()
            os._exit(0)
        except:
            os._exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            usage()
            exit(0)

    # execute the main function now
    print "Initializing jokebag"
    joke_bag = JokeBag()
    eeg = EEG()
    print "Finished initialization"


    my_threads = list()
    my_threads.append(threading.Thread(target=eeg.listen_to_process) )
    my_threads.append(threading.Thread(target=main, args=(joke_bag, eeg,) ) )
    my_threads[0].daemon = True # run this thread in the background
    my_threads[1].daemon = False
    my_threads[0].start()
    my_threads[1].start()

    try:
        for t in my_threads:
            while t.isAlive():
                t.join(1)
    except:
        os._exit(0)
