from pymongo import MongoClient
import math
import pprint
import json

# setup connection to mongo and the search engine database
client = MongoClient() # mongodb://localhost:27017/
db = client.search_engine

# Retrieve the "index" collection (main collection)
index_collection = db.index

# Retrieve the "metainf" collection (used to store number of docs)
meta_collection = db.metainf

doc_count = 0
batch = {}

def insert_dict(tf_dict, doc_id):
    global doc_count
    global batch

    for t, freq in tf_dict.items():
        doc = {
            "DOCID" : doc_id, # "0/0"
            "TF" : freq,
            "IDF": 0.0,
            "TFIDF": 0.0
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
        for doc in struct["DOCS"]:
            tf = doc["TF"]
            idf = math.log(doc_count/nterm)
            tfidf = tf * idf
            doc["IDF"] = idf
            doc["TFIDF"] = tfidf
            # tag mult here

def send_batch():
    batch_list = list(batch.values())
    id_list = index_collection.insert_many(batch_list)

def match(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def search_query(query, limit):
    cond = []
    qtokens = query.split()
    sortBy = "DOCS.TFIDF"
    results = index_collection.find({"_id":{"$in":qtokens}}, {"DOCS.DOCID":1, "DOCS.TFIDF":1}).sort([(sortBy,-1)])
    for term in results:
        for doc in term["DOCS"]:
            # call book keeping
            cond.append(doc["DOCID"])

    cond = match(cond)
    i = 0
    for e in cond:
        if i >= limit:
            return 
        print(e)
        i += 1