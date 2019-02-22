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

def search_query(query, limit):
    cond = set()
    qtokens = query.split()
    sortBy = "DOCS.TFIDF"
    results = index_collection.find({"_id":{"$in":qtokens}}, {"DOCS.DOCID":1, "DOCS.TFIDF":1}).sort([(sortBy,-1)])
    for term in results:
        for doc in term["DOCS"]:
            # call book keeping
            cond.add(doc["DOCID"])
            # make this shit work right, sort it by TFIDF
    i = 0
    for e in cond:
        if i >= limit:
            return 
        print(e)
        i += 1

random1 = {
    "a" : 4,
    "b" : 4,
    "c" : 3,
    "d" : 2,
    "e" : 2,
    "f" : 1,
}

random2 = {
    "a" : 5,
    "b" : 1,
    "c" : 1,
    "d" : 2,
    "f" : 1,
}

random3 = {
    "a" : 5,
    "b" : 1,
    "c" : 1,
    "d" : 2,
    "f" : 1,
}

#insert_dict(random1, "0/0")
#insert_dict(random2, "0/1")
#insert_dict(random3, "0/3")
#calc_all_tfidf()
#send_batch()
l = search_query("a b e", 2)



# > db.index.find({TERM:'a'}, { TERM:1, DOCS.DOCID:1, DOCS.TFIDF:1})

# index = db.index_collection # used to insert an item in the db

# index_collection.insert_one(post)

# doc = index_collection.find_one({"term": "t"})