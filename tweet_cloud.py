#-*- coding: utf-8 -*-

"""Usage: tweet_cloud.py [-f FILE]

-f FILE    specify input file [default: tweets.csv]
"""

import MeCab
import csv
from docopt import docopt
import re
import os
from operator import itemgetter

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import numpy as np
from query_integral_image import query_integral_image

import random

class Tweets(object):
    def __init__(self):
        self.word_count = {}
        self.text = []
        self.num_tweets = 0
        self.FONT_PATH = "ipagp.ttf"
        self.font_encoding = "utf-8"

    def read_from_file(self, name):
        """
        read tweets from file(default: tweets.csv)
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
        for i in range(self.num_tweets):
            words = self.get_noun(self.text[i])
            for w in words:
                self.word_count[w] = self.word_count[w]+1 if w in self.word_count else 1

    def get_noun(self, text):
        """
        get noun
        """
        noun = []
        mc = MeCab.Tagger('-Ochasen')

        node = mc.parseToNode(text)
        while node:
            if node.feature.split(',')[1] == "固有名詞":
                replace_node = re.sub(re.compile("[!-/:-@[-`{-~(\d)]|([a-zA-Z])"), "", node.surface)
                if replace_node != "" and replace_node != " " and replace_node != "ー":
                    noun.append(replace_node)
            node = node.next
        
        return noun

    def show_word_count(self, is_reverse=False):
        for k, v in sorted(self.word_count.items(), key=lambda x:x[1], reverse=is_reverse):
            print k, v

    def make_tag_cloud(self, name="tweet_cloud.png", width=320, height=240):
        top_words = self.get_top_words()

        w = []
        c = []
        for k, v in sorted(top_words.items(), key=lambda x:x[1], reverse=True):
            w.append(k.decode('utf-8'))
            c.append(v)

        words = np.array(w)
        counts = np.array(c)

        self.make_wordcloud(words, counts, name)

    def get_top_words(self):
        i = 0
        top = 100
        top_words = {}

        for k, v in sorted(self.word_count.items(), key=lambda x:x[1], reverse=True):
            top_words[k] = v
            i += 1
            if i > top:
                break

        return top_words

    # from https://github.com/amueller/word_cloud/blob/master/wordcloud.py
    # Author: Andreas Christian Mueller <amueller@ais.uni-bonn.de>
    # (c) 2012
    #
    # License: MIT
    def make_wordcloud(self, words, counts, fname, font_path=None, width=400, height=200,
                       margin=5, ranks_only=False):
        """Build word cloud using word counts, store in image.

        Parameters
        ----------
        words : numpy array of strings
        Words that will be drawn in the image.

        counts : numpy array of word counts
        Word counts or weighting of words. Determines the size of the word in
        the final image.
        Will be normalized to lie between zero and one.

        font_path : string
        Font path to the font that will be used.
        Defaults to DroidSansMono path.

        fname : sting
        Output filename. Extension determins image type
        (written with PIL).

        width : int (default=400)
        Width of the word cloud image.

        height : int (default=200)
        Height of the word cloud image.

        ranks_only : boolean (default=False)
        Only use the rank of the words, not the actual counts.

        Notes
        -----
        Larger Images with make the code significantly slower.
        If you need a large image, you can try running the algorithm at a lower
        resolution and then drawing the result at the desired resolution.

        In the current form it actually just uses the rank of the counts,
        i.e. the relative differences don't matter.
        Play with setting the font_size in the main loop vor differnt styles.

        Colors are used completely at random. Currently the colors are sampled
        from HSV space with a fixed S and V.
        Adjusting the percentages at the very end gives differnt color ranges.
        Obviously you can also set all at random - haven't tried that.

        """
        if len(counts) <= 0:
            print("We need at least 1 word to plot a word cloud, got %d."
                  % len(counts))

        if font_path is None:
            font_path = self.FONT_PATH

        # normalize counts
        counts = counts / float(counts.max())
        # sort words by counts
        inds = np.argsort(counts)[::-1]
        counts = counts[inds]
        words = words[inds]
        # create image
        img_grey = Image.new("L", (width, height))
        draw = ImageDraw.Draw(img_grey)
        integral = np.zeros((height, width), dtype=np.uint32)
        img_array = np.asarray(img_grey)
        font_sizes, positions, orientations = [], [], []
        # intitiallize font size "large enough"
        font_size = 1000
        # start drawing grey image
        for word, count in zip(words, counts):
            # alternative way to set the font size
            if not ranks_only:
                font_size = min(font_size, int(100 * np.log(count + 100)))
            while True:
                # try to find a position
                font = ImageFont.truetype(font_path, font_size, encoding=self.font_encoding)
                # transpose font optionally
                orientation = random.choice([None, Image.ROTATE_90])
                transposed_font = ImageFont.TransposedFont(font,
                                                           orientation=orientation)
                draw.setfont(transposed_font)
                # get size of resulting text
                box_size = draw.textsize(word)
                # find possible places using integral image:
                result = query_integral_image(integral, box_size[1] + margin,
                                              box_size[0] + margin)
                if result is not None or font_size == 0:
                    break
                # if we didn't find a place, make font smaller
                font_size -= 1

            if font_size == 0:
                # we were unable to draw any more
                break

            x, y = np.array(result) + margin // 2
            # actually draw the text
            draw.text((y, x), word, fill="white", font = font)
            positions.append((x, y))
            orientations.append(orientation)
            font_sizes.append(font_size)
            # recompute integral image
            img_array = np.asarray(img_grey)
            # recompute bottom right
            # the order of the cumsum's is important for speed ?!
            partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),
                                         axis=0)
            # paste recomputed part into old image
            # if x or y is zero it is a bit annoying
            if x > 0:
                if y > 0:
                    partial_integral += (integral[x - 1, y:]
                                         - integral[x - 1, y - 1])
                else:
                    partial_integral += integral[x - 1, y:]
            if y > 0:
                partial_integral += integral[x:, y - 1][:, np.newaxis]

            integral[x:, y:] = partial_integral

        # redraw in color
        img = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(img)
        everything = zip(words, font_sizes, positions, orientations)
        for word, font_size, position, orientation in everything:
            font = ImageFont.truetype(font_path, font_size, encoding=self.font_encoding)
            # transpose font optionally
            transposed_font = ImageFont.TransposedFont(font,
                                                       orientation=orientation)
            draw.setfont(transposed_font)
            draw.text((position[1], position[0]), word,
                      fill="hsl(%d" % random.randint(0, 255) + ", 80%, 50%)", font = font)
        img.show()
        img.save(fname)

def main():
    args = docopt(__doc__, version="1.0")
    f = args['-f']

    tw = Tweets()
    tw.read_from_file(f)

    tw.count_word()
    tw.make_tag_cloud()

if __name__ == '__main__':
    main()
