# pylint: skip-file
import csv
import re
from textblob import TextBlob
import pandas as pd

data = pd.read_csv("preprocess.csv", na_values = ['no info', '.'])
keys=['User Name','Tweet Created At','Tweet Text','User Location','Retweet Count','Polarity','Subjectivity']
with open('result_senti.csv', 'a') as csvFile:
    dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
    dict_writer.writeheader()
    for tweet in data.iterrows():
        i = tweet[0]
        te = data.loc[i, "Tweet Text"].decode('utf-8')
        blob = TextBlob(te)
        print(blob)
        dic_ = {
         'User Name': data.loc[i, "User Name"],
         'Tweet Created At': data.loc[i, "Tweet Created At"],
         'Tweet Text': data.loc[i, "Tweet Text"],
         'User Location': data.loc[i, "User Location"],
         'Retweet Count': data.loc[i, "Retweet Count"],
         'Polarity': blob.sentiment.polarity,
         'Subjectivity': blob.sentiment.subjectivity
        }
        dict_writer.writerow(dic_)
