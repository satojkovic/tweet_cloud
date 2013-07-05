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
        self.num_tweets = 0

    def read_from_file(self, name):
        """
        read tweets from file
        """
        cr = csv.reader(open(name, 'r'), delimiter=',')
        for row in cr:
            tweet = row[-1]
            if self._is_exclude(tweet):
                continue
            self.text.append(tweet)
            self.num_tweets += 1

    def _is_exclude(self, tweet):
        if re.match('RT ', tweet) or re.match('"', tweet) or \
                re.match('http', tweet) or re.match('\[', tweet) or \
                re.match('bookmarked:', tweet) or re.match('ugomemo_bot:', tweet) or \
                re.match('FYI:', tweet) or re.match('Link:', tweet):
            return True
        else:
            return False

    def show(self):
        """
        show tweets
        """
        for t in self.text:
            print t

    def count_word(self):
        """
        count word in each tweets
        """
        pass

def main():
    args = docopt(__doc__, version="1.0")
    f = args['-f']

    tw = Tweets()
    tw.read_from_file(f)
    tw.show()

if __name__ == '__main__':
    main()
