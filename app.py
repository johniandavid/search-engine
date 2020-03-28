from flask import Flask, render_template, request, url_for
import sys
import json
import os.path
from tokenizer import Tokenizer
from indexer import Indexer
from query import Query

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])

def index():

    if request.method == 'POST':

        indexer = _prepareIndex()
        with open(sys.argv[1] + "/bookkeeping.json", 'r') as file:
            bookkeeper = json.load(file)

        query = Query(bookkeeper, indexer)
        q = request.form["query"]
        documents = query.find_query(q.lower())

        return render_template("index.html", documents=documents, length=len(documents))
    else:
        return render_template("index.html")

def _prepareIndex():

    with open("index.json", 'r') as file:
        print("Detected saved Index ... Index Fetched!")
        index = json.load(file)
        indexer = Indexer(index["tfidf"], index["num_of_docs"])
        indexer.vectorize()
        print("Preparing for query ... ")

    return indexer

if __name__ == "__main__":

    if not os.path.isfile("index.json"):
        tokenizer = Tokenizer()
        indexer = Indexer()

        num_of_docs = 0
        for subdir, dirs, files in os.walk(sys.argv[1]):
            for filename in files:
                filepath = subdir + os.sep + filename
                docID = filepath[13:]

                if docID != "bookkeeping.json" and docID != "bookkeeping.tsv":
                    try:
                        with open(filepath, 'r') as file:
                            tokens = tokenizer.tokenize(file)
                            indexer.add(tokens,docID,tokenizer.title,tokenizer.strong,tokenizer.headers)
                            num_of_docs += 1
                            print("Fetching Document {} ... Indexed: {}".format(docID, num_of_docs))
                    except Exception as e:
                        print(e)

        indexer.calculate_Tfidf()
        indexer.vectorize()
        print("Finished!")

        index = {"tfidf" : indexer.tfidf, "num_of_docs" : indexer.num_of_docs}
        print("Saving Index ....... ")

        with open('index.json', 'w') as i:
           json.dump(index, i, indent=4)
        print("Index Saved!")

        analytics = open("index_analytics.txt", "w")
        analytics.write("Number of documents in index: " + str(indexer.num_of_docs) + "\n")
        analytics.write("Number of [unique] words: " + str(len(indexer.tfidf)) + "\n")
        analytics.write("Total size of index: " + str(os.path.getsize("index.json") / 1000) + " KB" + "\n")
        analytics.close()

    app.run(debug=True)

