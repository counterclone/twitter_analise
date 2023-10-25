import numpy as np
from numpy import nan
import math
import streamlit as st
import twitterbot as tb
import pandas as pd
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import matplotlib.pyplot as plt
import copy
import string


st.set_page_config(page_title="show",page_icon=":)")
st.sidebar.header("View results")

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


res = pd.read_csv("results.csv")
stopwordlist = ['a','about','above', 'after', 'again', 'ain', 'all', 'am', 'an', 'also',
                        'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
                        'being', 'below', 'between','both', 'by', 'but','can', 'cant',"can\'","cannot", 'd', 'did', 'do','dont', "don\'",
                        'does', 'doing', 'down', 'during', 'each','even','few', 'for', 'from',
                        'further', 'get','had', 'has', 'have', 'having', 'he', 'her', 'here',
                        'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
                        'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma','make','made',
                        'me', 'more', 'most','my', 'must','myself', 'now', 'not',"didn\'",'o', 'of', 'on', 'once', 'one',
                        'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such', 'still',
                        't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
                        'themselves', 'then', 'there', 'these', 'they','this', 'those',
                        'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
                        'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
                        'why', 'will', 'with', 'won', 'would','y', 'you', "youd","youll", "youre",
                        "youve", 'your', 'yours', 'yourself', 'yourselves', '➡' ,'✌']

L1=copy.deepcopy(stopwordlist)
L=[word.capitalize() for word in L1]
stopwordlist.extend(L)

words=pd.read_csv("Hate speech words - Sheet1.csv")
hate_words=words.values.tolist()
STOPWORDS = set(stopwordlist)


english_punctuations = string.punctuation
punctuations_list = english_punctuations

def cleaning_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])
def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)
def reason(text):
  text=text.lower()
  text=cleaning_stopwords(text)
  new_text=cleaning_punctuations(text)

  lst=new_text.split(' ')
  temp=copy.deepcopy(lst)
  dump=[]

  for item in hate_words:
    if(item[0] in temp and item[0] not in dump):
      dump.append(item[0])

  return ' '.join(dump)

res['words']=res[res['type']=='Negative']['tweet'].apply(lambda text:reason(text))
res['words']=res['words'].fillna(' ')

a=True
def show(label,res):
    df = pd.DataFrame(columns=["username","tweet"])
    usr=[]
    twet=[]
    for i in res.index:
            if(res['type'][i]=="Negative"):
                k=res['words'][i].split()
                for q in k:
                        if(q==label):
                            usr.append(res["username"][i])
                            twet.append(res["tweet"][i])
                            break
    df["username"]=usr
    df["tweet"]=twet
    st.dataframe(df)
labels=['positive','neutral','negative']
explode = (0, 0, 0.1)
p=0
n=0
ne=0
for i in res.index:
    if(res['type'][i]=="Positive"):
        p+=1
    elif(res['type'][i]=="Neutral"):
        ne+=1
    else:
        n+=1
data=[p,ne,n]
#sizes=res['type'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(data, explode=explode,
        labels=labels, 
        autopct='%1.1f%%',
    shadow=True, startangle=90)
ax1.axis('equal')
st.write(fig1)  # Equal aspect ratio ensures that pie is drawn as a circle.

but=[]

st.write(res)
A=res['words'].to_list()
for ele in A:
    if(ele!="" and ele!=" "):
            p=ele.split()
            for t in p:
                but.append(t)
but=list(set(but))

t=st.radio("choose",tuple(but))
show(t,res)

    
    







    
    
    


        
