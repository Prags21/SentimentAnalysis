# pylint: skip-file
import matplotlib
import re
import numpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
from collections import *

from random import randint
warnings.filterwarnings("ignore")
class OrderedCounter(Counter, OrderedDict):
    pass
#df = pd.DataFrame({'number':['123','234','345'],'contactnumber':['234','345','123'],'callduration':[1,2,4]})
df = pd.read_csv('/content/r.csv', encoding = "ISO-8859-1")
listOfTweets=[]
d =[]

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
        l_rt=[]
        if ":" in rt_source:
            d=re.split(r'@(\w+)' ,rt_source)
            for rt in d:
                if (rt.isalnum() or '_' in rt):
                    G.add_edges_from([(tweet[1]['Screen Name'],"@"+rt)], weight=tweet[1]['Retweet Count'])
                    listOfTweets.append("@"+rt)
        else :
            G.add_edges_from([(tweet[1]['Screen Name'],rt_source)], weight=tweet[1]['Retweet Count'])
            listOfTweets.append(rt_source)
counts=Counter(listOfTweets).most_common(9)
a=[]
size_n=[]
labels = {}
for i in counts:
    a.append(i[0])
for node in G.nodes():
    if node in a:
        #set the node name as the key and the label as its value
        print(node)
        size_n.append(160)
        labels[node] = node
    else:
        size_n.append(10)
pos = nx.spring_layout(G)
plt.figure(figsize=(12,12))

_=nx.draw_networkx_nodes(G, pos, node_size=size_n,alpha = 0.7)
_=nx.draw_networkx_edges(G, pos ,alpha=0.2 )
_=nx.draw_networkx_labels(G,pos,labels,font_size=12,font_color='r')


#nx.eigenvector_centrality_numpy(G)
#nx.degree_centrality(G)
#nx.betweenness_centrality(G)
#nx.clustering(G,'@LoomiAssistant')            