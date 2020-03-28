import math
import numpy as np


class Indexer:
    def __init__(self,tfidf={},num_of_docs=0):
        self.tfidf = tfidf
        self.num_of_docs = num_of_docs

        self.term_index = {}
        self.docs_index = {}
        self.vector = None

    def add(self,tokenList, docID, title, strong, headers):
        freq = dict()

        if len(tokenList) != 0:
            self.num_of_docs += 1
            for token in tokenList:
                if token in freq:
                        freq[token] +=1
                else:
                    freq[token] = 1

            for token in freq:
                tf = 1 + math.log10(freq[token])
                if token in title:
                    tf += 3
                if token in headers:
                    tf += 2
                if token in strong:
                    tf += 1

                if token not in self.tfidf:
                    self.tfidf[token] = {docID : tf}
                else:
                    self.tfidf[token][docID] = tf

    def vectorize(self):
        self.vector = np.zeros((len(self.tfidf),self.num_of_docs))

        term_index = 0
        doc_index = 0

        for term in self.tfidf:
            self.term_index[term] = term_index
            for docID in self.tfidf[term]:
                if docID not in self.docs_index:
                    self.docs_index[docID] = doc_index
                    self.vector[term_index, doc_index] = self.tfidf[term][docID]
                    doc_index += 1
                else:
                    self.vector[term_index, self.docs_index[docID]] = self.tfidf[term][docID]
            term_index += 1

    def calculate_Tfidf(self):
        for term in self.tfidf:
            for docID in self.tfidf[term]:
                self.tfidf[term][docID] *= math.log10(self.num_of_docs/len(self.tfidf[term]))







