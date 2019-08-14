# pylint: skip-file
import matplotlib
import re

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
from random import randint
warnings.filterwarnings("ignore")

#df = pd.DataFrame({'number':['123','234','345'],'contactnumber':['234','345','123'],'callduration':[1,2,4]})
df = pd.read_csv('/content/r.csv', encoding = "ISO-8859-1")
listOfTweets=[]
d = {}

G = nx.DiGraph()
def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [ source.strip()
             for tuple in rt_patterns.findall(tweet)
                 for source in tuple
                     if source not in ("RT", "via") ]
for tweet in df.iterrows():
    #print(df['Tweet Text'])
    t=str(tweet[1]['Tweet Text'])
    rt_sources = get_rt_sources(t)
    if not rt_sources: continue
    for rt_source in rt_sources:
        #print(tweet[1]['Screen Name'])
        dict_={'RT':rt_source,
              'user':tweet[1]['Screen Name'],
              'RT_Count':tweet[1]['Retweet Count']}
        G.add_edges_from([(rt_source,tweet[1]['Screen Name'])], weight=tweet[1]['Retweet Count'])
        d[rt_source]="Influencer"
        d[tweet[1]['Screen Name']]="U"

        listOfTweets.append(dict_)
df1 = pd.DataFrame(listOfTweets)
print(d)
#G = nx.from_pandas_edgelist(df1,'RT','user')
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 50)
nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
nx.draw_networkx_labels(G, pos, labels=d, ax=ax)

plt.show()