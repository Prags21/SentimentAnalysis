# pylint: skip-file
import matplotlib
import re
import numpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
from collections import *
from itertools import count

from random import randint
warnings.filterwarnings("ignore")
class OrderedCounter(Counter, OrderedDict):
    pass
listOfTweets=[]
d =[]
G = nx.DiGraph()
def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [ source.strip()
             for tuple in rt_patterns.findall(tweet)
                 for source in tuple
                     if source not in ("RT", "via") ]
for tweet in table.iterrows():
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
counts=Counter(listOfTweets).most_common(30)
a=[]
size_n=[]
labels = {}
n_color=[]
for i in counts:
    d={}
    d['node_']=i[0]
    d['frequency']=i[1]
    a.append(d)
for node in G.nodes():
    size_n.append(5)
    n_color.append('blue')
for node in G.nodes():
    for idx, item in enumerate(a):
        if node in item['node_']:
            size_n[idx] = round(item['frequency']/10)
            n_color[idx] = 'red'
            labels[item['node_']] = item['node_']

pos = nx.spring_layout(G)
plt.figure(figsize=(12,12))
_=nx.draw_networkx_nodes(G, pos, node_size=size_n,node_color=n_color,alpha = 0.7)
_=nx.draw_networkx_edges(G, pos ,alpha=0.2,edge_color='r' )
_=nx.draw_networkx_labels(G,pos,labels,font_size=12,font_color='g')


#nx.eigenvector_centrality_numpy(G)
#nx.degree_centrality(G)
#nx.betweenness_centrality(G)
#nx.clustering(G,'@LoomiAssistant')