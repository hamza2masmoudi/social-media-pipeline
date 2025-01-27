import praw

# New credentials
REDDIT_CLIENT_ID = "GeStL_TruckY_EW-SH7xww"
REDDIT_CLIENT_SECRET = "Ct99g73HZXBHNbHzwPqYbZam4NY6fw"
REDDIT_USER_AGENT = "script:hamza-social-pipeline-v1 (by /u/Available_Score5364)"

# Initialize Reddit client
REDDIT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username="Available_Score5364",
    password="Hamza00123@#"
)

try:
    subreddit = REDDIT.subreddit("technology")
    for post in subreddit.new(limit=1):
        print(f"Test Post Title: {post.title}")
except Exception as e:
    print(f"Reddit API Error: {e}")