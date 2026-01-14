# Development Approach:

I used Jupyter Notebooks to import the data and review it, checking for NULLs and duplication in the data. I then built up the code to stand up the SQLite database (as a proxy for whatever DB the data would be in) to store the data in the provided CSV, and validated the duplication through SQL queries. Once this was done I used Pandas to dedup the dataframe and push this to the database.
I then used Gemini to produce a shell script and HTML frontend for the API using the following prompt:
 
*"I have a sqlite database called trust.db which contains a table called sql_tp_reviews_dedup, I want to develop an HTML front end and Python API to filter this table and output the results to a csv. The user will choose from a drop down which offers two options "Business" and "User", if they select "User" they should then get a further drop down which asks if they want "Reviews" or "Account Info". If the user chooses "Business" or "User" and "Reviews" they will get one subset of columns. If the user selects "User" and "Account Info" they will get a different subset of columns. The columns in the Database which relates to "Business" is called "Business_Name" and the column which relates to "User" is called "Reviewer_Name""*

I updated the HTML to include a free text search box for the users input, and updated the Python to include a search_term parameter for the queries

I then used Gemini to generate the preview functionality for the UI as when testing I found it frustrating not seeing the potential output until I checked the CSV.

After two exports I realised I wanted to have the files be named automatically so that they were unique and descriptive, so I added in some logic to build a filename using datetime and the users inputs.

I then developed example calls for cURL and Python for additional use cases for the API which I included in the Readme in github

# Issues encountered:

The preview and output were using the index of the columns as opposed to the order I had specified in the Python. This was an easy enough fix in Python to generate the columns in the required order with a defined List, but I had issues with this still not lining up in the UI preview. Javascript is not my forte so I used Gemini to identify the issue which was with the javascript processing being cached, so it provided logic to allow the order to be forced. As a by product of this the download CSV button no longer showed up due to the previous code only showing the button when the preview had results, whose method was no longer compatible with the changes to force the order of the columns. Gemini again provided the fix to still provide the functionality, but with compatibility on the new logic to order the columns correctly.

After testing on a seperate environment some of the folder structure and path logic was updated to allow for the app to be called in different locations

# Considerations and choices:

When deciding on a mechanism to run I considered if simplicity for reviewer, or real world application should be prioritised. By this I mean if the application should be called in a shell script which checks for dependencies and installs them each time the application is initiated. This adds convenience by not having to install the supporting libraries, however they are single instance tasks. So I seperated out these steps, so that they don't run redundantly each time the application is started following initial setup. I see this as back end performance over convenience.

# Notes: 
I use the pathlib libarary throughout to allow for data and scripts to be stored in sibling directories, but then referenced without hardcoding paths for transportability.