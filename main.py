import html_parser
import sys
import os
import QueryDB
import create_postings_list

# will drop and load the DB from webpages_clean
def LoadDB():
    print("Loading database, this might take a while.")
    doc_list = create_postings_list.returnList 
    print("Dropping collection...")
    QueryDB.kill_collection()
    print("Tokenizing files...")
    for doc_id in doc_list:
        parser = html_parser.MyHTMLParser()
        file = open('./WEBPAGES_CLEAN/' + doc_id)
        for line in file:
            parser.line_num += 1
            feed = parser.feed(line)
        QueryDB.insert_dict(parser.term_dict, doc_id)
    print("Calculating TF-IDF's...")
    QueryDB.calc_all_tfidf()  
    print("Sending batch to database...")   
    QueryDB.send_batch()
    print("Completed!")

msg = "1 - LOAD DATABASE\n2 - SEARCH\n3 - METADATA\n4 - EXIT\n"

if __name__ == '__main__':
    while(1):
        us_in = input(msg + "> ")
        if us_in == '1':
            LoadDB()
        elif us_in == '2':
            qry = input("Query string> ")
            num = input("Number of results> ")
            QueryDB.search_query(qry, int(num))
        elif us_in == '3':
            QueryDB.getMeta()
        elif us_in == '4':
            sys.exit(0)
        else:
            print("Invalid Input!")