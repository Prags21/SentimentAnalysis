# pylint: skip-file
import csv
import re
import pandas as pd

listOfTweets=[]

data = pd.read_csv("result.csv", na_values = ['no info', '.'])
keys=['User Name', 'Tweet Created At', 'Tweet Text', 'User Location', 'Retweet Count']
with open('preprocess.csv', 'a') as csvFile:
    dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
    dict_writer.writeheader()
    for tweets in data.iterrows():
        # convert to lower case
        tweet = tweets[1]['Tweet Text'].lower()
        # Convert www.* or https?://* to space
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
        # Convert @username to space
        tweet = re.sub('@[^\s]+','',tweet)
        # Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        # trim
        tweet = tweet.strip('\'"')
        # Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        dic_ = {
         'User Name': tweets[1]['User Name'],
         'Tweet Created At': tweets[1]['Tweet Created At'],
         'Tweet Text': tweet,
         'User Location': tweets[1]['User Location'],
         'Retweet Count': tweets[1]['Retweet Count'],
        }
        listOfTweets.append(dic_)
        # writing in csv
        dict_writer.writerow(dic_)