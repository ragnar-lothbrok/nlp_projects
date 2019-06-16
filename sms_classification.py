#https://archive.ics.uci.edu/ml/datasets/sms+spam+collection

import pandas as pd
import numpy as np
from ensemble_method import performModellingSeparate
from sklearn import model_selection

#load dataset using pandas
df = pd.read_table('/Users/raghugup/Downloads/smsspamcollection/SMSSpamCollection', header=None, encoding='utf-8')
print('num of records : {} '.format(len(df)))
print(df[1].head(10))


def preprocessing(smsDf):
    # remove stop words
    # lower case
    formattedDf = smsDf.str.lower()
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    formattedDf = formattedDf.apply(lambda x: ' '.join(
        word for word in x.split() if word not in stop_words))

    # Remove punctuation
    formattedDf = formattedDf.str.replace(r'[^\w\d\s]', ' ')

    # Replace whitespace between terms with a single space
    formattedDf = formattedDf.str.replace(r'\s+', ' ')

    # Remove leading and trailing whitespace
    formattedDf = formattedDf.str.replace(r'^\s+|\s+?$', '')

    formattedDf = formattedDf.apply(lambda x: ' '.join(
        word for word in x.split() if word.isalpha()))

    print('formatted sms data = {} '.format(formattedDf.head(10)))

    # Stemming
    from nltk import PorterStemmer
    stemmer = PorterStemmer()
    formattedDf = formattedDf.apply(lambda x: ' '.join(
        stemmer.stem(term) for term in x.split()))

    #lemmatization
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    formattedDf = formattedDf.apply(lambda x: ' '.join(
        lemmatizer.lemmatize(word, pos ="a") for word in x.split()))

    print('formatted lemmatized sms data = {} \n'.format(formattedDf.head(10)))

    formattedDf = formattedDf.apply(lambda x: ' '.join(
        word for word in x.split() if word not in stop_words))

    return formattedDf


import nltk
allWords = []
formattedDF = preprocessing(df[1]);

#Feature generation using CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer().fit(formattedDF)
#index of words
bag_of_words = vec.transform(formattedDF)
sum_words = bag_of_words.sum(axis=0)
print('Sum of words {}'.format(len(vec.vocabulary_.items())))
words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
words_freq = sorted(words_freq, key = lambda x: x[1], reverse = True)
print('Most common words: {}'.format(words_freq[:15]))


vector = vec.transform(formattedDF)

wordsInVectorizer = []
for tuple in list(vec.vocabulary_.items()):
    wordsInVectorizer.append(tuple[0])

#Feature generation manually
for sms in formattedDF:
    for word in sms.split():
        if len(word) > 1:
            allWords.append(word)

wordDist = nltk.FreqDist(allWords)
# print the total number of words and the 15 most common words
print('Number of words: {}'.format(len(wordDist)))
print('Most common words: {}'.format(wordDist.most_common(15)))
# use the 1500 most common words as features
word_features = list(wordDist.keys())[:1500]


from sklearn.preprocessing import LabelEncoder
# convert class labels to binary values, 0 = ham and 1 = spam
encoder = LabelEncoder()
Y = encoder.fit_transform(df[0])
print('Classes Count : ')
print(df[0].value_counts())

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfVectorizer = TfidfVectorizer(ngram_range=(1,1) , max_features=5000 , vocabulary= wordsInVectorizer)
vectorizer = tfidfVectorizer.fit_transform(formattedDF)
dense = vectorizer.todense()
df = pd.DataFrame(dense)
df = pd.DataFrame(vectorizer.toarray(), columns = tfidfVectorizer.get_feature_names())

#Count Vectorizer
from nltk import  word_tokenize
seed = 1
np.random.seed = seed
def find_features(message):
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = (word in words)
    return features
featuresets = [(find_features(text), label) for (text, label) in zip(formattedDF,Y)]
training, testing = model_selection.train_test_split(featuresets, test_size = 0.25, random_state=seed)
print(len(training))
print(len(testing))


from ensemble_method import performModellingSeparate
performModellingSeparate(training, testing)


from ensemble_method import ensembling
ensembling(training, testing)


#tfidf vectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from ensemble_method import models
model_accuracy = []
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df, Y, test_size=0.25, random_state=seed)
for name, estimator in models():
    estimator.fit(X_train, y_train)
    print('Predicting on train data : ')
    y_pred = estimator.predict(X_train)
    print(confusion_matrix(y_train, y_pred))
    print(classification_report(y_train, y_pred))
    train_accuracy_ = accuracy_score(y_train, y_pred)

    print('Predicting omn test data : ')
    y_pred = estimator.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    test_accuracy_ = accuracy_score(y_test, y_pred)
    model_accuracy.append('{} Accuracy Score Training : {} Testing = {} '.format(name, train_accuracy_, test_accuracy_))

print('\n'.join(map(str, model_accuracy)))
