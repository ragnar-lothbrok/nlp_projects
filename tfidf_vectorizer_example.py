from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer


# TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
#ln2 2.303 on base e

def vectorizerAllData(newsgroups_data):
        # Create vectorizer
        vectorizer = TfidfVectorizer()

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

        # Check words?
        print('To the source:')
        print(vectorizer.inverse_transform(arr[0]))
        print()


def vectorizerFilteredData(newsgroups_data):
        # Create vectorizer
        vectorizer = TfidfVectorizer()

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

        # Check words?
        print('To the source:')
        print(vectorizer.inverse_transform(arr[0]))
        print()

vectorizerAllData(fetch_20newsgroups())

vectorizerFilteredData(fetch_20newsgroups(remove=('headers', 'footers', 'quotes')))
