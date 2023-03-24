import streamlit as st
import datetime
import time
import pandas as pd
import snscrape.modules.twitter as sntwitter
import pymongo
import os.path


# Streamlit Page Configuration.
st.set_page_config(page_title="Twitter Scraping",page_icon=":tada",layout='wide')
header = st.container()
with header:
    st.title("Twitter Scrapping Using snscrape with python")
    st.header("To Scrap Enter The Keyword")
    font = "Keyword"
    keyword = st.text_input(f"Enter The Keyword",font)
    start = st.date_input("select the start date",datetime.date(2022,1,1))
    end = st.date_input("select the end date",datetime.date(2023,2,15))
    tweet_count = st.slider('Tweet count', 0, 100, 1)
    current_time = time.ctime()
#st.number_input("Tweet Count",min_value=None,max_value=None)

# Creating A CSV File For The Extracted Data.
def Create():
    d = filter_data()
    tweets_df1 = pd.DataFrame(d, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    tweets_df1.to_csv('D:\Assignments\Capstone - 2/user-tweets.csv',sep=',', index=False)

# Checking Whether the File Exist Or Not.
def File_Check():
    file_exist = os.path.exists('D:\Assignments\Capstone - 2/user-tweets.csv')
    if file_exist == False:
        Create()
    else:
        check_Duplicate()

# Scrapping Data from Twitter Using SNSCRAPE Library.
def filter_data():
    tweets_list1 = []
    # Using TwitterSearchScraper to scrape data
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword},since:{start} until:{end}').get_items()):
        if i > tweet_count:
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang])
    return tweets_list1

# Appending Data to The Existing File.
def Append():
    d1 = filter_data()
    tweets_df2 = pd.DataFrame(d1)
    tweets_df2.to_csv('D:\Assignments\Capstone - 2/user-tweets.csv',sep=',',mode='a', index=False,header=False)

#Checking For Duplicate Values.
def check_Duplicate():
    Append()
    check = pd.read_csv('D:\Assignments\Capstone - 2/user-tweets.csv')
    df1 = check.drop_duplicates(keep='first')
    df1.to_csv('D:\Assignments\Capstone - 2/Values.csv', sep=',', index=False, header=True)

# Checking Whether Database is Already Present Or Not Returns a Boolean Value.
def checkExistence_DB(DB_NAME, client):
    """It verifies the existence of DB"""
    DBlist = client.list_database_names()
    if DB_NAME in DBlist:
        print(f"DB: '{DB_NAME}' exists")
        return True
    print(f"DB: '{DB_NAME}' not yet present present in the DB")
    return False

# Connecting MongoDb With Pycharm Using Pymongo Library And Entering Collections into it.
def upload_to_DB():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    df = filter_data()
    saving = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    saving.to_csv('show_value.csv', sep=',', index=False, header=False)
    if checkExistence_DB(DB_NAME="mydatabase", client=myclient) == True:
        db = myclient["mydatabase"]
        COLLECTION_NAME = keyword
        df1 = pd.read_csv('D:\Assignments\Capstone - 2/user-tweets.csv')
        collection = db[COLLECTION_NAME+"_"+str(current_time)+"_"+str(len(df1.values))+"_"+"Records Created"]
        for ind, row in df1.iterrows():
            x = collection.insert_many([row.to_dict()])
    else:
        db = myclient["mydatabase"]
        COLLECTION_NAME = keyword
        df2 = pd.read_csv('D:\Assignments\Capstone - 2/user-tweets.csv')
        collection = db[COLLECTION_NAME+"_"+str(current_time)+"_"+str(len(df2.values))+" - Records Created"]
        for ind, row in df2.iterrows():
            x = collection.insert_many([row.to_dict()])

# Converting DataFrame File To CSV File.
def convert_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun.
    return df.to_csv().encode('utf-8')

# Creating Button Placement Fields.

col1, col2, col3= st.columns(3)

# Custom Button For Submit Action.
with col1:
    submit = st.button('Submit')
    if submit:
        File_Check()
        st.success('Data filtered Successfully', icon="✅")

# Custom Button For Viewing DataFrame.
show = st.button('Show DF')
if show:
    df = filter_data()
    tweets_df1 = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    st.dataframe(tweets_df1)

# Custom Button For DB Upload.
with col2:
    upload = st.button('Upload To DB')
    if upload:
        upload_to_DB()
        st.success('Uploaded To DB', icon="✅")

# Custom Button For Download Option.
with col3:
    option = st.selectbox(
        'How would you like to download!!',
        ('Json','CSV'))
    df = filter_data()
    tweets_df1 = pd.DataFrame(df, columns=['Date', 'Tweet Id', 'Tweet Content', 'User_Name', 'Language'])
    # To Download as CSV.
    if option == 'CSV':
        csv = convert_csv(tweets_df1)
        st.download_button("Download",data=csv,file_name='keyword.csv',mime='text/csv')
    # To Download as JSON.
    else:
        df1 = tweets_df1.to_json(orient="index")
        st.download_button("Download", data=df1, file_name='keyword.json', mime='text/json')


