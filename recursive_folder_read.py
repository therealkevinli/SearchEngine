import os
import sys


somethingElse = []
path = './WEBPAGES_RAW'
#code from https://stackoverflow.com/questions/2212643/python-recursive-folder-read
for root, subdirs, files in os.walk(path):

    for file in os.listdir(root):

        filePath = os.path.join(root, file)

        if os.path.isdir(filePath):
            pass

        else:
        	somethingElse.append(filePath)
            #f = open (filePath, 'r')
            # Do Stuff

print(len(somethingElse))