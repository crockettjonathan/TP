# TrustPilot Review Exporter
A lightweight web application built with Flask and SQLite3 (This database choice was used for simplicity, but any alterntive could be easily retrofitted in) to filter, preview, and export trustpilot review data. This tool allows users to dynamically switch between "Business" and "User" contexts, preview results in the browser, and download a custom-named CSV file.

## 🚀 Features
***Security***: Uses parameterized SQL queries to prevent SQL injection.

### Frontend only features
***Dynamic UI***: Second-level dropdowns appear only when "User" is selected.

***Live Preview***: View the top 50 results in an HTML table before downloading.

***Smart Filenaming***: Exported CSVs are automatically named with a timestamp and search parameters (e.g., 20260113_153000_User_Reviews_John_Doe.csv).

***Keyboard Friendly***: Pressing Enter in the search box triggers the preview immediately.


## 🛠️ Setup Instructions
### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Installation
Clone this repository or download the source code, then install the required dependencies:

```
pip install flask pandas
```

If you want to call the API via python then please also run the following:

```
pip install requests
```

### 3. Project Structure
Your directory must look like this for the Flask templates to load correctly:

```
.
├── app.py                           # Flask Backend
├── trust.db                         # SQLite Database (created using setup.py)
├── call.py                          # an example call of the API from Python
├──  010_source_data/
│    └── tp_reviews.csv              # Source data
│
├──  050_data_review/
│    └──Data_import_cleanse.ipynb    # A Jupyter Notebook used to review the data
│
├──  075_setup/
│    ├── db_dc.py                    # Close DB connection
│    └── setup.py                    # Python ETL
│
└── templates/
     └── index.html                  # Frontend Logic
```

### 4. Database Preparation - Not required, included for reference
*This step has been included to show how the database was established using the data provided. This step has already been run and the database is present in the repo ready for use.*

Navigate to the setup folder (\repo\075_setup) in your terminal and run the following to import the data, cleanse it and prepare the database for the application. The code contains a section to drop the precleansed data to save on space if this is a concern:

```
python setup.py
```

The application expects a table named sql_tp_reviews_dedup with the following columns (at minimum):

Business_Name
Reviewer_Name
Review_Title
Review_Rating
Review_Content
Review_Date
Review_Id
Email_Address
Reviewer_ID

## 📘 Definitions

The API has 3 inputs

1. **category**: This can be either *"Business"* or *"User"*, and defines if the data is filtered on *"Business_Name"* or *"Reviewer_Name"* respectively
2. **sub_category**: If category is *"Business"* then sub category is ignored, if category is *"User"* then if sub_category is *"Reviews"* it will out put reviews for this user, any other value and it will output Account Info.
3. **search_term**: this is the value which will be searched on the relative column as defined in *"category"*, and will do a fuzzy matching search to bring back names containing the search_term

## 🖥 Usage
Start the Server: Run the following command in your terminal from the repo:

```
python app.py
```

Once running, the API be accessed via an HTML frontend (example included) or using standard HTML protocols. Below are some examples to use the API:

### Example Front End

Access the Web Interface: Open your browser and navigate to: http://127.0.0.1:5000

***Search & Filter***:

Select Business or User from the dropdown.

If User is selected, choose between Reviews or Account Info.

Enter a name in the text box and press Enter or click Show Preview.

***Export***:

If results are found, a Download Full CSV button will appear. Click it to save the results to your computer.

### Example cURL calls

An example to filter for Businesses which contain "Artisan" and output Reviews to a CSV called "my_export.csv"
```
curl -X POST http://127.0.0.1:5000/export -d "category=Business" -d "search_term=Artisan" --output my_export.csv
```

An example to filter for Users which contain "Donna" and output Reviews to a CSV called "my_export.csv"
```
curl -X POST http://127.0.0.1:5000/export -d "category=User" -d "sub_category=Reviews" -d "search_term=Donna" --output my_export.csv
```

An example to filter for Users which contain "Donna" and output Account Info to a CSV called "my_export.csv"
```
curl -X POST http://127.0.0.1:5000/export -d "category=User" -d "sub_category=Account Info" -d "search_term=Donna" --output my_export.csv
```

### Example Python call

Here is an example using the requests library to access the API, to adjust filters comment/uncomment the appropriate lines (this has been included in the base directory):

```
import requests
import re

url = "http://127.0.0.1:5000/export"
payload = {
    "category": "Business",
    #"category": "User",
    #"sub_category": "Reviews",
    #"sub_category": "Account Info",
    "search_term": "Artisan"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    # Get filename from the Content-Disposition header
    d = response.headers.get('content-disposition')
    fname = re.findall("filename=(.+)", d)[0]
    
    with open(fname, "wb") as f:
        f.write(response.content)
    print(f"Saved as: {fname}")
else:
    print(f"Error: {response.status_code}")
```

## 📝 Configuration Note
The column subsets for different views are defined in the get_query_config function within app.py. You can modify this function to add or remove columns, and adjust the order they will appear, from the export as the database schema evolves.

## 🛡️ Troubleshooting
***Site can't be reached***: Ensure you are using http:// and not https://.

***Template Not Found***: Ensure your index.html is inside a folder named templates.

***Port 5000 in use***: If another app is using the port, change the port in app.py (last line of code):

```
app.run(debug=True, port=5001)
```