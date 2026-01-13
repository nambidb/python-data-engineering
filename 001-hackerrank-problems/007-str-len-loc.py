import pandas as pd

# Example data
tweets = pd.DataFrame({
    'tweet_id': [1, 2],
    'content': ["Let us Code", "More than fifteen chars are here!"]
})

invalid_tweets = tweets.loc[tweets['content'].str.len() > 15,['tweet_id']]

print(invalid_tweets)
