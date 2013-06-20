#-*- conding: utf-8 -*-

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

def main():
    TEXT = "A tag cloud is a visual representation for text data, typically\
used to depict keyword metadata on websites, or to visualize free form text."

    tags = make_tags(get_tag_counts(TEXT), maxsize=80)

    create_tag_image(tags, 'cloud.png', size=(640, 480), fontname='Lobster')

    import webbrowser
    webbrowser.open('cloud.png')

if __name__ == '__main__':
    main()
