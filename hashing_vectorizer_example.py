from sklearn.feature_extraction.text import HashingVectorizer

docs = ["John is agent in secret service organization",
        "Finch works for the machine which is independent organization",
        "Finch hired john to protect people",
        "people can be victim or perpetrator"]

hashingVectorizer = HashingVectorizer(n_features=20)

# To actually create the vectorizer, call fit on the text data
hashingVectorizer.fit(docs)

# To create a vector, we can do so by passing the text into the countVectorizer to get back counts
vector = hashingVectorizer.transform(docs)

# summarize encoded vector
print('Document vector: ')
print(list(vector.toarray()[0]))

# We could also do the whole thing at once with the fit_transform method:
print('Fit & Transform:')
vectorizer = HashingVectorizer(n_features=20)
print(vectorizer.fit_transform(docs).toarray())
