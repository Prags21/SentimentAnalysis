# pylint: skip-file

# #Visualisation
# import matplotlib.pyplot as plt
# import matplotlib
# import seaborn as sns
# from IPython.display import display
# from mpl_toolkits.basemap import Basemap
# from wordcloud import WordCloud, STOPWORDS
# matplotlib.style.use('ggplot')
# pd.options.mode.chained_assignment = None
# %matplotlib inline
import pandas as pd
import networkx as nx
import re
g = nx.DiGraph()
all_tweets = pd.read_csv('../r.csv', encoding = "ISO-8859-1")

# all_tweets = [ tweet
#                for page in search_results
#                    for tweet in page["results"] ]
def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [ source.strip()
             for tuple in rt_patterns.findall(tweet)
                 for source in tuple
                     if source not in ("RT", "via") ]
for tweet in all_tweets.iterrows():

    t=tweet[1]['Tweet Text']
    rt_sources = get_rt_sources(t)
    if not rt_sources: continue
    for rt_source in rt_sources:
        g.add_edge(rt_source, tweet[1]["Screen Name"])

print(g.number_of_nodes())
print(g.number_of_edges())
print(g.edges.data())
#g.edges(data=True)([0])
#print(len(nx.connected_components(g.to_undirected())))
#sorted(nx.degree(g).values())
OUT = "snl_search_results.dot"

try:
    nx.drawing.write_dot(g, OUT)

except ImportError as e:
    # Help for Windows users:
    # Not a general-purpose method, but representative of
    # the same output write_dot would provide for this graph
    # if installed and easy to implement

    dot = ['"%s" -> "%s" [tweet_id=%s]' % (n1, n2, g[n1][n2]['tweet_id']) \
        for n1, n2 in g.edges()]
    f = open(OUT, 'w')
    f.write('strict digraph {\n%s\n}' % (';\n'.join(dot),))
    f.close()