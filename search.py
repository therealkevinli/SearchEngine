from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import QueryDB

app = Flask(__name__)
CORS(app)

@app.route("/api/search", methods=['POST'])
def query_the_search():
    try:
        data = request.data
        dataDict = json.loads(data)
        query = dataDict['query']
        print( query )
        results = QueryDB.search_query(query, 50)
        results = [result[0] for result in results]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'message' : 'error reading query'}), 500

if __name__ == '__main__':
    app.run()