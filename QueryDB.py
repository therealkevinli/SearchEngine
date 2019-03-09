from pymongo import MongoClient
import math
import pprint
import json
import create_postings_list
import os
import sys
import operator
from nltk.stem import PorterStemmer #for the stemmer

stopwords = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
champ_thresh = 5.0

# setup connection to mongo and the search engine database
client = MongoClient() # mongodb://localhost:27017/
db = client.search_engine

# Retrieve the "index" collection (main collection)
index_collection = db.index

# Retrieve the "metainf" collection (used to store number of docs)
meta_collection = db.metainf

doc_count = 0
batch = {}

os.chdir("/home/georgio/workspace/121/search-engine/WEBPAGES_CLEAN")
json_dict = create_postings_list.json_dict
def insert_dict(tf_dict, doc_id):
    global doc_count
    global batch

    for t, freq in tf_dict.items():
        doc = {
            "DOCID" : doc_id, # "0/0"
            "TF" : freq[0],
            "IDF": 0.0,
            "TFIDF": 0.0,
            "TAGRANK": freq[1]
        } 
        if t in batch:
            batch[t]["DOCS"].append(doc)
        else:
            batch[t] = {
                "_id" : t,
                "DOCS" : [] # list of doc's
            }
            batch[t]["DOCS"].append(doc)
    doc_count += 1  

def calc_all_tfidf():
    global batch
    for term, struct in batch.items():
        nterm = len(struct["DOCS"])
        index = 0
        for doc in struct["DOCS"]:
            tf = doc["TF"]
            idf = math.log(doc_count/nterm)
            tfidf = tf * idf
            doc["IDF"] = idf
            doc["TFIDF"] = tfidf

            # remove values below champions threshold
            if tfidf < champ_thresh:
                del batch[term]["DOCS"][index]

            index += 1


def send_batch():
    batch_list = list(batch.values())
    id_list = index_collection.insert_many(batch_list)

def match(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def kill_collection():
    index_collection.remove({})

def search_query(query, limit): # add a new func here 
    if len(query) == 0:
        return []
    ps = PorterStemmer() #Porter Stemmer object    
    query = query.lower()
    doc_rank = {} # dictionary that will hold document rankings
    qtokens = query.split()
    qtokens = [ps.stem(token) for token in qtokens if token not in stopwords] # stems the query tokens
    sortBy = "DOCS.TFIDF"
    results = index_collection.find({"_id":{"$in":qtokens}}, {"DOCS.DOCID":1, "DOCS.TFIDF":1, "DOCS.TAGRANK":1})#.sort([(sortBy,-1)])

    for term in results:
        for doc in term["DOCS"]:
            doc_id = doc["DOCID"]
            doc_tfidf = doc["TFIDF"]
            doc_tagrank = doc["TAGRANK"]

            # Stored sum of tfidf in dictionary ranks urls
            if doc_id in doc_rank:
                doc_rank[doc_id] += doc_tfidf + doc_tagrank
            else:
                doc_rank[doc_id] = doc_tfidf + doc_tagrank

    # sort by largest sum
    url_list = sorted(doc_rank.items(), key=operator.itemgetter(1), reverse=True)
    # url_list = [(json_dict[url[0]],url[1]) for url in url_list]
    url_list = [(json_dict[url[0]], url[1], url[0]) for url in url_list]
    pprint.pprint(url_list[:limit])
    return url_list[:limit]

def getMeta():
    # print("# of unique terms: {}".format(len(batch)))
    # print("Size of index: {}Kb".format(index_collection.(scale=1024)))
    results = db.command("dbstats")
    print("Number of unique terms: {}".format(results["objects"]))
    print("Index size: {}Kb".format(int(results["indexSize"])/1024))