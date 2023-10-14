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

hashtag=[""]
rate=5
st.title("twitter analysis")

with st.form('hashtag'):
    lst= st.text_input('enter text space seperated')
    rate=st.number_input('enter refresh rate')
    submit = st.form_submit_button('give')

if submit:
    #ashtags = [tag.strip() for tag in hashtags.split(",")]
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
    #df['username']=usernames
    df.to_csv('output.csv', index=False)
    print("csv file saved")
    st.write("fetching complete")
    


    #############################################################################################################
    #os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    print("started analysis" )
    st.write("analysis started")
    words=pd.read_csv("Hate speech words - Sheet1.csv")
    df=pd.read_csv("output.csv")
    newdf=df.dropna()

    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

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


    STOPWORDS = set(stopwordlist)

    def cleaning_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])

    english_punctuations = string.punctuation
    punctuations_list = english_punctuations
    def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)

    #classification of tweets
    newdf['type']=newdf['tweet'].apply(lambda text:sentiment(text))

    output_path='results.csv'
    newdf.to_csv(output_path,index=False)

    #read the classification file
    res=pd.read_csv("results.csv")

    # prepare pie chart based on the classification
    neg=res[res['type']=='Negative']
    pos=res[res['type']=='Positive']
    neu=res[res['type']=='Neutral']
    a=len(neg)
    b=len(pos)
    c=len(neu)
    f1=a/(a+b+c)
    f2=b/(a+b+c)
    f3=c/(a+b+c)
    lst=[f1,f2,f3]
    colors = ['#ffff99', '#66b3ff', '#99ff99']
    labels = ['Negative','Positive','Neutral']
    plt.figure(figsize=(6, 6))
    plt.pie(lst,labels=labels,autopct='%1.1f%%', colors=colors)

    #extraction of words

    hate_words=words.values.tolist()
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


    output_path='results.csv'
    st.dataframe(res,width=800,height=700)
    res.to_csv(output_path,index=False)
    print("completed")
    st.write("completed")


    a=0
    while(a<=1):
        placeholder=st.empty()
        placeholder.markdown('<iframe title="visualisation" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=ba0a8ce2-c8dc-4b86-92c2-8f8c5df685a2&autoAuth=true&ctid=e94ad81e-d07a-4dd5-a808-2271a395a380" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)
        time.sleep(30)
        placeholder.empty()


        
