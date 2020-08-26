import pandas as pd
from textblob import TextBlob

df = pd.read_csv("processed.csv")
df_new =pd.DataFrame()
df_new['tweets']=df['cleaned_tweets']


senti = []
for i in range(len(df_new.index)):
    tweet = df_new.loc[i]['tweets']
    print(tweet)
    analysis = TextBlob(str(tweet))
    if analysis.sentiment[0]>0:
        #df_copy.loc[i]['sentiment'] = 'Positive'
        senti.append('positive')
    elif analysis.sentiment[0]<0:
        #df_copy.loc[i]['sentiment'] = 'Negative'
        senti.append('negative')
    else:
        senti.append('neutral')
        #df_copy.loc[i]['sentiment'] = 'Neutral'

#print(senti)
df_new['sentiment']=senti
print(df_new)
df_new.to_csv('tb_sentiment.csv')
