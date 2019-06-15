import requests
from bs4 import BeautifulSoup

# page = requests.get("http://www.thebetterindia.com/102639/fight-right-to-education-anurag-kundu/")
# soup = BeautifulSoup(page.text)
# for tag in soup.findAll('a'):
#     print(tag['href'])
#     print(tag.get('href'))

# articles = []
# for tag in soup.findAll('p'):
#     if len(tag.get_text()) > 20 :
#         articles.append(tag.get_text())
#
# print(articles)

import re
re.ASCII
print(re.ASCII)

from nltk.corpus import wordnet as wn

dog = wn.synset('dog.n.01')

print(dog.hypernyms())



filename = '/Users/coder/Downloads/cleaning.txt'
file = open(filename)
text = file.read()
file.close()

words = text.split()
print(words[:100])

print('========REMOVE PUNCTUATION')
import string
table = str.maketrans('','',string.punctuation)
stripped = [word.translate(table) for word in words]
print(stripped[:100])

print('========REMOVE PUNCTUATION')
pun = list(string.punctuation)
strpped_alter = [word for word in words if word not in pun]
print(strpped_alter[:100])
print(string.punctuation)

print('========Lower Case')
lowerCased = [word.lower() for word in strpped_alter]
print(lowerCased[:100])

print('========SENTENCE TOKENIZE')
from nltk import sent_tokenize
sents = sent_tokenize(text)
print(sents[:10])

print('========WORD TOKENIZE')
from nltk import word_tokenize
words = word_tokenize(text)
print(words[:100])
filtered = [word for word in words if word.isalpha()]
print(filtered[:100])


print('========STOP WORDS')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
print(stop_words)

print('========REMOVE STOP WORDS')
filtered_stopwords = [word for word in lowerCased if word not in stop_words]
print(filtered_stopwords[:100])

print('========STemMING')
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stem_words = [stemmer.stem("automotive") for word in filtered_stopwords]
print(stem_words[:100])

print('========Lemmatzation')
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print("rocks :", lemmatizer.lemmatize("automotive"))
