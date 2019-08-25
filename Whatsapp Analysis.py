#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dateutil
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates


# In[ ]:


file = open('Put_your_text_file_location_here.txt',encoding="utf-8")
lines = file.readlines()


# In[ ]:


#convert the list and add delimiter
linem,linem1,linem2,linem3 = [],[],[],[]
for i in range(0,len(lines)):
    linem.append(lines[i].replace(',',' ',1))
for i in range(0,len(linem)):
    linem1.append(linem[i].replace('-','|',1))
for i in range(0,len(linem1)):
    linem2.append(linem1[i].replace(':','|',2))
for i in range(0,len(linem2)):
    linem3.append(linem2[i].replace('|',':',1))


# In[ ]:


y = []
date,time,sign,sender,message = [],[],[],[],[]
print(len(date),type(date))
#break strings on basis of delimiter
#convert each category to lists
for i in range(0,(len(linem3))):
    y = str(linem3[i]).split('|',2)
    if (len(y)) is 3:
        date.append(y[0])
        sender.append(y[1])
        message.append(y[2])
NewList = [date,sender,message]


# In[ ]:


messages = []
for i in range(0,len(message)):
    messages.append(message[i].replace('\n',''))


# In[ ]:


#convert list to dataframe
data_tuples = list(zip(date,sender,messages))
df = pd.DataFrame(data_tuples, columns=['Date','Sender','Message'])
df.count()


# In[ ]:





# In[ ]:


#data cleaning
df['Sender'] = df['Sender'].str.strip()

#from datetime import datetime 
df['datetime'] = pd.to_datetime(df['Date'],infer_datetime_format=True,errors='coerce')

#drop data from 
df.dropna(subset=['datetime'],axis=0,inplace=True)

##adds diffrent columns using existing dates
df['Year'] = df['datetime'].dt.strftime('%Y')
df['Month'] = df['datetime'].dt.strftime('%b')
df['day_month_year'] = pd.to_datetime(df['datetime']).dt.to_period('D')
df['Day'] = df['datetime'].dt.strftime('%d')
df['WeekDay'] = df['datetime'].dt.strftime('%a')
df['Hour'] = df['datetime'].dt.strftime('%H')
df['day_month_year'] = df['day_month_year'].values.astype('datetime64[D]')


# In[ ]:


names=[]
for name in df['Sender'].unique():
    names.append(name)
    
users = df['Sender'].unique() 


# In[ ]:


#bar describing frequency per user over the week
fig, ax = plt.subplots(figsize=(16,7))
sns.countplot(x='WeekDay', hue='Sender', data=df)


# In[ ]:


#bar plot for frequency on basis of hour per day
fig, ax = plt.subplots(figsize=(16,7))
sns.countplot(x='Hour', hue='Sender', data=df)


# In[ ]:


countofwords = []

for sentence in df['Message']:
    counter = len(sentence.split())
    countofwords.append(counter)

df['Countofmessages'] = countofwords
df.groupby(['WeekDay','Sender']).sum()["Countofmessages"].reset_index()


# In[ ]:


#box plot which contains all the frequency of messages over the time for all users

df3 = df.groupby(['day_month_year','Sender']).sum()["Countofmessages"].reset_index()
df3['day_month_year'] = pd.to_datetime(df3['day_month_year'])
df3['WeekDay'] = df3['day_month_year'].dt.strftime('%a')
df3.groupby(['WeekDay','Sender']).sum()["Countofmessages"]
users = df3['Sender'].unique()
df3_user1 = df3.query("Sender == @users[0]")
df3_user2 = df3.query("Sender == @users[1]")


sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(16,7))
ax = sns.boxplot(x="WeekDay", y="Countofmessages", data=df3_user1, palette="Set3")

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(16,7))
ax = sns.boxplot(x="WeekDay", y="Countofmessages", data=df3_user2, palette="Set3")


# In[ ]:


#boxplot comparison of frequency of message over the week
fig, ax = plt.subplots(figsize=(16,7))
ax = sns.boxplot(x="WeekDay", y="Countofmessages", hue="Sender",data=df3, palette="Set3")


# In[ ]:


#boxplot comparison of frequency of message for users and observe outliers
fig, ax = plt.subplots(figsize=(16,7))
ax = sns.boxplot(y="Sender", x="Countofmessages",orient="h",data=df3, palette="Set3", showfliers=True)

