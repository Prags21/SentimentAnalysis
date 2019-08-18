# pylint: skip-file
import pandas as pd
import re
import warnings

pd.options.mode.chained_assignment = None
warnings.filterwarnings("ignore")

# %matplotlib inline

tweets = pd.read_csv('RawResult.csv',encoding = "utf-8")

# Preprocessing del RT @blablabla:
tweets['tweetos'] = ''
a= tweets['Tweet Text']

b = bytes(a, "utf-8").decode("unicode_escape") # python3

print(b)

# add tweetos first part
for i in range(len(tweets['Tweet Text'])):

    try:
        tweets['tweetos'][i] = tweets['Tweet Text'].str.split(' ')[i][0]
    except AttributeError:
        tweets['tweetos'][i] = 'other'

#Preprocessing tweetos. select tweetos contains 'RT @'
for i in range(len(tweets['Tweet Text'])):
    if tweets['tweetos'].str.contains('@')[i]  == False:
        tweets['tweetos'][i] = 'other'

# remove URLs, RTs, and twitter handles
for i in range(len(tweets['Tweet Text'])):
    tweets['Tweet Text'][i] = " ".join([word for word in tweets['Tweet Text'][i].split()
                                if 'http' not in word and '@' not in word and '<' not in word])



tweets['Tweet Text'] = tweets['Tweet Text'].apply(lambda x: re.sub('[!@#$:).;,?&]', '', x.lower()))
tweets['Tweet Text'] = tweets['Tweet Text'].apply(lambda x: re.sub('  ', ' ', x))
#print(tweets['Tweet Text'][1])