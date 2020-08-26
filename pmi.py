from __future__ import division
from collections import defaultdict
import pandas as pd
import numpy as np
from math import log


DATA_PATH = "np.txt"
POS_SEED = ['awesome', 'congratulate', 'superior', 'loves', 'brilliant', 'loved', 'fantastic', 'successful', 'congratulated', 'success', 'class', 'excellent', 'good', 'pleasant', 'scores', 'phenomenal', 'improved', 'win', 'correct', 'positive', 'better', 'delightful', 'fortunate', 'best', 'won', 'love', 'perfect', 'happy', 'gains', 'lovely', 'improving', 'strong', 'profit', 'beneficial', 'amazing', 'nice']

NEG_SEED = ['nasty', 'lost', 'hated', 'hates', 'failure', 'evil', 'damages', 'unpleasant', 'zero', 'wrong', 'lose', 'abusive', 'tough', 'down', 'weak', 'negligent', 'worst', 'poor', 'inferior', 'horrible', 'terrible', 'difficult', 'unfortunate', 'bad', 'negative', 'loss', 'unhappy', 'tragic', 'losses', 'demolition', 'volatile', 'worry', 'litigation', 'disgusting', 'awful', 'sad', 'annoy', 'hate']
def tokenizer():
    bow=defaultdict(float);
    with open(DATA_PATH, 'r', encoding="utf8") as doc:
        content=doc.read()
    tokens=content.split();
    tokens_lower=map(lambda y: y.lower(), tokens)
    for y in tokens_lower:
        bow[y]+=1.0
    return bow

def polarity_calc (filter_500=False):

    count=0
    bow=tokenizer()
    w_pos=defaultdict(float)
    w_neg=defaultdict(float)
    polarity=defaultdict(float)
    pos_word_count=0
    neg_word_count=0
    N=sum(bow.values())
    for keys in bow.keys():
        if (keys in POS_SEED):
            pos_word_count+=bow[keys]
        elif (keys in NEG_SEED):
            neg_word_count+=bow[keys]
    for line in open(DATA_PATH, encoding="utf8"):
        count+=1
        tokens=line.split()
        tokens_lc=list(map(lambda y: y.lower(), tokens))
        for t in range(len(tokens_lc)):
            if tokens_lc[t] in POS_SEED:
                
                for t2 in tokens_lc[0:t]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_pos[t2]+=1.0
                for t2 in tokens_lc[t+1:]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_pos[t2]+=1.0
            elif tokens_lc[t] in NEG_SEED:
                for t2 in tokens_lc[0:t]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_neg[t2]+=1.0
                for t2 in tokens_lc[t+1:]:
                    if(t2[0]!='@' and t2[0]!='#' and (t2 not in POS_SEED and t2 not in NEG_SEED)):
                        w_neg[t2]+=1.0
    if(filter_500==True):
        for keys in bow.keys():
            if(keys not in POS_SEED and keys not in NEG_SEED and keys[0]!='@' and keys[0]!='#'and bow[keys]<500):
                PMI_pos=(w_pos[keys]/N)/((pos_word_count/N)*(bow[keys]/N))
                PMI_neg=(w_neg[keys]/N)/((neg_word_count/N)*(bow[keys]/N))
                
                if PMI_neg==0 and PMI_pos==0:
                    polarity[keys]=0
                elif PMI_pos==0:
                    
                    if log(PMI_neg,2)<0:
                        polarity[keys]=log(PMI_neg,2)
                    else:
                        polarity[keys]=-log(PMI_neg,2)
                elif PMI_neg==0:
                    polarity[keys]=abs(log(PMI_pos,2))
    else:
        for keys in bow.keys():
            if(keys not in POS_SEED and keys not in NEG_SEED and keys[0]!='@' and keys[0]!='#'):
                PMI_pos=(w_pos[keys]/N)/((pos_word_count/N)*(bow[keys]/N))
                PMI_neg=(w_neg[keys]/N)/((neg_word_count/N)*(bow[keys]/N))
                
                if PMI_neg==0 and PMI_pos==0:
                    polarity[keys]=0
                elif PMI_pos==0:
                    
                    if log(PMI_neg,2)<0:
                        polarity[keys]=log(PMI_neg,2)
                    else:
                        polarity[keys]=-log(PMI_neg,2)
                elif PMI_neg==0:
                    polarity[keys]=abs(log(PMI_pos,2))
                    
    return polarity
        

if __name__=='__main__':

    processed = pd.read_csv('processed.csv')
    data = processed['cleaned_tweets']
    np.savetxt(r'np.txt', data.values, fmt='%s',encoding='utf8')
    a = polarity_calc()
    print(a)


    i = 0
    print(sum)
    df = pd.DataFrame(columns=['tweet','pol_value','sentiment'])
    words1 = tokenizer()
    for line in open(DATA_PATH, encoding="utf8"):

        sum = 0
        pol=[]
        words = line.split()
        #print(words)
        lower = list(map(lambda y: y.lower(), words))
        # print(lower)
        for word in lower:
            sum+= a[word]
        i+=1
        #print(i)
        df.loc[i,'tweet'] = line
        pol.append(sum)
        df.loc[i,'pol_value'] = sum
        if sum>0:
            df.loc[i,'sentiment']='positive'
        elif sum<0:
            df.loc[i,'sentiment']='negative'
        else:
            df.loc[i,'sentiment']='neutral'
        i += 1
        #print(i)

    df.to_csv('pmi.csv')