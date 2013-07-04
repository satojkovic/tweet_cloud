#-*- coding: utf-8 -*-

"""Usage: tweet_cloud.py [-f FILE]

-f FILE    specify input file [default: tweets.csv]
"""

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

import MeCab
import csv
from docopt import docopt
import re

class Tweets(object):
    def __init__(self):
        self.text = []

    def read_from_file(self, name):
        """
        read tweets from file
        """
        cr = csv.reader(open(name, 'r'), delimiter=',')
        for row in cr:
            tweet = row[-1]
            self.text.append(tweet)

    def show(self):
        """
        show tweets
        """
        for t in self.text:
            print t

def main():
    args = docopt(__doc__, version="1.0")
    f = args['-f']

    tw = Tweets()
    tw.read_from_file(f)
    tw.show()

if __name__ == '__main__':
    main()
