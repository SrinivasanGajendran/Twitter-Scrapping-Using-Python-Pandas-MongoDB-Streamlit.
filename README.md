# Capstone_Project_21-01-2023
# Twitter Scrapping Using Python, Pandas, MongoDB & Streamlit.
# IDE - Pycharm

Our Task is to create a twitter scrapper using Python, MongoDB, Pandas and Streamlit.

Packages used:
Streamlit, Pandas, Snscrape, Pymongo(Used to work in MongoDb). 

First stage we created a header container where we used to declare the Title, Header, and the user input using streamlit. 

Then I have created a functions for filtering the data **filter_data()** from Twitter then creating a data frame for it and then appending it in a CSV file.
Before that we should make sure that the CSV file is already created or not for that we use **File_Check() & Create()**.
If its not present then it will create a CSV file at the location where program is presented. we are checking for any kind of duplicate data in CSV file if so we will remove it for that we will use **Check_Duplicate()**.

Now we have filtered the data from Twitter and stored in a CSV file.

Next step is to store it in a database for that we are using **MongoDB**. so now we have to check whether the database is already present or not for that we have to declare a function called **CheckExistence_DB** this function returns a boolean value. So if it is true then we'll use the database which is present inside and will create a collection naming it same as the **keyword** which we are going to scrap from the Twitter and then we're adding it to into the database along with the current time stamp and length of the records.

if the database is not present in that case we will create a new database and we will create a collection inside it and then we will insert the records along with the **current_timestamp**.

Now we have to create buttons for the web page. we Will be creating 4 buttons Submit, Show_DF, Upload_DB, Download. 

1.) Submit button will perform the data filteration action.
2.) Show_DF will display the DataFrame filtered at the moment in the browser.
3.) Upload_DB will upload the filtred data into the Mongo_DB which we created.
4.) Download Button will give us the option to download the data into CSV as well as JSON Format.
