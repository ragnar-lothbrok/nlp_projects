# https://www.drivendata.org/competitions/54/machine-learning-with-a-heart/
# https://www.kaggle.com/ronitf/heart-disease-uci/downloads/heart.csv/1
# https://www.drivendata.org/competitions/54/machine-learning-with-a-heart/data/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import model_selection
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from ensemble_method import models

train_data = pd.read_csv("/Users/raghugup/Downloads/train_values.csv")
train_data = train_data.drop(columns = ['patient_id'])

test_data = pd.read_csv("/Users/raghugup/Downloads/test_values.csv")
patientIdDF = test_data['patient_id']
test_data = test_data.drop(columns = ['patient_id'])

train_labels = pd.read_csv("/Users/raghugup/Downloads/train_labels.csv")
train_labels = train_labels.drop(columns = ['patient_id'])

# print(train_data.head(4))

print(train_data.columns)

print(train_data.shape)

# print(test_data.head(4))

print(test_data.columns)

print(test_data.shape)

# print(train_labels.head(4))

print(train_labels.columns)

all_disease_data = train_data.append(test_data)

print(all_disease_data.shape)

# corr = train_data.corr()
# sns.heatmap(corr,
#             xticklabels=corr.columns.values,
#             yticklabels=corr.columns.values)
# plt.show()

print(all_disease_data.corr())

#Feature Engineering

train_data_with_label = train_data.join(train_labels['heart_disease_present'])

fig, axs = plt.subplots(ncols=train_data_with_label.columns.size -1)

columns = train_data.columns

# i = 0
# for column in columns:
#     sns.barplot(x=column, y='heart_disease_present', data=train_data_with_label, ax=axs[i])
#     i = i +1
#     plt.show()

for column in columns:
    print(all_disease_data[column].value_counts())
    print('distinct values = '+str(all_disease_data[column].unique().size))
    print('\n\n\n')

numeric_columns = all_disease_data._get_numeric_data().columns
print('Numerical Count = '+str(numeric_columns.size))
print(numeric_columns)

categorical_cols = list(set(all_disease_data.columns) - set(numeric_columns))
print('Categorical Count = ' + str(len(categorical_cols)))
print(categorical_cols)

all_disease_data["thal"] = all_disease_data["thal"].astype('category').cat.codes

train_test_data = all_disease_data[0:180]
submission_data = all_disease_data[180:]
print(train_test_data.shape)
print(submission_data.shape)

seed = 1
np.random.seed = seed

print(train_test_data.shape)
print(train_labels.shape)
X_train, X_test, y_train, y_test = model_selection.train_test_split(train_test_data ,train_labels , test_size = 0.25, random_state=seed, stratify = None)
model_accuracy = []
for name, estimator in models():
    estimator.fit(X_train, y_train)
    print('{} Predicting on train data : '.format(name))
    y_pred = estimator.predict(X_train)
    print(confusion_matrix(y_train, y_pred.round()))
    print(classification_report(y_train, y_pred.round()))
    train_accuracy_ = accuracy_score(y_train, y_pred.round()) * 100

    print('{} Predicting omn test data : '.format(name))
    y_pred = estimator.predict(X_test)
    print(confusion_matrix(y_test, y_pred.round()))
    print(classification_report(y_test, y_pred.round()))
    test_accuracy_ = accuracy_score(y_test, y_pred.round()) * 100
    model_accuracy.append('{} Accuracy Score Training : {} Testing = {} '.format(name, train_accuracy_, test_accuracy_))

    if name == 'RandomForest Regressor':
        submission_pred = estimator.predict(submission_data)
        result = pd.DataFrame(submission_pred, columns=['heart_disease_present'])
        finalDF = pd.DataFrame(patientIdDF, columns=['patient_id']).join(result)
        print(finalDF.shape)
        finalDF.heart_disease_present = finalDF.heart_disease_present.astype(float)
        finalDF.to_csv('/Users/raghugup/Downloads/submission_format.csv',index=False)




print('\n'.join(map(str, model_accuracy)))
