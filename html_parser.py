import os

from html.parser import HTMLParser
from collections import defaultdict
from nltk.stem import PorterStemmer #for the stemmer

stopwords = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.line_num = 0
        self.term_dict = defaultdict(lambda: (0,0))
        self.tag_dict = defaultdict(bool)
        self.tag_weights = {"body": 1,"title": 10, "h1": 6,\
                            "h2": 5, "h3": 4, "b": 4, "strong": 4}
        self.tagStack = ['title']
        
    
    def handle_starttag(self, tag, attrs):
        if len(self.tagStack) > 0 and self.tagStack[0] == 'title':
            self.tagStack.pop()
        self.tagStack.append(tag)


    def handle_endtag(self, tag):
        if (self.tagStack[-1] == '\\'+tag):
            self.tagStack.pop()


    def handle_data(self, data):
        tokens = "".join((char if char.isalnum() else " ") for char in data).split()
        # Lowercase all tokens
        # tokens = [token.lower() for token in tokens]
        ps = PorterStemmer() #Porter Stemmer object
        #removing all stop words; applies stemming; lowercases everything
        tokens = [ps.stem(token.lower()) for token in tokens if token.lower() not in stopwords]
        
        for token in tokens:
            #countDict[word] += 1    
            for tag in self.tagStack:
                if tag in self.tag_weights.keys():
                    freq, weighted_total = self.term_dict[token]
                    self.term_dict[token] = (freq + 1, weighted_total\
                                             + self.tag_weights[tag])
