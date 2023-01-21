# Capstone_Project_21-01-2023
Our Task is to create a twitter scrapper using Python, MongoDB, Pandas and Streamlit.

At the beginning stage we created a header container where we used to declare the Title, Header, keyword streamlit. 

Then I have created a functions for filtering the data **filter_data()** from Twitter then creating a data frame for it then appending it in a CSV file.
Before that we should make sure that the CSV file is already created. If not then it will create a CSV file then we are checking for any kind of duplicate data in CSV file if so we will remove it.

Now we have filtered the data from Twitter and stored in a CSV file.

Next step is to store it in a database for that we are using **MongoDB**. so now we have to check whether the database is already present or not for that we have to declare a function called **CheckExistence_DB** this function returns a boolean value. So if it is true then we'll use the database which is present inside and will create a collection naming it same as the **keyword** which we are going to scrap from the Twitter and then we're adding it to into the database along with the current time stamp and length of the records.

if the database is not present in that case we will create a new database and we will create a collection inside it and then we will insert the records along with the **current_timestamp**.

Now we have to create buttons for the web page. we Will be creating 4 buttons Submit, Show_DF, Upload_DB, Download. 

1.) Submit button will perform the data filteration action.
2.) Show_DF will display the DataFrame filtered at the moment in the browser.
3.) Upload_DB will upload the filtred data into the Mongo_DB which we created.
4.) Download Button will give us the option to download the data into CSV as well as JSON Format.
