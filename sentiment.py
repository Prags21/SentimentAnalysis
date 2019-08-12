# pylint: skip-file
import csv
import pandas as pd
#nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize


# keys=['User Name','Tweet Created At','Tweet Text','User Location','Retweet Count','Polarity','Subjectivity']
# with open('result_senti.csv', 'a') as csvFile:
#     dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
#     dict_writer.writeheader()
# for tweet in data.iterrows():
#     i = tweet[0]
#     te = data.loc[i, "Tweet Text"].decode('utf-8')
#     blob = TextBlob(te)
#     print(blob)
#     dic_ = {
#      'User Name': data.loc[i, "User Name"],
#      'Tweet Created At': data.loc[i, "Tweet Created At"],
#      'Tweet Text': data.loc[i, "Tweet Text"],
#      'User Location': data.loc[i, "User Location"],
#      'Retweet Count': data.loc[i, "Retweet Count"],
#      'Polarity': blob.sentiment.polarity,
#      'Subjectivity': blob.sentiment.subjectivity
#     }
tweets = pd.read_csv("output.csv")
tweets['text'].fillna("No Text", inplace = True)

tweets['polarity'] = ''
tweets['sentiment'] = ''

a=''
headers = [
    'text',	'in_reply_to_screen_name',	'created_at',	'listed_count',
    'location',	'description',	'user_created_at',
    'statuses_count',	'followers_count',	'name',	'time_zone',
    'user_lang',	'friends_count',	'screen_name',	'country_code',
    'country',	'place_type',	'full_name', 'tweetos', 'clean text','polarity','sentiment']

tweets['text_lem'] = [''.join([WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', line)) for line in lists]).strip() for lists in tweets['text']]
vectorizer = TfidfVectorizer(max_df=0.5,max_features=10000,min_df=5,stop_words='english',use_idf=True)
X = vectorizer.fit_transform(tweets['text_lem'].str.upper())
sid = SentimentIntensityAnalyzer()
tweets['sentiment_compound_polarity'] = tweets.text_lem.apply(lambda x: sid.polarity_scores(x)['compound'])
tweets['sentiment_neutral'] = tweets.text_lem.apply(lambda x: sid.polarity_scores(x)['neu'])
tweets['sentiment_negative'] = tweets.text_lem.apply(lambda x: sid.polarity_scores(x)['neg'])
tweets['sentiment_pos'] = tweets.text_lem.apply(lambda x: sid.polarity_scores(x)['pos'])
tweets['sentiment_type'] = ''
tweets.loc[tweets.sentiment_compound_polarity>0, 'sentiment_type'] = 'POSITIVE'
tweets.loc[tweets.sentiment_compound_polarity==0, 'sentiment_type'] = 'NEUTRAL'
tweets.loc[tweets.sentiment_compound_polarity<0, 'sentiment_type'] = 'NEGATIVE'
print(tweets['sentiment_compound_polarity'][9],tweets['sentiment_neutral'][9],
tweets['sentiment_negative'][9],tweets['sentiment_pos'][9])
# for i in range(len(tweets['text'])):

#     tweets['polarity'][i] = tweets['sentiment_compound_polarity'][i]
#     tweets['sentiment'][i] = tweets['sentiment_type'][i]

# tweets.to_csv('senti.csv', columns = headers, encoding='utf-8')