## tweet_cloud

tweet_cloud is a command line tool to create a wordcloud from your twitter archive.

## Requirements

* MeCab
* docopt
* PIL
* numpy

## Usage

To view options, use the help flag.

    $ python tweet_cloud.py --help
    Usage: tweet_cloud.py [-f FILE]

    -f FILE    specify input file [default: tweets.csv]

A basic execution may look like this:

    $ python tweet_cloud.py

