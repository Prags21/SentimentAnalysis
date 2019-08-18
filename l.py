#Visualisation
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from IPython.display import display
from wordcloud import WordCloud, STOPWORDS

matplotlib.style.use('ggplot')

def wordcloud(tweets,col):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="white",stopwords=stopwords,random_state = 2016).generate(" ".join([i for i in tweets[col]]))
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("Good Morning Datascience+")
    
wordcloud(tweets,'text')
#preprocess text in tweets by removing links, @UserNames, blank spaces, etc.
#preprocess text in tweets by removing links, @UserNames, blank spaces, etc.
def preprocessing_text(table):
    #put everythin in lowercase
    table['Tweet Text'] = table['Tweet Text'].str.lower()
  
    for ind,item in enumerate(table['Tweet Text']):
        table.at[ind,'Tweet Text']= bytes(item, "utf-8").decode("unicode_escape")
     
    #Replace rt indicating that was a retweet
    table['Tweet Text'] = table['Tweet Text'].str.replace('rt', '')
    #Replace occurences of mentioning @UserNames
    table['Tweet Text'] = table['Tweet Text'].replace(r'@\w+', '', regex=True)
    #Replace links contained in the tweet
    table['Tweet Text'] = table['Tweet Text'].replace(r'http\S+', '', regex=True)
    table['Tweet Text'] = table['Tweet Text'].replace(r'www.[^ ]+', '', regex=True)
    #remove numbers
    table['Tweet Text'] = table['Tweet Text'].replace(r'[0-9]+', '', regex=True)
    #replace special characters and puntuation marks
    table['Tweet Text'] = table['Tweet Text'].replace(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', regex=True)
    return table