import os

from html.parser import HTMLParser
from collections import defaultdict
import queue


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.line_num = 0
        self.term_dict = defaultdict(tuple)
        self.tag_dict = defaultdict(bool)
        self.tag_weights = {"body": 1,"title": 10, "h1": 6,\
                            "h2": 5, "h3": 4, "b": 4, "strong": 4}
        self.tagStack = queue.LifoQueue()
        
    
    def handle_starttag(self, tag, attrs):
        self.tag_dict[tag] = True
        self.tagStack.put(tag)


    def handle_startendtag(self, attr)
        pass


    def handle_endtag(self, tag):
        self.tag_dict[tag] = False
        self.tagStack.get()


    def handle_data(self, data):
        token = "???"
        for tag in self.tagStack:
            self.term_dict[token][0] += 1
            self.term_dict[token][1] += self.tag_weights[tag]
            

        
            


os.chdir("C:/Users/Kevin/Documents/CompSci/CS121/Assignment3/")

parser = MyHTMLParser()

file = open('./index.html')

for line in file:
    parser.line_num += 1
    feed = parser.feed(line)
    
    
##parser.feed('<html><head><title>Test</title></head>'
##            '<body><h1>Parse me!</h1></body></html>')
