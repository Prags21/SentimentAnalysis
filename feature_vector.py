# pylint: skip-file
import csv
import re
import pandas as pd
from textblob import TextBlob

listOfTweets=[]
data = pd.read_csv("result.csv", na_values = ['no info', '.'])
tweets = []
featureList = []


def getFeatureVector(tweet):
    featureVector = []
    # split tweet into words
    words = tweet.split()
    for w in words:
        # replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # ignore if it is a stop word
        if(val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector


def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def preprocessData(t):
    # Convert to lower case
    tweet = t.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet


for i in range(len(data)):
    tweet = data['Tweet Text'][i]
    processedTweet = preprocessData(tweet)
    featureVector = getFeatureVector(processedTweet)
    print(featureVector)
    featureList.extend(featureVector)
    for fv in featureVector:
        sentiments = TextBlob(fv).sentiment
        tweets.append((fv, sentiments))
        print(tweets)
        break

# Remove featureList duplicates
featureList = list(set(featureList))
print(featureList)


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features