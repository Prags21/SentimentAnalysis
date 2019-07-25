def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector

###load airline sentiment training data

airlinetrain = pd.read_csv("Airline-Sentiment-2-w-AA.csv", encoding ="ISO-8859-1")
tweets = []
featureList = []
for i in range(len(airlinetrain)):
    sentiment = airlinetrain['airline_sentiment'][i]
    tweet = airlinetrain['text'][i]
    processedTweet = processTweet2(tweet)
    featureVector = getFeatureVector(processedTweet)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment))

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end

### Remove featureList duplicates
featureList = list(set(featureList))