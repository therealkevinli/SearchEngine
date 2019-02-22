import json

json_dict = {}

def fetch_url(path):
    global json_dict
    if (len(json_dict) == 0):
        json_file = open("WEBPAGES_CLEAN/bookkeeping.json")
        json_dict = json.load(json_file)
        json_file.close()
        
    url = json_dict[path]
    return url
    

if __name__ == '__main__':
    while (True):
        try:
            path = input()
            if (path == "exit"):
                break
            url = fetch_url(path)
            print(url)
        except:
            print("Try again.")
