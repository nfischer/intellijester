"""
Python class to store jokes according to categories
"""

# Constants
LENGTH_THRESHOLD = 350

# Custom exception thrown if joke is too lengthy
class JokeTooLong(Exception):
    def __init__(self, message):
        self.message = message

class JokeBag:
    def __init__(self):
        self.cat_map = { }

    def add_joke(self, joke):
        text = joke["joke"]
        cat = joke["category"]

        if len(text) > LENGTH_THRESHOLD:
            raise JokeTooLong("Length exceeds threshold")
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

