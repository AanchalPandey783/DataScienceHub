import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterSentimentAnalyzer:
    '''
    A class for fetching and analyzing sentiment from Twitter data.
    '''
    def __init__(self):
        '''
        Constructor to initialize Twitter API credentials and set up API access.
        '''
        # Replace with your actual Twitter API credentials
        consumer_key = 'YOUR_CONSUMER_KEY'
        consumer_secret = 'YOUR_CONSUMER_SECRET'
        access_token = 'YOUR_ACCESS_TOKEN'
        access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

        # Attempt to authenticate with the Twitter API
        try:
            # Initialize OAuthHandler object with consumer keys
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # Set access tokens
            self.auth.set_access_token(access_token, access_token_secret)
            # Create a Tweepy API object to interact with Twitter
            self.api = tweepy.API(self.auth)
        except tweepy.TweepError:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet_text):
        '''
        Cleans tweet text by removing special characters, links, and usernames using regex.
        '''
        return ' '.join(re.sub(r"(@\w+)|([^a-zA-Z0-9 \t])|(\w+:\/\/\S+)", "", tweet_text).split())

    def analyze_sentiment(self, tweet_text):
        '''
        Determines the sentiment of a tweet using TextBlob.
        '''
        # Create a TextBlob object from the cleaned tweet text
        analysis = TextBlob(self.clean_tweet(tweet_text))
        # Classify the sentiment based on polarity
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def fetch_tweets(self, keyword, num_tweets=10):
        '''
        Fetches and processes tweets based on a search keyword.
        '''
        tweets_list = []

        try:
            # Fetch tweets from Twitter API using the search keyword
            fetched_tweets = self.api.search(q=keyword, count=num_tweets)

            # Process each tweet fetched
            for tweet in fetched_tweets:
                parsed_tweet = {
                    'text': tweet.text,
                    'sentiment': self.analyze_sentiment(tweet.text)
                }

                # Add tweet to the list only if it is not a retweet
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets_list:
                        tweets_list.append(parsed_tweet)
                else:
                    tweets_list.append(parsed_tweet)

            return tweets_list

        except tweepy.TweepError as error:
            print(f"Error: {str(error)}")

def main():
    # Create an instance of the TwitterSentimentAnalyzer class
    twitter_analyzer = TwitterSentimentAnalyzer()
    # Fetch and analyze tweets related to a specific keyword
    tweets = twitter_analyzer.fetch_tweets(keyword='Python', num_tweets=200)

    # Filter tweets by sentiment
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # Display the percentage of positive tweets
    print(f"Positive tweets percentage: {100 * len(positive_tweets) / len(tweets)}%")
    # Display the percentage of negative tweets
    print(f"Negative tweets percentage: {100 * len(negative_tweets) / len(tweets)}%")
    # Display the percentage of neutral tweets
    print(f"Neutral tweets percentage: {100 * (len(tweets) - len(positive_tweets) - len(negative_tweets)) / len(tweets)}%")

    # Print some of the positive tweets
    print("\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])

    # Print some of the negative tweets
    print("\nNegative tweets:")
    for tweet in negative_tweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    # Execute the main function
    main()