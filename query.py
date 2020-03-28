import math
import operator
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import numpy as np
from scipy.spatial.distance import cosine



class Query:
    def __init__(self, bookkeeper, indexer):
        self.bookkeeper = bookkeeper
        self.vector = indexer.vector
        self.tfidf = indexer.tfidf

        self.term_index = indexer.term_index
        self.docs_index = indexer.docs_index
        self.query = {}

    def parse(self,q):
        freq = {}

        for query in word_tokenize(q):
            if query in freq:
                freq[query] += 1
            else:
                freq[query] = 1

        for term in freq:
            if term in self.tfidf:
                self.query[term] = 1 + math.log10(freq[term]) * math.log10(len(self.docs_index) / len(self.tfidf[term]))
            else:
                self.query[term] = 0

    def find_query(self,q):
        results = {}
        docIDs = []
        self.parse(q)

        for term in self.query:
            if term in self.tfidf:
                count = 0
                for docID, score in sorted(self.tfidf[term].items(), key=operator.itemgetter(1),reverse=True):
                    if count < 50:
                        if docID not in docIDs:
                            count +=1
                            docIDs.append(docID)
        count = 0
        vec1 = np.array(self.vectorize())
        for docID in docIDs:
            count += 1
            print("Searching Index: {} %".format(str(round(count / len(docIDs) * 100, 2))))
            vec2 = self.vector[:, self.docs_index[docID]]
            results[docID] = 1 - cosine(vec1,vec2)

        count = 0
        documents = []

        for docID, score in sorted(results.items(), key=operator.itemgetter(1),reverse=True):
            if results[docID] != 0:
                if count < 20:
                    count += 1
                    documents.append(self.get_details(docID))
        return documents

    def get_details(self,docID):
        with open("WEBPAGES_RAW/" + docID, 'r') as file:
            soup = BeautifulSoup(file, 'lxml')

            if soup.find('title') != None:
                title = soup.find('title').string
            else:
                title = ""

            if soup.find('meta', attrs={'name': 'description'}) != None:
                description = soup.find('meta', attrs={'name': 'description'}).get("content")
            else:
                description = ""

        return {"docID" : docID, "url": self.bookkeeper[docID], "title" : title, "description": description}

    def vectorize(self):
        query_vector = np.zeros(len(self.term_index))

        for query in self.query:
            if query in self.term_index:
                query_vector[self.term_index[query]] = self.query[query]

        return query_vector









