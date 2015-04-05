#!/usr/bin/python

# In python already, with my x-mashape-key that has the unlimited queries, I believe

import unirest          # requires a pip install
import os               # for URL path modification

# Constants
MASHAPE_KEY = "Dv7dJmG74lmshSyC5z2CezBN0A1Xp1OpexHjsnJDI2yWrnmYhS"
URL_BASE = "https://webknox-jokes.p.mashape.com/jokes"

COMMON_ENG_WORDS = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for"]

def get_rand_joke():
    url = os.path.join(URL_BASE, "random")
    response = unirest.get(url, headers={"X-Mashape-Key": MASHAPE_KEY, "Accept": "application/json"})
    if response.code != 200:
        # Request failed
        print response.code
        raise Exception("Request Failed")
    return response.body

def get_joke_type(cat, count, word):
    # These code snippets use an open-source library.
    url = os.path.join(URL_BASE, "search?category="+cat+"&keywords="+word+"&minRating=9&numJokes="+str(count) )
    response = unirest.get(url, headers={"X-Mashape-Key": MASHAPE_KEY, "Accept": "application/json"})
    if response.code != 200:
        # Request failed
        print response.code
        raise Exception("Request Failed")
    return response.body

def print_joke(j):
    if "title" in j:
        print j["title"]
        print "Title"

    print j["joke"]

# Call the api a few times. This is only for testing purposes, and should
# not be executed normally
if __name__ == "__main__":
    #for k in range(0, 8):
    joke = get_joke()
    print_joke(joke)
