# dataset https://myleott.com/op-spam.html
import pandas as pd
import os
import numpy as np
import  nltk
from nltk.corpus import stopwords
dir = "/Users/raghugup/Downloads/drive-download-20190611T023257Z-001/"

stop_words = stopwords.words('english')
allreviews = []
target = []
# r=root, d=directories, f = files
for r, d, f in os.walk(dir):
    for file in f:
        if '.txt' in file:
            path = os.path.join(r, file)
            if "dec" in os.path.join(r, file):
                allreviews.append(open(path).read())
                target.append('d')
            elif "tru" in os.path.join(r, file):
                allreviews.append(open(path).read())
                target.append('t')

def preprocessing(reviews_df, exclude_stop_words):

    # lower case
    formattedDf = reviews_df[0].str.lower()

    # remove stop words
    if exclude_stop_words == 'true':
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

    print('formatted reviews data = {} '.format(formattedDf.head(10)))

    formattedDf = formattedDf.apply(lambda x: ' '.join(
        "/".join(word) for word in nltk.pos_tag(x.split()) ))

    print('formatted reviews data = {} '.format(formattedDf.head(10)))
    return formattedDf

def modelling(reviews_df, target):
    from sklearn.preprocessing import LabelEncoder
    # convert class labels to binary values, 0 = ham and 1 = spam
    encoder = LabelEncoder()
    df = pd.DataFrame(target)
    Y = encoder.fit_transform(df[0])
    print('Classes Count : ')
    print(df[0].value_counts())

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidfVectorizer = TfidfVectorizer(ngram_range=(1,1) , max_features=5000)
    vectorizer = tfidfVectorizer.fit_transform(reviews_df)
    dense = vectorizer.todense()
    df = pd.DataFrame(dense)
    df = pd.DataFrame(vectorizer.toarray(), columns = tfidfVectorizer.get_feature_names())

    #tfidf vectorizer
    from nltk import  word_tokenize
    seed = 1
    np.random.seed = seed
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    from ensemble_method import models
    model_accuracy = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(df, Y, test_size=0.25, random_state=seed)
    for name, estimator in models():
        estimator.fit(X_train, y_train)
        print('{} Predicting on train data : '.format(name))
        y_pred = estimator.predict(X_train)
        # print(confusion_matrix(y_train, y_pred))
        # print(classification_report(y_train, y_pred))
        train_accuracy_ = accuracy_score(y_train, y_pred) * 100

        print('{} Predicting omn test data : '.format(name))
        y_pred = estimator.predict(X_test)
        # print(confusion_matrix(y_test, y_pred))
        # print(classification_report(y_test, y_pred))
        test_accuracy_ = accuracy_score(y_test, y_pred) * 100
        model_accuracy.append('{} Accuracy Score Training : {} Testing = {} '.format(name, train_accuracy_, test_accuracy_))

    print('\n'.join(map(str, model_accuracy)))

with_stopwords = preprocessing(pd.DataFrame(allreviews), 'false')
without_stopwords = preprocessing(pd.DataFrame(allreviews), 'true')

print('without Stop words :')
modelling(without_stopwords, target)

print('with Stop words :')
modelling(with_stopwords, target)
