import sys
import json
import os.path
from tokenizer import Tokenizer
from indexer import Indexer
from query import Query

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

    else:
        with open("index.json", 'r') as file:
            print("Detected saved Index ... Index Fetched!")
            index = json.load(file)
            indexer = Indexer(index["tfidf"],index["num_of_docs"])
            indexer.vectorize()

    print("Preparing for query ... ")

    with open(sys.argv[1] + "/bookkeeping.json", 'r') as file:
        bookkeeper = json.load(file)

    q = input("\nEnter search query (q to exit): ").lower()
    while q.lower() != 'q':
        query = Query(bookkeeper,indexer)
        documents = query.find_query(q)
        count = 0
        for docs in documents:
            if count < 20:
                count += 1
                print(str(count) +") " + "title:" + docs["title"] + " url: " + docs["url"] )
        q = input("\nEnter search query (q to exit): ").lower()

    print("Successfully exited!")

