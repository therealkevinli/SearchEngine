import os

from html.parser import HTMLParser
from collections import defaultdict


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.line_num = 0
        self.term_dict = defaultdict(lambda: (0,0))
        self.tag_dict = defaultdict(bool)
        self.tag_weights = {"body": 1,"title": 10, "h1": 6,\
                            "h2": 5, "h3": 4, "b": 4, "strong": 4}
        self.tagStack = []
        
    
    def handle_starttag(self, tag, attrs):
        self.tagStack.append(tag)


    def handle_endtag(self, tag):
        if (self.tagStack[-1] == '\\'+tag):
            self.tagStack.pop()


    def handle_data(self, data):
        tokens = "".join((char if char.isalnum() else " ") for char in line).split()
        # Lowercase all tokens
        tokens = [token.lower() for token in tokens]

        for token in tokens:
            #countDict[word] += 1    
            for tag in self.tagStack:
                if tag in self.tag_weights.keys():
                    freq, weighted_total = self.term_dict[token]
                    self.term_dict[token] = (freq + 1, weighted_total\
                                             + self.tag_weights[tag])


if __name__ == '__main__':
    os.chdir("C:/Users/Kevin/Documents/CompSci/CS121/Assignment3/")

    parser = MyHTMLParser()

    file = open('tryThis.html')

    for line in file:
        parser.line_num += 1
        feed = parser.feed(line)

    print(parser.term_dict)
    ##parser.feed('<html><head><title>Test</title></head>'
    ##            '<body><h1>Parse me!</h1></body></html>')
