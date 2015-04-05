"""
Python class to store jokes according to categories
"""

import api

# Constants
LENGTH_THRESHOLD = 350
STARTING_COUNT = 10
STARTING_KEYS = ["sex", "criminal"]

# Custom exception thrown if joke is too lengthy
class JokeTooLong(Exception):
    def __init__(self, message):
        self.message = message

class JokeBag:
    def __init__(self):
        self.cat_map = { }

        # Populate the map with initial values
        for k in STARTING_KEYS:
            self.cat_map[k] = set()
            for cw in api.COMMON_ENG_WORDS[:4]:
                j_list = api.get_joke_type(k, STARTING_COUNT, cw)
                # print cw
                for j in j_list:
                    self.cat_map[k].add(j["joke"])
                    # print j["joke"][:80]
                    # count = count + 1
                # print count
            # print len(self.cat_map[k]), count, anticount

    def add_joke(self, joke):
        text = joke["joke"]
        cat = joke["category"]

        if len(text) > LENGTH_THRESHOLD:
            raise JokeTooLong("Length exceeds threshold")
        if cat not in self.cat_map:
            # This key is not already in here
            self.cat_map[cat] = set()
        # add the joke body to the set of jokes
        self.cat_map[cat].add(text)

    def retrieve_joke(self, cat):
        if cat not in self.cat_map or len(self.cat_map[cat]) == 0:
            # Asked for invalid joke category
            raise Exception("We don't have any room")
        else:
            return self.cat_map[cat].pop()

