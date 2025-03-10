import pandas as pd

posts = pd.read_csv('./all_posts.csv')
for record in range(posts.iloc[:, 0:1].size):
    print(dict(posts['user_review'][record]))
