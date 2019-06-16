from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import accuracy
from sklearn.ensemble import VotingClassifier
import pandas as pd


def models():
    names = ['Logistics Regression', 'SGD Classifier', 'SVC Linear', 'Naive Bayes', 'Decision Tree', 'KNeighbors'
        , 'Random Forest', 'Ada Boost', 'Bagging Classifier', 'Extra Tress Classifier']


    classfiers = [
        LogisticRegression(solver='liblinear', penalty='l1'),
        SGDClassifier(max_iter= 100),
        SVC(kernel='sigmoid', gamma=1.0),
        MultinomialNB(alpha=0.2),
        DecisionTreeClassifier(min_samples_split=7, random_state=111),
        KNeighborsClassifier(n_neighbors=49),
        RandomForestClassifier(n_estimators=31, random_state=111),
        AdaBoostClassifier(n_estimators=62, random_state=111),
        BaggingClassifier(n_estimators=9, random_state=111),
        ExtraTreesClassifier(n_estimators=9, random_state=111)
    ]

    models = zip(names, classfiers)
    return models

def performModellingSeparate(training, testing):
    for name, model in models():
        nltk_model = SklearnClassifier(model)
        nltk_model.train(training)
        test_accuracy_ = accuracy(nltk_model, testing) * 100
        train_accuracy_ = accuracy(nltk_model, training) * 100
        print('{} Accuracy Score Training : {} Testing = {} '.format(name, train_accuracy_, test_accuracy_))

def ensembling(training, testing):
    print('Ensembling====')
    nltk_ensemble = SklearnClassifier(VotingClassifier(estimators=list(models()), voting='hard', n_jobs=-1))
    nltk_ensemble.train(training)
    test_accuracy_ = accuracy(nltk_ensemble, testing) * 100
    train_accuracy_ = accuracy(nltk_ensemble, training) * 100
    print('ensembling : Accuracy Score Training : {} Testing = {} '.format(train_accuracy_, test_accuracy_))


def printClassficationReportConfusionMatrix(actual, predicted):
    print(classification_report(actual, predicted))

def printConfusionMatrix(actual, predicted, label1, label2):
    df = pd.DataFrame(
            confusion_matrix(actual, predicted),
            index= [['actual', 'actual'], [label1, label2]],
            columns= [['predicted', 'predicted'], [label1, label2]]
        )
    print(df)
