import re
from datetime import datetime
import csv
import numpy as np
import pandas as pd



class Swn:
    np_dictionary = []  # Stores the dictionary in the form of a numpy array

    def __init__(self):

        pass

    @staticmethod
    def convert_sentiwordnet_to_csv(input_filename, output_filename):
        print("Converting sentiwordnet lexicon to csv...")
        with open(input_filename, 'r') as reader, open(output_filename, 'w') as writer:
            reader = reader.readlines()
            start_time = datetime.now().time()
            line_count = 0
            for line in reader:
                line_count += 1
                # read the header and write into the other file
                line_contents = line.split('\t')
                line_contents = line_contents[:-1]
                pattern = re.compile(r'(.*?)#[\d]+')
                words_to_clean = pattern.findall(line_contents[-1])
                cleaned_words_list = []
                for word in words_to_clean:
                    cleaned_words_list.append(word.strip())
                cleaned_words = " ".join(cleaned_words_list)
                line_contents[-1] = cleaned_words
                new_line = ','.join(line_contents)
                writer.write(new_line)
                writer.write('\n')
        print("CSV conversion completed...")

    @staticmethod
    def get_words_in_tweet(tweet):
        words_in_tweet = []
        if len(tweet) != 0:
            words_in_tweet = tweet.split()
        return words_in_tweet

    def load_dictionary(self, file_path):
        dictionary_list = []
        with open(file_path, 'r') as f:
            csv_data = csv.reader(f, delimiter=',')
            for row in csv_data:
                word_list = []
                word_list.append(row[0])  # Add context of word i.e adjective, noun, etc
                word_list.append(row[2])  # Add positive score of word
                word_list.append(row[3])  # Add negative score of word
                word_list.append(row[4])  # Add the word(s)
                dictionary_list.append(word_list)  # Add details of the word into the dictionary
        return dictionary_list

    @staticmethod
    def return_dictionary_object(raw_tweet, cleaned_tweet, tweet_sentiment, tweet_sentiment_score, tweet_words,
                                 tweet_words_scores):
        tweet_json_obj = {}
        tweet_json_obj["raw_tweet"] = raw_tweet
        tweet_json_obj["cleaned_tweet"] = cleaned_tweet
        tweet_json_obj["sentiment"] = tweet_sentiment
        tweet_json_obj["sentiment_score"] = tweet_sentiment_score
        tweet_json_obj["tweet_words"] = tweet_words
        tweet_json_obj["tweet_words_scores"] = tweet_words_scores
        return tweet_json_obj

    @staticmethod
    def compute_sentiment_scores_of_word(word, dictionary_indices):
        rows = dictionary_indices[0]
        positive_score_sum = 0
        negative_score_sum = 0
        for r in rows:

            positive_score_sum += float(np_dictionary[r][1])
            negative_score_sum += float(np_dictionary[r][2])
        avg_positive_score_word = positive_score_sum / (len(rows))
        avg_negative_score_word = negative_score_sum / (len(rows))

        return (avg_positive_score_word, avg_negative_score_word)

    def sentiment_analysis(self, raw_tweets, cleaned_tweets):
        sentiment_analysis_results = []
        analysis_results_to_plot = []
        dictionary_list = self.load_dictionary("sentiwordnet_dictionary.csv")  # Change file path as required
        global np_dictionary
        np_dictionary = np.array(dictionary_list)  # Converted to numpy.array for faster search using numpy.where()
        for c_tweet, r_tweet in zip(cleaned_tweets, raw_tweets):
            analysis_result_tweet = {}
            words = self.get_words_in_tweet(str(c_tweet).strip())
            #print("Current tweet: " + str(r_tweet))
            if not words:
                print("Assigning neutral rating for: " + str(r_tweet))
                analysis_result_tweet = self.return_dictionary_object(r_tweet, c_tweet, "neutral", "0", [], [])
                sentiment_analysis_results.append(analysis_result_tweet)
            else:
                analysis_result_tweet["raw_tweet"] = r_tweet
                analysis_result_tweet["cleaned_tweet"] = c_tweet
                analysis_result_tweet["tweet_words"] = words
                positive_scores_sum = 0
                negative_scores_sum = 0
                tweet_words_scores = []
                for word in words:
                    #print("Current word: " + word)
                    word_scores = {}
                    indices = np.where(np_dictionary == str(word))
                    dict_rows = indices[0]
                    #print("dict rows: " + str(dict_rows))
                    if len(dict_rows) == 0:  # If the word is not present in the dictionary.
                        result = (positive_sentiment_score, negative_sentiment_score) = (0, 0)  # Consider it neutral
                        word_scores["word"] = str(word)
                        word_scores["positive"] = str(positive_sentiment_score)
                        word_scores["negative"] = str(negative_sentiment_score)
                        tweet_words_scores.append(word_scores)
                        continue
                    else:
                        (positive_sentiment_score, negative_sentiment_score) = self.compute_sentiment_scores_of_word(
                            word, indices)
                        word_scores["word"] = str(word)
                        word_scores["positive"] = str(positive_sentiment_score)
                        word_scores["negative"] = str(negative_sentiment_score)
                        tweet_words_scores.append(word_scores)
                        positive_scores_sum += float(positive_sentiment_score)  # Sum up score of every word in tweet
                        negative_scores_sum += float(negative_sentiment_score)
                word_count = len(words)
                tweet_sentiment_score = (positive_scores_sum - negative_scores_sum) / word_count

                if tweet_sentiment_score > 0:
                    tweet_sentiment = "positive"
                elif tweet_sentiment_score < 0:
                    tweet_sentiment = "negative"
                else:
                    tweet_sentiment = "neutral"
                analysis_result_tweet["tweet_words_scores"] = tweet_words_scores
                analysis_result_tweet["sentiment_score"] = str(tweet_sentiment_score)
                analysis_result_tweet["bsentiment"] = tweet_sentiment
                sentiment_analysis_results.append(analysis_result_tweet)
                analysis_results_to_plot.append(str(tweet_sentiment_score))
            print("Tweet: " + str(c_tweet) + " -> [" + str(tweet_sentiment) + ", " + "{:1.6f}".format(
                tweet_sentiment_score) + "]")

        with open('swn_scores.txt', 'w') as f:
            f.write(str(analysis_results_to_plot))
        return sentiment_analysis_results

analyze = Swn()
    
    
df = pd.read_csv('processed.csv')
print(df.head())
raw_tweet = df['tweet']
cleaned_tweets = df['cleaned_tweets']
print("Sentiment Analysis")
analysis_result = analyze.sentiment_analysis(raw_tweet, cleaned_tweets)
basic = pd.DataFrame(analysis_result)
basic.to_csv('swn_sentiment.csv')

