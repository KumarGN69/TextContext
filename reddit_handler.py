import praw, time, json, dotenv, os
import pandas as pd


class RedditHandler:
    """
    """

    def __init__(self, queries):
        dotenv.load_dotenv()
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.client_useragent = os.getenv('REDDIT_USER_AGENT')
        self.client_searchquery = queries
        self.subreddits = ["GooglePixel", "Pixel"]

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

    def fetch_posts(self):
        """Fetch user reviews (comments) from Reddit posts related to the search query."""
        all_posts = []
        try:
            reddit = self.getRedditInstance()
            for subreddit in self.subreddits:
                # reddit = self.getRedditInstance()
                for query in self.client_searchquery:
                    print(f"\nSearching in r/{subreddit} for posts related to: '{query}'")
                    # reddit = self.getRedditInstance()
                    subreddit_instance = reddit.subreddit(subreddit)
                    posts = subreddit_instance.search(
                        # query=self.client_searchquery,
                        query=query,
                        time_filter=os.getenv('TIME_FILTER'),
                        limit=int(os.getenv('NUM_POSTS'))
                    )
                    # print(len(posts))
                    for post in posts:
                        # print(f"📌 Found Post: {post.title} (Upvotes: {post.score})")
                        post.comments.replace_more(limit=2)  # Avoid excessive API calls
                        all_posts.append({
                            "user_review": {
                                "post_title": post.title,
                                "self_text": "".join(line for line in post.selftext.splitlines()),
                            }
                        })
                        time.sleep(1)  # Pause to prevent API rate limits

        except Exception as e:
            print(f"Error fetching reviews: {e}")

        # return all_posts
        if all_posts:
            df = pd.DataFrame(all_posts)
            json_filename = "all_posts.json"
            csv_filename = "all_posts.csv"
            df.to_json(json_filename, index=False)
            df.to_csv(csv_filename,index=False)
        return all_posts
