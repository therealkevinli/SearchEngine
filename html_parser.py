import re
import operator
from collections import defaultdict
from html.parser import HTMLParser


class CleanHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.title_processed = False
        self.freq = defaultdict(list)
        self.tag = ""

    def handle_starttag(self, tag, attrs):
        self.tag = tag

    def handle_data(self, data):
        get
            


def parse_html(data):
    parser = CleanHTMLParser()
    parser.feed(data)
    parser.close()
    return 0

if __name__ == '__main__':
    while (True):
        try:
            docName = input()
            if (docName == 'exit'):
                break
            docName = "WEBPAGES_CLEAN/{}".format(docName)
            print(docName)
            data = open(docName).read()
            parse_html(data)
        except IndexError:
            print("Try again.")
