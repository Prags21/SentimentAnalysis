# pylint: skip-file
import pandas as pd
import csv
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

table=pd.read_csv('cleanedDatasetE.csv',delimiter = ',')

list_wrd=[]
adjectives=[]
nouns=[]


for ind,item in table.iterrows():
    tagged = nltk.pos_tag(word_tokenize(item['Tweet Text']))
    for wrdA in tagged:
        if (wrdA[1] in ('JJ','JJR','JJS')):
            for wrdN in tagged:
                  if (wrdN[1] in ('NN','NNS')):
                        list_wrd.append((wrdA[0],wrdN[0]))

c=Counter(list_wrd).most_common(160)
print(c)
