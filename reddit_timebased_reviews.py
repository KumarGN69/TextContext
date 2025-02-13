import praw
from psaw import PushshiftAPI
import pandas as pd
import datetime, json
import dotenv, os

dotenv.load_dotenv()
# # ✅ Reddit API credentials (Replace with your own)
# REDDIT_CLIENT_ID = "your_client_id"
# REDDIT_CLIENT_SECRET = "your_client_secret"
# REDDIT_USER_AGENT = "your_user_agent"

# ✅ Initialize PRAW and PSAW
reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )

api = PushshiftAPI(reddit)  # Connect PSAW to PRAW

# ✅ Define Search Parameters
SUBREDDITS = ["GooglePixel", "Android"]  # Target subreddits
SEARCH_QUERY = "Google Pixel ecosystem experience"  # Topic to search

# ✅ Define Timeframe (e.g., last 7 days)
DAYS_BACK = 7
end_time = int(datetime.datetime.utcnow().timestamp())  # Current time (UTC)
start_time = int((datetime.datetime.utcnow() - datetime.timedelta(days=DAYS_BACK)).timestamp())

# ✅ Fetch posts within timeframe using PushshiftAPI
print(f"🔍 Searching for posts from the last {DAYS_BACK} days...")

posts = list(api.search_submissions(
    q=SEARCH_QUERY,
    subreddit=SUBREDDITS,
    after=start_time,
    before=end_time,
    limit=10,  # Adjust as needed
    sort="desc"
))

print(f"✅ Found {len(posts)} posts")

# ✅ Extract Comments from the Posts using PRAW
all_comments = []

for post in posts:
    try:
        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=2)  # Get top-level comments
        
        for comment in submission.comments.list():
            if comment.created_utc >= start_time and comment.created_utc <= end_time:  # Filter by timeframe
                all_comments.append({
                    "subreddit": submission.subreddit.display_name,
                    "post_title": submission.title,
                    "post_url": submission.url,
                    "comment": comment.body,
                    "upvotes": comment.score,
                    "comment_time": datetime.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                })
    except Exception as e:
        print(f"❌ Error fetching comments for post {post.id}: {e}")

# ✅ Save to CSV
if all_comments:
    df = pd.DataFrame(all_comments)
    file_name = "reddit_comments_filtered.csv"
    df.to_csv(file_name, index=False)
    print(f"\n✅ Data saved successfully to '{file_name}'")
else:
    print("⚠️ No comments found in the given timeframe!")
