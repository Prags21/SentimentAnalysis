
from tqdm import tqdm
%matplotlib inline
#Module to handle regular expressions
import re
#manage files
import os
#Library for emoji
import emoji
#Import pandas and numpy to handle data
import pandas as pd
import numpy as np

#import libraries for visualization
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image

#Import nltk to check english lexicon
import nltk
from nltk.tokenize import word_tokenize

from nltk.corpus import (
    wordnet,
    stopwords
)

#import libraries for tokenization and ML
import json
import keras
import keras.preprocessing.text as kpt
#from keras.preprocessing.text import Tokenizer;

import sklearn
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfVectorizer
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#Import all libraries for creating a deep neural network
#Sequential is the standard type of neural network with stackable layers
from keras.models import (
    Sequential,
    model_from_json
)
#Dense: Standard layers with every node connected, dropout: avoids overfitting
from keras.layers import Dense, Dropout, Activation
table=pd.read_csv('Dataset.csv', delimiter = ',',encoding = "utf-8")
#preprocess text in tweets by removing links, @UserNames, blank spaces, etc.
def preprocessing_text(table):
    #put everythin in lowercase
    table['Tweet Text'] = table['Tweet Text'].str.lower()

    for ind,item in enumerate(table['Tweet Text']):
        table.at[ind,'Tweet Text']= bytes(item, "utf-8").decode("unicode_escape")

    #Replace rt indicating that was a retweet
    table['Tweet Text'] = table['Tweet Text'].str.replace('rt', '')
    #Replace occurences of mentioning @UserNames
    table['Tweet Text'] = table['Tweet Text'].replace(r'@\w+', '', regex=True)
    #Replace links contained in the tweet
    table['Tweet Text'] = table['Tweet Text'].replace(r'http\S+', '', regex=True)
    table['Tweet Text'] = table['Tweet Text'].replace(r'www.[^ ]+', '', regex=True)
    #remove numbers
    table['Tweet Text'] = table['Tweet Text'].replace(r'[0-9]+', '', regex=True)
    #replace special characters and puntuation marks
    table['Tweet Text'] = table['Tweet Text'].replace(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', regex=True)
    return table

#Replace elongated words by identifying those repeated characters and then remove them and compare the new word with the english lexicon
def in_dict(word):
    if wordnet.synsets(word):
        #if the word is in the dictionary, we'll return True
        return True

def replace_elongated_word(word):
    regex = r'(\w*)(\w+)\2(\w*)'
    repl = r'\1\2\3'
    if in_dict(word):
        return word
    new_word = re.sub(regex, repl, word)
    if new_word != word:
        return replace_elongated_word(new_word)
    else:
        return new_word

def detect_elongated_words(row):
    regexrep = r'(\w*)(\w+)(\2)(\w*)'
    words = [''.join(i) for i in re.findall(regexrep, row)]
    for word in words:
        if not in_dict(word):
            row = re.sub(word, replace_elongated_word(word), row)
    return row
def stop_words(table):
    #We need to remove the stop words
    stop_words_list = stopwords.words('english')
    table['Tweet Text'] = table['Tweet Text'].str.lower()
    table['Tweet Text'] = table['Tweet Text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words_list)]))
    return table
def replace_antonyms(word):
    #We get all the lemma for the word
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            #if the lemma is an antonyms of the word
            if lemma.antonyms():
                #we return the antonym
                return lemma.antonyms()[0].name()
    return word

def handling_negation(row):
    #Tokenize the row
    words = word_tokenize(row)
    speach_tags = ['JJ', 'JJR', 'JJS', 'NN', 'VB', 'VBD', 'VBG', 'VBN', 'VBP']
    #We obtain the type of words that we have in the text, we use the pos_tag function
    tags = nltk.pos_tag(words)
    #Now we ask if we found a negation in the words
    tags_2 = ''
    if "n't" in words and "not" in words:
        tags_2 = tags[min(words.index("n't"), words.index("not")):]
        words_2 = words[min(words.index("n't"), words.index("not")):]
        words = words[:(min(words.index("n't"), words.index("not")))+1]
    elif "n't" in words:
        tags_2 = tags[words.index("n't"):]
        words_2 = words[words.index("n't"):]
        words = words[:words.index("n't")+1]
    elif "not" in words:
        tags_2 = tags[words.index("not"):]
        words_2 = words[words.index("not"):]
        words = words[:words.index("not")+1]

    for index, word_tag in enumerate(tags_2):
        if word_tag[1] in speach_tags:
            words = words+[replace_antonyms(word_tag[0])]+words_2[index+2:]
            break

    return ' '.join(words)
def cleaning_table(table):
    #This function will process all the required cleaning for the text in our tweets
    table = preprocessing_text(table)
    table['Tweet Text'] = table['Tweet Text'].apply(lambda x: detect_elongated_words(x))
    table['Tweet Text'] = table['Tweet Text'].apply(lambda x: handling_negation(x))
    table = stop_words(table)
    return table


def word_cloud(tweets):

    #We get the directory that we are working on
    file = os.getcwd()
    #We read the mask image into a numpy array
    #Now we store the tweets into a series to be able to process
    #tweets_list = pd.Series([t for t in tweet_table.tweet]).str.cat(sep=' ')
    #We generate the wordcloud using the series created and the mask
    word_cloud = WordCloud(width=2000, height=1000, max_font_size=200, background_color="black", max_words=2000, contour_width=1,
                           contour_color="steelblue", colormap="nipy_spectral", stopwords=["sometimes","old","make","new","data","data old","data new",
                                                                                           "aificial","via","ht","aificial inteligence",
                                                                                           "aificialinteligence","get pregnant","pregnant get","pregnant",
                                                                                           "old data","it's","b'"])
    word_cloud.generate(tweets)

    #wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(tweets_list)

    #Now we plot both figures, the wordcloud and the mask
    plt.figure(figsize=(15,15))
    #plt.figure(figsize=(10,10))
    plt.imshow(word_cloud, interpolation="hermite")
    plt.axis("off")
    #plt.imshow(avengers_mask, cmap=plt.cm.gray, interpolation="bilinear")
    #plt.axis("off")
    plt.show()

  table=cleaning_table(table)
  #print(table['Tweet Text'])
  word_cloud(pd.Series([t for t in table['Tweet Text']]).str.cat(sep=' '))