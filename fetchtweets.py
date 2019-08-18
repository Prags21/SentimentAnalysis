# pylint: skip-file
import csv
import tweepy



Auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
Auth.set_access_token(Access_token, Access_token_secret)

api = tweepy.API(Auth)
#public_tweets = api.search('chandrayaan2')

maximum_number_of_tweets_to_be_extracted = 1000

# Mention the hashtag that you want to look out for
listOfTweets=[]
keys=['Screen Name','User Name','Tweet Created At','Tweet Text','User Location','Retweet Count','Phone Type']

with open('result.csv', 'a') as csvFile:
    dict_writer = csv.DictWriter(csvFile, fieldnames=keys)
    dict_writer.writeheader()

    for tweet in tweepy.Cursor(api.search, q='robotics workplace', since = "2019-07-08", until = "2019-08-13", rpp=100, lang = "en", tweet_mode='extended').items(1500):
        print(tweet)
        break
        dict_ = {'Screen Name': str(tweet.user.screen_name),
                 'User Name': tweet.user.name.encode('utf-8'),
                 'Tweet Created At': str(tweet.created_at),
                 'Tweet Text': tweet.full_text.encode('utf-8'),
                 'User Location': tweet.user.location.encode('utf-8'),
                 'Retweet Count': str(tweet.retweet_count),
                 'Phone Type': tweet.source.encode('utf-8')
                }
        listOfTweets.append(dict_)
        dict_writer.writerow(dict_)
