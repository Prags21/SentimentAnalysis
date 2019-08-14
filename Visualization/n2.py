# pylint: skip-file
import matplotlib
import re

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

#df = pd.DataFrame({'number':['123','234','345'],'contactnumber':['234','345','123'],'callduration':[1,2,4]})
df = pd.read_csv('/content/result (6).csv', encoding = "ISO-8859-1")
listOfTweets=[]

G = None
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
        #print(dict_)

        listOfTweets.append(dict_)
df1 = pd.DataFrame(listOfTweets)
#print(listOfTweets)
G = nx.from_pandas_edgelist(df1,'RT','user')

# G = nx.from_pandas_edgelist(df,'number','contactnumber', edge_attr='callduration')
#durations = [i['callduration'] for i in dict(G.edges).values()]
labels = [i for i in dict(G.nodes).keys()]
labels = {i:i for i in dict(G.nodes).keys()}

fig, ax = plt.subplots(figsize=(12,5))
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, ax = ax, labels=True)
nx.draw_networkx_edges(G, pos, width=3, ax=ax)
_ = nx.draw_networkx_labels(G, pos, labels, ax=ax)
# #df = pd.DataFrame({'number':['123','234','345'],'contactnumber':['234','345','123'],'callduration':[1,2,4]})
# df = pd.read_csv('../r.csv', encoding = "ISO-8859-1")

# df

# G = nx.from_pandas_edgelist(df,'number','contactnumber', edge_attr='callduration')
# durations = [i['callduration'] for i in dict(G.edges).values()]
# labels = [i for i in dict(G.nodes).keys()]
# labels = {i:i for i in dict(G.nodes).keys()}

# fig, ax = plt.subplots(figsize=(12,5))
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, ax = ax, labels=True)
# nx.draw_networkx_edges(G, pos, width=durations, ax=ax)
# _ = nx.draw_networkx_labels(G, pos, labels, ax=ax)