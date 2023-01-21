import csv
import streamlit as st
import datetime
import time
import pandas as pd
import snscrape.modules.twitter as sntwitter
import pymongo
import os.path
import json


st.set_page_config(page_title="Twitter Scraping",page_icon=":tada",layout='wide')
header = st.container()
with header:
    st.title("Twitter Scrapping Using snscrape with python")
    st.header("To Extract Enter The Values")
    st.markdown("""Format for input should be : "**its the elephant since:2020-06-01 until:2020-07-31** """)
    keyword = st.text_input("Username")
    tweet_count = st.number_input("Tweet Count",min_value=None,max_value=None)
    current_time = time.ctime()

def Create():
    d = filter_data()
    tweets_df1 = pd.DataFrame(d, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    tweets_df1.to_csv('user-tweets.csv',sep=',', index=False)

def File_Check():
    file_exist = os.path.exists('D:/Practice/user-tweets.csv')
    if file_exist == False:
        Create()
    else:
        check_Duplicate()

def filter_data():
    tweets_list1 = []
    # Using TwitterSearchScraper to scrape data
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword}').get_items()):
        if i > tweet_count:
            break
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang])
    return tweets_list1

def Append():
    d1 = filter_data()
    tweets_df2 = pd.DataFrame(d1)
    tweets_df2.to_csv('user-tweets.csv',sep=',',mode='a', index=False,header=False)

def check_Duplicate():
    Append()
    check = pd.read_csv('D:/Practice/user-tweets.csv')
    df1 = check.drop_duplicates(keep='first')
    df1.to_csv('user-tweets.csv', sep=',', index=False, header=True)

def checkExistence_DB(DB_NAME, client):
    """It verifies the existence of DB"""
    DBlist = client.list_database_names()
    if DB_NAME in DBlist:
        print(f"DB: '{DB_NAME}' exists")
        return True
    print(f"DB: '{DB_NAME}' not yet present present in the DB")
    return False


def upload_to_DB():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    df = filter_data()
    saving = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    saving.to_csv('show_value.csv', sep=',', index=False, header=False)
    if checkExistence_DB(DB_NAME="mydatabase", client=myclient) == True:
        db = myclient["mydatabase"]
        COLLECTION_NAME = keyword
        df1 = pd.read_csv('D:/Practice/show_value.csv')
        collection = db[COLLECTION_NAME+"_"+str(current_time)+"_"+str(len(df1.values))+"_"+"Records Created"]
        for ind, row in df1.iterrows():
            x = collection.insert_many([row.to_dict()])
    else:
        db = myclient["mydatabase"]
        COLLECTION_NAME = keyword
        df2 = pd.read_csv('D:/Practice/show_value.csv')
        collection = db[COLLECTION_NAME+"_"+str(current_time)+"_"+str(len(df2.values))+" - Records Created"]
        for ind, row in df2.iterrows():
            x = collection.insert_many([row.to_dict()])

def convert_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

col1, col2, col3= st.columns(3)

# Custom Button For Submit Action
with col1:
    submit = st.button('Submit')
    if submit:
        File_Check()
        st.success('Data filtered Successfully', icon="✅")

# Custom Button For Viewing DataFrame
show = st.button('Show DF')
if show:
    df = filter_data()
    tweets_df1 = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    st.dataframe(tweets_df1)

#Custom Button For DB Upload
with col2:
    upload = st.button('Upload To DB')
    if upload:
        upload_to_DB()
        st.success('Uploaded To DB', icon="✅")

#Custom Button For Download Option
with col3:
    option = st.selectbox(
        'How would you like to download!!',
        ('Json','CSV'))
    df = filter_data()
    tweets_df1 = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    if option == 'CSV':
        csv = convert_csv(tweets_df1)
        st.download_button("Download",data=csv,file_name='keyword.csv',mime='text/csv')
    else:
        df1 = tweets_df1.to_json(orient="index")
        st.download_button("Download", data=df1, file_name='keyword.json', mime='text/json')