import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite
a=pd.read_csv('file.csv',delimiter = ',')
G = nx.DiGraph()
edges_=[]
n_size=[]
noun=[]
adj=[]
labels={}
n_color=[]
weights=[]
for ind,item in a.iterrows():
    #G.add_nodes_from(item['Adj'],bipartite=0)
    #G.add_nodes_from(item['Adj'],bipartite=1)
    adj.append(item['Adj'])
    noun.append(item['Noun'])
    edges_.append((item['Adj'],item['Noun']))
    weights.append(item['Count']/800)
    n_size.append(item['Count']/3)
    #n_color.append('blue')  
    #n_color.append('blue')  
    labels[item['Adj']]=item['Adj']
    labels[item['Noun']]=item['Noun']

    edge_=set(tuple(i) for i in edges_)
    G.add_edges_from(edge_)
#for node in G.nodes():
    #print(node)
    #size_n.append(5)
    #n_color.append('blue')  
for ind,node in enumerate(G):
  if node in adj:
  #if ind%2==0:
      n_color.append('blue')
  else: n_color.append('green') 
pos = nx.spring_layout(G,k=2.5)
plt.figure(figsize=(15,15))
_=nx.draw_networkx_nodes(G, pos,scale=100, node_size=n_size,node_color=n_color,alpha = 0.9)
_=nx.draw_networkx_edges(G, pos ,alpha=0.9,width=weights )
#_=nx.draw_networkx_labels(G,pos,labels,font_size=12)  
pos_attrs = {}
for node, coords in pos.items():
    if coords[0]<0:
      coords[0]=coords[0]-0.06
      if coords[1]<0:
        coords[1]=coords[1]-0.04
      else:
        coords[1]=coords[1]+0.04
    else:
      coords[0]=coords[0]+0.06
      if coords[1]<0:
        coords[1]=coords[1]-0.04
      else:
        coords[1]=coords[1]+0.04
    pos_attrs[node] = (coords[0], coords[1])


_=nx.draw_networkx_labels(G, pos_attrs, labels,font_weight ='bold',font_size =10)