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

def main():
    joke_bag = JokeBag()
    try:
        while 1:
            text = raw_input("\nPress enter to see a joke, q to quit: ")
            key_list = []
            key = ""
            if text != "":
                key_list = text.split()
                key = key_list[0]

            if matches(key,"quit") or key == "Q" or key == ";q" or key == "exit":
                exit(0)
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
                        j = joke_bag.retrieve_joke(my_cat)
                        # print_joke(j) # only if j is an object
                        print j
                        break
                    except JokeTooLong as e:
                        continue # Try again!
                    except Exception as e:
                        print str(e)
    except:
        exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            usage()
            exit(0)

    # execute the main function now
    main()
