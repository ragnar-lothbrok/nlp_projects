from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import  pandas as pd

# TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
#ln2 2.303 on base e
docs = ["John is agent in secret service organization",
        "Finch works for the machine which is independent organization",
        "Finch hired john to protect people",
        "people can be victim or perpetrator"]


countVectorizer = CountVectorizer()
fitVectorizer = countVectorizer.fit_transform(docs)

print(fitVectorizer.shape)

#rows and columns
tfidfTransformer = TfidfTransformer(smooth_idf=True,use_idf=True)

# To actually create the vectorizer, call fit on the text data
tfidfTransformer.fit(fitVectorizer)

# print idf values
df_idf = pd.DataFrame(tfidfTransformer.idf_, index=countVectorizer.get_feature_names(), columns=["tf_idf_weights"])

# sort ascending
df_idf.sort_values(by=['tf_idf_weights'])

print(df_idf)

# count matrix
count_vector = countVectorizer.transform(docs)
# tf-idf scores
tf_idf_vector = tfidfTransformer.transform(count_vector)

feature_names = countVectorizer.get_feature_names()

# get tfidf vector for first document
first_document_vector = tf_idf_vector[0]

# print the scores
df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
df.sort_values(by=["tfidf"], ascending=False)
print(df)
