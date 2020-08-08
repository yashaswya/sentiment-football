import pandas as pd
import nltk
from autocorrect import Speller
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tag import pos_tag,map_tag
from nltk.corpus import sentiwordnet as swn
import time, string
import re
#nltk.download('universal_tagset')

#Load CSV to DataFrame
df = pd.read_csv('api_data_Arsenal.csv')
df_copy = df
df_test = df.head()
# print(len(df_copy))


# Initializing the Lemmatizer, Stemmer and stop words
lemma = WordNetLemmatizer()
stem = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Cleaning or Pre-processing tweets
pstem = PorterStemmer()
#nltk.download('wordnet')
lem = WordNetLemmatizer()
stop_words = stopwords.words('english')

spell=Speller(fast=True)


# Pre-processing Test
tweets = df_copy['tweet']
tweets_copy = tweets
# b=[]
# for tweet in tweets_copy:
#     b.append(''.join(re.sub("(@[A-Za-z0–9]+)|([0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))
#     tweet = ''.join([i for i in tweet if not i in b])
#     print(tweet)
def remove_emoji(string):
    emoticons = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoticons.sub(r'', string)
def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)
a=[]
for tweet in tweets:
    tweet = re.sub(r"\d", "", tweet) # Removing digits
    tweet = ' '.join([spell(word) for word in tweet.split()])
    a.append(remove_emoji(strip_all_entities(strip_links(tweet))))
    # ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

print(a)
df_copy['cleaned_tweets'] = a

print(df_copy)
df_copy.to_csv('processed.csv')