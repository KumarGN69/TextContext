import praw, time, json, dotenv, os

class RedditHandler:
    """
    """

    def __init__(self,query):
        dotenv.load_dotenv()
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.client_useragent = os.getenv('REDDIT_USER_AGENT')
        self.client_searchquery = query
        self.subreddits = ["GooglePixel"]
    
    def getRedditInstance(self):
        try:
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT')
            )
            print("Successfully authenticated with Reddit API")
            return reddit
        except Exception as e:
            print(f"Error authenticating with Reddit: {e}")
            exit()
   
    def fetch_reviews(self):
        """Fetch user reviews (comments) from Reddit posts related to the search query."""
        all_posts = []
        try:
            for subreddit in self.subreddits:
                print(f"\n Searching in r/{subreddit} for posts related to: '{self.client_searchquery}'")
                reddit = self.getRedditInstance()
                subreddit_instance = reddit.subreddit(subreddit)
                posts = subreddit_instance.search(
                    query=self.client_searchquery,
                    time_filter=os.getenv('TIME_FILTER'),
                    limit=int(os.getenv('NUM_POSTS'))
                    )
                for post in posts:
                    
                    # print(f"📌 Found Post: {post.title} (Upvotes: {post.score})")
                    post.comments.replace_more(limit=2)  # Avoid excessive API calls
                    all_posts.append({
                        "post_title": post.title,
                        "self_text":post.selftext,
                    })
                    time.sleep(1)  # Pause to prevent API rate limits

        except Exception as e:
            print(f"Error fetching reviews: {e}")

        # return all_posts
        return all_posts

    
