from sklearn.feature_extraction.text import CountVectorizer

docs = ["John is agent in secret service organization",
        "Finch works for the machine which is independent organization",
        "Finch hired john to protect people",
        "people can be victim or perpetrator"]

countVectorizer = CountVectorizer()

# To actually create the vectorizer, call fit on the text data
countVectorizer.fit(docs)


# Inspect how our countVectorizer vectorized the text. Print out a list of words used, and their index in the vectors
print('Vocabulary: ')
print(countVectorizer.vocabulary_)

# To create a vector, we can do so by passing the text into the countVectorizer to get back counts
vector = countVectorizer.transform(docs)

# Our final vector:
print('Document vector: ')
print(vector.toarray())

# To get the vector for one word:
print('Secret vector: ')
print(countVectorizer.transform(['secret']).toarray())

print('John vector: ')
print(countVectorizer.transform(['John']).toarray())

# To get multiple vectors at once to build matrices
print('John and Finch: ')
print(countVectorizer.transform(['John', 'Finch']).toarray())

# We could also do the whole thing at once with the fit_transform method:
print('Fit & Transform:')
vectorizer = CountVectorizer()
print(vectorizer.fit_transform(docs).toarray())
