from tweepy import StreamingClient, OAuth2BearerHandler
import json

# Twitter API credentials (v2)
BEARER_TOKEN = 'your_bearer_token'

class MyListener(StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    # Initialize the listener with your Bearer Token
    listener = MyListener(BEARER_TOKEN)

    # Start streaming
    listener.filter(tweet_fields=["text"])