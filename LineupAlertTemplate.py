#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pandas as pd
#pd.set_option("display.max_rows", 100, "display.max_columns", 50)
#import numpy as np
#import math
from bs4 import BeautifulSoup
import requests
headers = {'User-Agent':'Mozilla/5.0'}
import smtplib, ssl


# In[55]:

# URL for your first Yahoo fantasy team
url = "https://baseball.fantasysports.yahoo.com/b1/99999/5"

source = requests.get(url,headers=headers)
soup = BeautifulSoup(source.content,'lxml')
teams = [th.findParent() for th in soup.find_all(title='Not in Starting Lineup')]
teams = [th.findParent() for th in teams]
teams = [th.findParent() for th in teams]
teams = [th.getText() for th in teams]

gameOn = ['Top','Bot','W,','L,','Mid']

if teams:
    df= pd.DataFrame(teams)
    df[0] = df[0].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df= df[0].str.rsplit('\n',n=10,expand=True)
    df[8]="League Name 1"
    df[9]=df[7].str.contains('|'.join(gameOn))

if not teams:
    column_names=[0,2,8,9]
    df = pd.DataFrame(columns=column_names)


# In[56]:

# URL for your second Yahoo fantasy team
url2 = "https://baseball.fantasysports.yahoo.com/b1/99999/5"

source2 = requests.get(url2,headers=headers)
soup2 = BeautifulSoup(source2.content,'lxml')
teams2 = [th2.findParent() for th2 in soup2.find_all(title='Not in Starting Lineup')]
teams2 = [th2.findParent() for th2 in teams2]
teams2 = [th2.findParent() for th2 in teams2]
teams2 = [th2.getText() for th2 in teams2]

if teams2:
    df2= pd.DataFrame(teams2)
    df2[0] = df2[0].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df2= df2[0].str.rsplit('\n',n=10,expand=True)
    df2[8]="League Name 2"
    df2[9]=df2[7].str.contains('|'.join(gameOn))

if not teams2:
    column_names=[0,2,8,9]
    df2 = pd.DataFrame(columns=column_names)


# In[57]:


frames=[df,df2]
dfMaster = pd.concat(frames)


# In[58]:


dfMaster=dfMaster[[0,2,8,9]]

dfMaster = dfMaster[dfMaster[9]!=True]
dfMaster = dfMaster[dfMaster[0]!='BN ']
dfMaster = dfMaster[dfMaster[0]!='IL ']
dfMaster = dfMaster[dfMaster[0]!='SP ']
dfMaster = dfMaster[dfMaster[0]!='RP ']
dfMaster = dfMaster[dfMaster[0]!='P ']

#dfMaster


# In[6]:


class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "[sending email address]"
        self.password = "[app password goes here]"
        

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject:{subject}\n{content}")
        service.quit()


if __name__ == '__main__':
    #mails = input("[receiving email address]").split()
    #subject = input("Benched players in the starting lineup")
    #content = input("Enter content: ")
    mails = "[receiving email address]".split()
    subject = "Benched players in the starting lineup"
    content = dfMaster

    mail = Mail()
    if len(dfMaster.index)>0:
        mail.send(mails, subject, content)

