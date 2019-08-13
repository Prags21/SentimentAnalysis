# pylint: skip-file
import csv
import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")

tweets = pd.read_csv('tweets_all.csv', encoding = "ISO-8859-1")
# Preprocessing del RT @blablabla:
tweets['tweetos'] = ''
tweets['clean text'] = ''

headers = [
    'text',	'in_reply_to_screen_name',	'created_at',	'listed_count',
    'location',	'description',	'user_created_at',
    'statuses_count',	'followers_count',	'name',	'time_zone',
    'user_lang',	'friends_count',	'screen_name',	'country_code',
    'country',	'place_type',	'full_name', 'tweetos', 'clean text']

# add tweetos first part
for i in range(len(tweets['text'])):
    try:
        tweets['tweetos'][i] = tweets['text'].str.split(' ')[i][0].encode('utf-8')
    except AttributeError:
        tweets['tweetos'][i] = 'other'.encode('utf-8')
# Preprocessing tweetos. select tweetos contains 'RT @'
for i in range(len(tweets['text'])):
    if tweets['tweetos'].str.contains('@')[i] == False:
        tweets['tweetos'][i] = 'other'.encode('utf-8')
# remove URLs, RTs, and twitter handles
for i in range(len(tweets['text'])):
    tweets['text'][i] = " ".join([word for word in tweets['text'][i].split()
                                if 'http' not in word and '@' not in word and '<' not in word])

tweets['text'] = tweets['text'].apply(lambda x: re.sub('[!@#$:).;,?&]', '', x.lower()))
tweets['text'] = tweets['text'].apply(lambda x: re.sub('  ', ' ', x))
print(tweets['text'][1])
# with open('res.csv', 'a') as csvFile:
# dict_writer = csv.DictWriter(csvFile)
# dict_writer.writeheader()
for i in range(len(tweets['text'])):

    tweets['clean text'][i] = tweets['text'][i]

tweets.to_csv('output.csv', columns = headers, encoding='utf-8')