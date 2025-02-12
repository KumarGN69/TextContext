import praw
import pandas as pd
import time, json
from textblob import TextBlob

#  Reddit API credentials - Replace these with your credentials
REDDIT_CLIENT_ID = "IR5d96aUn_Jowv2GaR4HQQ"
REDDIT_CLIENT_SECRET = "KaW7TY_ozL0kTIwzVjSzF2O2B1yQ-Q"
REDDIT_USER_AGENT = "Review scrapper 1.0"

# Initialize Reddit API using PRAW
try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    print("✅ Successfully authenticated with Reddit API")
except Exception as e:
    print(f"❌ Error authenticating with Reddit: {e}")
    exit()

# Search Query & Subreddits
# search_query = "How would you rate the Google Pixel ecosystem experience?"
search_query = "Google Pixel Buds user experience?"
subreddits = ["GooglePixel", "Android"]  # Targeted subreddits
num_posts = 10  # Number of posts to fetch

def fetch_reviews():
    """Fetch user reviews (comments) from Reddit posts related to the search query."""
    all_comments = []
    
    try:
        for subreddit in subreddits:
            print(f"\n🔍 Searching in r/{subreddit} for posts related to: '{search_query}'")
            
            subreddit_instance = reddit.subreddit(subreddit)
            posts = subreddit_instance.search(search_query, limit=num_posts)

            for post in posts:
                print(f"📌 Found Post: {post.title} (Upvotes: {post.score})")

                post.comments.replace_more(limit=2)  # Avoid excessive API calls
                for comment in post.comments.list():
                    if comment.body:
                        all_comments.append({
                            "subreddit": subreddit,
                            "post_title": post.title,
                            "post_url": post.url,
                            "comment": comment.body,
                            "upvotes": comment.score
                        })
                        # print(comment.body)
                
                time.sleep(1)  # Pause to prevent API rate limits

    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")

    return all_comments

# Extract reviews
reviews = fetch_reviews()
reviews_json= json.loads(json.dumps(reviews))
nuetral = positive = negative = 0
for review in reviews_json:
    sentiment = TextBlob(review['comment']).sentiment
    if sentiment.subjectivity <=0.5 and sentiment.polarity > 0.05: 
        # print(f"title: {review['post_title']},comment: {review['comment']}")
        # print(f"Sentiment is fact based and positive: {sentiment.polarity}")
        positive += 1
    elif sentiment.subjectivity <= 0.5 and sentiment.polarity < -0.05:
        # print(f"Sentiment is fact based and negative: {sentiment.polarity}")
        negative += 1
    elif sentiment.subjectivity <= 0.5 and (sentiment.polarity >= -0.05 and sentiment.polarity <= 0.05):
        # print(f"sentiment is nuetral")
        nuetral += 1
print(f"Positive: {positive}, Negative:{negative}, Nuetral: {nuetral}")        
# Save to CSV
if reviews:
    df = pd.DataFrame(reviews)
    file_name = "reddit_pixel_ecosystem_reviews.csv"
    df.to_csv(file_name, index=False)
    df.to_json("reddit_pixel_ecosystem_reviews.json")
    print(f"\n✅ Data saved successfully to '{file_name}'")
else:
    print("⚠️ No reviews found!")