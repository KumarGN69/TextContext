## Sentiment and Classification of User Reviews from Reddit based on specific search query
For Sentiment analysis based on a search string from reddit

1. ### **class RedditHandler** 
   2. Creates and instance and retrieves post for specified timeframe for the search string
3. class SentimentAnalyzer
   * assess the sentiments based on post title and the original user review/comment
   - **_Sentiment analysis is based on TextBlob package_**
   - **_The threshold values for sentiment analysis needs to be fine-tuned_**
   - **_Need to cross check with LLM based prompting to cross verify the output from TextBlob_**_

### 5. **class ReviewClassifier**

  *   classifies the combined review (post title + original user review) into specific categories 
    * Usability
    * Service
    * Support
    * Others
    *     **_Classification is based on LLM based prompting_**
    *     **_Currently using Ollama and llama3.2. try with other LLMs_**
    *     **_The prompt needs to be enhanced to get the correct classification_**
