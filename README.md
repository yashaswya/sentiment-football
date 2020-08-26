# sentiment-football

Sentiment analysis on football data extracted from twitter.

<!-- GETTING STARTED -->
## Getting Started
Here we will use lexicon based sentiment analysis on football related tweets extracted from twitter.
We will mainly use the following approaches:
1. TextBlob
2. SWN Lexicon
3. VADER Lexicon
4. SO-PMI based
### Usage
1. To download the tweets execute the script tweets_api.py with appropriate keyword to be used as a search term.
2. Once the tweets are downloaded replace the generated csv file in the tweets_basic_preprocessing.py script. This script will generate a processed csv file.
3. <b>TextBlob:</b> Load the generated processed csv file in the textblob.py script.
4. <b>VADER:</b> Load the file generated in step 2 in vader.py and execute the script.
5. <b>SWN:</b> Load the file generated in step 2 in swn.py and execute the script.
6. <b>SO-PMI:</b> Load the file generated in step 2 in pmi.py and execute the script.
