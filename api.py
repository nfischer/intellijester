#!/usr/bin/python

# In python already, with my x-mashape-key that has the unlimited queries, I believe

import unirest

def get_rand_joke():
    response = unirest.get("https://webknox-jokes.p.mashape.com/jokes/random", headers={"X-Mashape-Key": "Dv7dJmG74lmshSyC5z2CezBN0A1Xp1OpexHjsnJDI2yWrnmYhS", "Accept": "application/json"})

    if response.code != 200:
        # Request failed
        print response.code
        raise Exception("Request Failed")

    body = response.body

    return body

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
