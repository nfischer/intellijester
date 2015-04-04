#!/usr/bin/python

# Commandline interface for intellijester

import os
import sys
import api

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

class JokeBag:
    def __init__(self):
        self.cat_map = { }

    def add_joke(self, joke):
        text = joke["joke"]
        cat = joke["category"]

        if len(text) > 350:
            print "Joke too long!" # DEBUG
            return # This joke is too long
        if cat not in self.cat_map:
            # This key is not already in here
            self.cat_map[cat] = list()
        # append the joke body to the list of jokes
        # print type(self.cat_map)
        # print type(self.cat_map[cat])
        self.cat_map[cat].append(text)

    def retrieve_joke(self, cat):
        if cat not in self.cat_map or len(self.cat_map[cat]) == 0:
            # Asked for invalid joke category
            raise Exception("We don't have any room")
        else:
            return self.cat_map[cat].pop()

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
                try:
                    j = api.get_joke()
                    my_cat = j["category"]
                    joke_bag.add_joke(j)
                    j = joke_bag.retrieve_joke(my_cat)
                    # print_joke(j) # only if j is an object
                    print j
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
