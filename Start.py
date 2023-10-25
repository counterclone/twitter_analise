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
import sys

st.set_page_config(page_title="Start",page_icon="^0^")

st.sidebar.success("choose")

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

hashtag=[""]

st.title("twitter analysis")

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

            


lst= st.text_input('enter text space seperated',"gun violence")
rate=st.number_input('enter refresh rate',2)
submit = st.checkbox('give')

if (submit):
        
    
        lst=[tag.strip() for tag in lst.split(" ")]
        hashtag.extend(lst)
        #st.write(hashtag)
        username="DiscordM8285"
        password="helloworld1234567890"
        st.write("login started")

        bot = tb.Twitterbot(username,password )

        #login
        bot.login()
        st.write("login finished")
        #get clean-text tweets
        tweets,usernames=bot.get_tweets(hashtag,rate)
        print("done")
        st.write("fetching data")
        df=pd.DataFrame({'username':usernames,'tweet':tweets})

        df.to_csv('output.csv', index=False)
        print("csv file saved")
        st.write("fetching complete")
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
        st.dataframe(newdf,width=2000,height=700)
        res.to_csv(output_path,index=False)
        print("completed")


        
                
