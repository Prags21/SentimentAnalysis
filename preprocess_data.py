# pylint: skip-file
import csv
import re
import pandas as pd
#from textblob import TextBlob
listOfTweets=[]

data = pd.read_csv("RawResult.csv", encoding = "utf-8")
keys=['User Name', 'Tweet Created At', 'Tweet Text', 'User Location', 'Retweet Count','Polarity','Subjectivity']
with open('preprocess.csv', 'a') as csvFile:
    dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
    dict_writer.writeheader()
    for tweets in data.iterrows():
        # convert to lower case
        tweet = tweets[1]['Tweet Text'].str().lower()
        # Convert www.* or https?://* to space
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
        print(tweet)
        break
        # Convert @username to space
        tweet = re.sub('@[^\s]+','',tweet)
        # Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        # trim
        tweet = tweet.strip('\'"')
        # Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #blob = TextBlob(tweet.decode('utf-8'))
        #print(blob.sentiment.polarity)
        # dic_ = {
        #  'User Name': tweets[1]['User Name'],
        #  'Tweet Created At': tweets[1]['Tweet Created At'],
        #  'Tweet Text': tweet,
        #  'User Location': tweets[1]['User Location'],
        #  'Retweet Count': tweets[1]['Retweet Count'],
        #  'Polarity': blob.sentiment.polarity,
        #  'Subjectivity': blob.sentiment.subjectivity
        # }
        # listOfTweets.append(dic_)
        # writing in csv
        # dict_writer.writerow(dic_)
        print(tweet)