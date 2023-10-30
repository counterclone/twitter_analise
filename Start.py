import streamlit as st
import selenium as st
import twitterbot as tb
import pandas as pd
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import matplotlib.pyplot as plt
import copy
import string
import sys
@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

st.set_page_config(page_title="Start",page_icon="^0^")



os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

hashtag=[""]

st.title("Twitter Analysis")


#============================================================================
def process(text):
        encoded_tweet = tokenizer(text, return_tensors='pt')
        return encoded_tweet

def sentiment(text):
        enct=process(text)
        output=model(**enct)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        dic={}
        for i in range(len(scores)):
            dic[scores[i]]=labels[i]
        # return max(dic.keys())
        return dic[max(dic.keys())]
#=================================================================================



lst= st.text_input('Enter hashtags',"gun bjp hindu muslim")
rate=st.number_input('Refresh Rate',2)
submit = st.button('Submit')

if (submit):
        
    
        lst=[tag.strip() for tag in lst.split(" ")]
        hashtag.extend(lst)
        #st.write(hashtag)
        
        st.write("login started")
        bot = tb.Twitterbot( )
        bot.login(0)
               
        st.write("login finished")
        #get clean-text tweets
        st.write("fetching data")
        tweets,usernames=bot.get_tweets(hashtag,rate)
        print("done")
        
        df=pd.DataFrame({'username':usernames,'tweet':tweets})
        df.dropna(subset=['tweet'], inplace=True)
        st.write("fetching complete")
        df.to_csv('output.csv', index=False)
        print("csv file saved")
        
        print("started analysis" )
        st.write("analysis started")
        words=pd.read_csv("Hate speech words - Sheet1.csv")
        df=pd.read_csv("output.csv")
        newdf=df.dropna()

        roberta = "cardiffnlp/twitter-roberta-base-sentiment"

        model = AutoModelForSequenceClassification.from_pretrained(roberta)
        tokenizer = AutoTokenizer.from_pretrained(roberta)

        labels = ['Negative', 'Neutral', 'Positive']

        

        #classification of tweets
        newdf['type']=newdf['tweet'].apply(lambda text:sentiment(text))

        output_path='results.csv'
        newdf.to_csv(output_path,index=False)

        #read the classification file
        res=pd.read_csv("results.csv")
        output_path='results.csv'
        # st.write(newdf.to_markdown(index=False))
        st.dataframe(newdf,width=2000,height=700)
        res.to_csv(output_path,index=False)
        print("completed")
        st.write("switch to show tab")


        
                
