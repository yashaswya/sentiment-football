import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from wordcloud import WordCloud, STOPWORDS

sns.set(style="darkgrid")

# raw tweets with sentiment orientation
og = pd.read_csv('api_data_Arsenal.csv')
og_true = og['sentiment']
# print(og_true,type(og_true))

processed = pd.read_csv('processed.csv')

# TextBlob lexicon
tb = pd.read_csv('lexicon_sentiment.csv')
tb['sentiment'].str.lower()
tb_pred = tb['sentiment']
# print(len(og_true),len(tb_pred))

# so-pmi lexicon
pmi = pd.read_csv('pmi.csv')
pmi_pred = pmi['sentiment']

# Vader Lexicon
vader = pd.read_csv('vader_sentiment.csv')
vader['tweets'] = vader['tweets'].astype(str)
vader_pred = vader['sentiment']

# swn lexicon
swn = pd.read_csv('swn_sentiment.csv')
swn_pred = swn['basic_avg_sentiment']

# count plot
data = pd.DataFrame()
data['Actual'] = og_true
data['TextBlob'] = tb_pred
data['SO-PMI'] = pmi_pred
data['Vader'] = vader_pred
data['SWN'] = swn_pred
vader_count = sns.countplot(x="Vader",data=data,hue='Vader')
plt.show()
# vader_count.figure.savefig("vader_count.png")
tb_count = sns.countplot(x="TextBlob",data=data,hue='TextBlob')
plt.show()
# tb_count.figure.savefig("tb_count.png")
pmi_count = sns.countplot(x="SO-PMI",data=data,hue='SO-PMI')
plt.show()
# pmi_count.figure.savefig("pmi_count.png")
swn_count = sns.countplot(x="SWN",data=data,hue='SWN')
plt.show()
# swn_count.figure.savefig("swn_count.png")

print('*'*25 +'TextBlob Results'+'*'*25)
tb_confusion_matrix = pd.crosstab(og_true, tb_pred, rownames=['Actual'], colnames=['Predicted'])
print (tb_confusion_matrix)
tb_heat = sns.heatmap(tb_confusion_matrix, annot=True)
plt.show()
tb_heat.figure.savefig("tb_heat.png")
report_tb = classification_report(og_true, tb_pred, target_names=['negative','neutral','positive'])
print(report_tb)


print('*'*25 +'SO-PMI Results'+'*'*25)
pmi_confusion_matrix = pd.crosstab(og_true, pmi_pred, rownames=['Actual'], colnames=['Predicted'])
print (pmi_confusion_matrix)
pmi_heat = sns.heatmap(pmi_confusion_matrix, annot=True)
plt.show()
pmi_heat.figure.savefig("pmi_heat.png")
report_pmi = classification_report(og_true, pmi_pred, target_names=['negative','neutral','positive'])
print(report_pmi)


print('*'*25 +'Vader Results'+'*'*25)
vader_confusion_matrix = pd.crosstab(og_true, vader_pred, rownames=['Actual'], colnames=['Predicted'])
print (vader_confusion_matrix)
vader_heat = sns.heatmap(vader_confusion_matrix, annot=True)
plt.show()
vader_heat.figure.savefig("vader_heat.png")
report_vader = classification_report(og_true, vader_pred, target_names=['negative','neutral','positive'])
print(report_vader)


print('*'*25 +'SWN Results'+'*'*25)
swn_confusion_matrix = pd.crosstab(og_true, swn_pred, rownames=['Actual'], colnames=['Predicted'])
print (swn_confusion_matrix)
swn_heat = sns.heatmap(swn_confusion_matrix, annot=True)
plt.show()
swn_heat.figure.savefig("swn_heat.png")
report_swn = classification_report(og_true, swn_pred, target_names=['negative','neutral','positive'])
print(report_swn)

# overall = sns.countplot(x="sentiment",data=og)
# plt.show()
# overall.figure.savefig("overall_count.png")
#
#
# df = processed
# df['cleaned_tweets'] = df['cleaned_tweets'].astype(str)
# words = ' '.join(df['cleaned_tweets'])
# wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=2500, width=3000).generate(str(words))
# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()
# wordcloud.to_file("overall.png")


# vader_pos = vader[vader['sentiment'] == 'positive']
# vader_neg = vader[vader['sentiment'] == 'negative']
#
# # positive tweets
# vader_pos_words = ' '.join(vader_pos['tweets'])
# vader_wc_pos = WordCloud(stopwords=STOPWORDS, background_color='white', height=2500, width=3000).generate(vader_pos_words)
# plt.imshow(vader_wc_pos)
# plt.axis('off')
# plt.show()
#
# # negative tweets
# vader_neg_words = ' '.join(vader_neg['tweets'])
# vader_wc_neg = WordCloud(stopwords=STOPWORDS, background_color='white', height=2500, width=3000).generate(vader_neg_words)
# plt.imshow(vader_wc_neg)
# plt.axis('off')
# plt.show()


