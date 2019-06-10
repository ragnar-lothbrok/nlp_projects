from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def vectorizerAllData(newsgroups_data):
        # Create vectorizer
        vectorizer = CountVectorizer()

        # check dataset
        print('Total Datasets : ')
        print(newsgroups_data.data.__len__())

        print('First Dataset : ')
        print(newsgroups_data.data[0])


        arr = vectorizer.fit_transform(newsgroups_data.data).toarray()
        print(arr[0])

        # What's the length?
        print('First Dataset (vectorized) length: ')
        print(len(arr[0]))


        # How many words does it have?
        print('First Dataset  (vectorized) sum: ')
        print(np.sum(arr[0]))
        print()

        # Check words?
        print('To the source:')
        print(vectorizer.inverse_transform(arr[0]))
        print()


def vectorizerFilteredData(newsgroups_data):
        # Create vectorizer
        vectorizer = CountVectorizer()

        # check dataset
        print('Total Datasets : ')
        print(newsgroups_data.data.__len__())

        print('First Dataset : ')
        print(newsgroups_data.data[0])

        arr = vectorizer.fit_transform(newsgroups_data.data).toarray()
        print(arr[0])

        # What's the length?
        print('First Dataset (vectorized) length: ')
        print(len(arr[0]))

        # How many words does it have?
        print('First Dataset  (vectorized) sum: ')
        print(np.sum(arr[0]))
        print()

        # Check words?
        print('To the source:')
        print(vectorizer.inverse_transform(arr[0]))
        print()

vectorizerAllData(fetch_20newsgroups())

vectorizerFilteredData(fetch_20newsgroups(remove=('headers', 'footers', 'quotes')))
