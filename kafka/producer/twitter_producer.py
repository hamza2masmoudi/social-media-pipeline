from tweepy import StreamingClient, Rule
from kafka import KafkaProducer
import json

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGGdyQEAAAAADVvVt%2FI1y5OPPPYpohtEidu%2Fygc%3DiqMYtDM2WqRATjOjrTpT6TwyLNuPy5WBrDTQy1SHVfe6FCPgPC'  # Keep this secret!
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'social-media'

class TwitterListener(StreamingClient):
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def on_tweet(self, tweet):
        # Send both text and tweet ID for tracking
        data = {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at.isoformat()
        }
        self.producer.send(TOPIC_NAME, value=data)
        print(f"Sent tweet: {tweet.id}")  # Debugging
        return True

    def on_errors(self, errors):
        print("Stream Error:", errors)

if __name__ == "__main__":
    listener = TwitterListener(BEARER_TOKEN)

    # Clean up existing rules
    existing_rules = listener.get_rules().data or []
    if existing_rules:
        listener.delete_rules([rule.id for rule in existing_rules])

    # Add a sample rule (track tweets containing "python")
    listener.add_rules(Rule(value="python lang:en -is:retweet"))  # Customize this

    # Start streaming
    listener.filter(
        tweet_fields=["id", "text", "created_at"],
        expansions=["author_id"],
        user_fields=["username"]
    )