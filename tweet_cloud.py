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

def main():
    args = docopt(__doc__, version="1.0")

    f = args['-f']
    cr = csv.reader(open(f, 'r'), delimiter=',')
    for row in cr:
        tweet = row[-1]
        tweet_date = "YYYY-MM-DD HH:MM:SS"
        for r in row:
            s = re.search('((\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+))', r)
            if s is not None:
                tweet_date = s.group(1)

        print tweet_date, tweet

if __name__ == '__main__':
    main()
