from sklearn.feature_extraction.text import TfidfVectorizer


# TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
#ln2 2.303 on base e
docs = ["John is agent in secret service organization",
        "Finch works for the machine which is independent organization",
        "Finch hired john to protect people",
        "people can be victim or perpetrator"]

tfidfVectorizer = TfidfVectorizer()

# To actually create the vectorizer, call fit on the text data
tfidfVectorizer.fit(docs)


# Inspect how our tfidfVectorizer vectorized the text. Print out a list of words used, and their index in the vectors
print('Vocabulary: ')
print(tfidfVectorizer.vocabulary_)

# To create a vector, we can do so by passing the text into the tfidfVectorizer to get back counts
vector = tfidfVectorizer.transform(docs)

# Our final vector:
print('Document vector: ')
print(vector.toarray())

# To get the vector for one word:
print('Secret vector: ')
print(tfidfVectorizer.transform(['secret']).toarray())

print('John vector: ')
print(tfidfVectorizer.transform(['John']).toarray())

# To get multiple vectors at once to build matrices
print('John and Finch: ')
print(tfidfVectorizer.transform(['John', 'Finch']).toarray())

# We could also do the whole thing at once with the fit_transform method:
print('Fit & Transform:')
vectorizer = TfidfVectorizer()
print(vectorizer.fit_transform(docs).toarray()[0])

# What's the length?
print('First Dataset (vectorized) length: ')
print(len(vectorizer.fit_transform(docs).toarray()[0]))

# Check words?
print('To the source:')
print(vectorizer.inverse_transform(vectorizer.fit_transform(docs).toarray()[0]))
print()
