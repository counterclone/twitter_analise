import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time, os
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



def remove_non_ascii(input_string):
    return ''.join(char if ord(char) < 128 else '' for char in input_string)

def remove_extra_spaces(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def keep_alphabets_and_spaces(input_string):
    cleaned_string = re.sub(r'[^a-zA-Z\s]', '', input_string)
    return cleaned_string

def remove_duplicates(input_list):
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result



cred =pd.read_csv("cred.csv")
k=0

def listToString(s):
    str1 = " "
    return (str1.join(map(str, s)))

class Twitterbot:
    
    def __init__(self):
        print("login")
        self.k=0
        chrome_options = Options()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument(f'user-agent={user_agent}')
        # chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--allow-running-insecure-content')
        
        self.bot = webdriver.Chrome(options=chrome_options)
        # # chrome_version = "93.0.4577.15"
        # # self.bot=webdriver.Chrome(service=Service(ChromeDriverManager(version=chrome_version).install()), options=chrome_options)
        # chrome_driver_path = "./chromedriver.exe"  # Adjust the path if needed
        # #self.bot = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        # # Use service_args to specify the ChromeDriver path
        # self.bot = webdriver.Chrome(service_args=[f'--webdriver-path={chrome_driver_path}'], options=chrome_options)
        

        

    def login(self,k):
        bot=self.bot
        self.email =cred['username'][k]
        self.password= cred['password'][k]
        print("login started")
        bot.get('https://twitter.com/i/flow/login?input_flow_data=%7B"requested_variant"%3A"eyJsYW5nIjoiZW4ifQ%3D%3D"%7D')
        time.sleep(3)
        # page_source = bot.page_source
        # soup = BeautifulSoup(page_source,'html.parser')
        email=bot.find_element(By.NAME,'text')
        email.send_keys(self.email)
        button=bot.find_element(By.CSS_SELECTOR,"div[class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu'] span[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")
        button.click()
        time.sleep(3)
        # page_source=bot.page_source
        # soup = BeautifulSoup(page_source,'lxml')
        password = bot.find_element(By.CSS_SELECTOR,"input[name='password']")
        password.send_keys(self.password)
        time.sleep(1)
        button1=bot.find_element(By.XPATH,"(//div[@class='css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0'])[3]")
        button1.click()
        time.sleep(1)
        print("login finished")

    def get_tweets(self, hashtag_list,l): 
        tweets=[]
        username=[]
        bot=self.bot
        
        num=0
        i=0
        while i<len(hashtag_list):
            t=l
            p=0
            hashtag=hashtag_list[i]
            print(hashtag)

                    #https://twitter.com/search?q=hello&src=typed_query
            bot.get('https://twitter.com/search?q=' + hashtag + '&src=typed_query&f=live')
            time.sleep(5)
            if(hashtag==""):
                i+=1
                continue

            while(t>0):
                page_source = bot.page_source
                soup = BeautifulSoup(page_source,'lxml')
                t-=1
                q= soup.find('div',{'class':'css-1dbjc4n'})
                a=q.find_all('div',{'data-testid':'cellInnerDiv'})
                k=1 
                for b in a:
                    u=b.find('div',{'class':'css-1dbjc4n r-zl2h9q'})
                    if(u==None):
                        continue
                    
                    c=u.find('span',{'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
                    #user=remove_non_ascii(c.text)
                    user=c.text.encode('utf-8')


                    w=b.find_all('div',{'dir':'auto'})
                    for z in w:
                        m=z.find('span',{'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
                        if m is not None:                
                            k+=1
                            z=keep_alphabets_and_spaces(remove_extra_spaces(remove_non_ascii(m.text)))
                            if z is not None or z !=" " or z != "  " or z !="   ":
                                tweets.append(z)
                                username.append(user)
                                p+=1
                                print(f"{user} : {z}")
                                #user=user.decode('utf-8')
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
            print(f"number of tweets fetched by {hashtag} = {p}")
            if(p==0):
                self.k+=1
                cv=self.k
                i-=1
                self.login(cv)
                continue
            i+=1
            num+=p
            time.sleep(1)
        
        print(f"total tweets fetched {num} ")
        return tweets,username


       

     

        



            
