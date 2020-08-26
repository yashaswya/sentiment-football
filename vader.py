import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("processed.csv")
analyser = SentimentIntensityAnalyzer()
df_new = pd.DataFrame()
df_new['tweets'] = df['cleaned_tweets']
print(df_new['tweets'])
i=0
for tweet in df_new['tweets']:
    print(tweet)
    score = analyser.polarity_scores(str(tweet))
    #print(type(score))
    df_new.loc[i,'neg_score'] = score['neg']
    df_new.loc[i,'neu_score'] = score['neu']
    df_new.loc[i,'pos_score'] = score['pos']
    df_new.loc[i,'com_score'] = score['compound']
    compound = score['compound']
    if compound >= 0.05:
        df_new.loc[i,'sentiment'] = 'positive'
    elif (compound > -0.05) and (compound < 0.05):
        df_new.loc[i, 'sentiment'] = 'neutral'
    else:
        df_new.loc[i, 'sentiment'] = 'negative'
    
    i+=1
    #print(score)
print(df_new)
df_new.to_csv("vader_sentiment.csv")
