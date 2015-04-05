"""
Python class to store jokes according to categories
"""

import api

# Constants
LENGTH_THRESHOLD = 250
STARTING_COUNT = 10         # This maxes at 10
STARTING_KEYS = ["sex", "chuck norris", "ethnic", "work"]
INITIAL_SCORE = 5
NUM_COMMON_WORDS = 1 # DEBUG, should be higher

# Custom exception thrown if joke is too lengthy
class JokeTooLong(Exception):
    def __init__(self, message):
        self.message = message


class JokeBag:
    def __init__(self):
        self.cat_map = { }
        self.score_map = { }

        # Populate the map with initial values
        for k in STARTING_KEYS:
            self.cat_map[k] = set()
            for cw in api.COMMON_ENG_WORDS[:NUM_COMMON_WORDS]:
                j_list = api.get_joke_type(k, STARTING_COUNT, cw)
                for j in j_list:
                    self.cat_map[k].add(j["joke"])

        for k in self.cat_map.keys():
            self.score_map[k] = INITIAL_SCORE # initialize all scores
            # print k

    ## This adds a single joke to the category
    ## @param joke: json dict object
    def add_joke(self, joke):
        text = joke["joke"]
        try:
            cat = joke["category"].lower()
        except:
            cat = "misc"

        if len(text) > LENGTH_THRESHOLD:
            raise JokeTooLong("Length exceeds threshold")
        if cat not in self.cat_map:
            # This key is not already in here
            self.cat_map[cat] = set()
            self.score_map[cat] = INITIAL_SCORE
        # add the joke body to the set of jokes
        self.cat_map[cat].add(text)

    ## This retuns a joke from the specified category
    ## @param cat: string
    def retrieve_joke(self, cat):
        if cat not in self.cat_map or len(self.cat_map[cat]) == 0:
            # Asked for invalid joke category
            raise Exception("We don't have any room")
        else:
            return self.cat_map[cat].pop()

    ## This is a comparison to sort keys based on their scores
    ## This enables highest scores to be sorted first, lowest scores last
    def score_comp(self, str1, str2):
        val1 = self.score_map[str1]
        val2 = self.score_map[str2]
        if val1 < val2:
            return 1
        elif val2 < val1:
            return -1
        else:
            return 0

    def get_joke_wrapper(self):
        j = api.get_rand_joke()
        self.add_joke(j)
        next_cat = self.get_next_cat()
        j_text = self.retrieve_joke(next_cat)
        return (next_cat, j_text)

    ## This returns the next joke category based on preference values and if
    ## jokes in that category are available
    ## @throws Exception if there are no available jokes
    def get_next_cat(self):
        # Go through every key that has a score, and pick the highest one
        sortedKeys = self.score_map.keys()
        sortedKeys.sort(cmp=self.score_comp)

        # Verify that all keys are lower case
        # for key in sortedKeys: # DEBUG
        #     if key != key.lower():
        #         print "hi", key, key.lower()

        # TODO: MACHINE LEARNING to select a *high* score but not necessarily the top score
        for key in sortedKeys:
            if len(self.cat_map[key]) > 0:
                return key

        raise Exception("No more jokes")

    ## Does not catch exceptions if the category passed in is invalid
    def change_score(self, cat, amt):
        self.score_map[cat] = self.score_map[cat] + amt # could be negative
        # print self.score_map[cat]

