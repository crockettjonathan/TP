# TrustPilot Review Exporter
A lightweight web application built with Flask and SQLite3 (This database choice was used for simplicity, but any alterntive could be easily retrofitted in) to filter, preview, and export trustpilot review data. This tool allows users to dynamically switch between "Business" and "User" contexts, preview results in the browser, and download a custom-named CSV file.

## 🚀 Features
**Dynamic UI**: Second-level dropdowns appear only when "User" is selected.

**Live Preview**: View the top 50 results in an HTML table before downloading.

**Smart Filenaming**: Exported CSVs are automatically named with a timestamp and search parameters (e.g., 20260113_153000_User_Reviews_John_Doe.csv).

**Keyboard Friendly**: Pressing Enter in the search box triggers the preview immediately.

**Security**: Uses parameterized SQL queries to prevent SQL injection.

## 🛠️ Setup Instructions
### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Installation
Clone this repository or download the source code, then install the required dependencies:

pip install flask pandas

### 3. Project Structure
Your directory must look like this for the Flask templates to load correctly:

```
.
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
└── 100_prod/
    ├── app.py                       # Flask Backend
    ├── trust.db                     # SQLite Database (created using setup.py)
    └── templates/
        └── index.html               # Frontend Logic
```

### 4. Database Preparation
Navigate to the setup folder (\repo\075_setup) in your terminal and run the following to import the data, cleanse it and prepare the database for the application. The code contains a section to drop the precleansed data to save on space if this is a concern:

python setup.py

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

## 🖥 Usage
Start the Server: Run the following command in your terminal:

python app.py

Access the Web Interface: Open your browser and navigate to: http://127.0.0.1:5000

**Search & Filter**:

Select Business or User from the dropdown.

If User is selected, choose between Reviews or Account Info.

Enter a name in the text box and press Enter or click Show Preview.

**Export**:

If results are found, a Download Full CSV button will appear. Click it to save the results to your computer.

## 📝 Configuration Note
The column subsets for different views are defined in the get_query_config function within app.py. You can modify this function to add or remove columns, and adjust the order they will appear, from the export as the database schema evolves.

## 🛡️ Troubleshooting
**Site can't be reached**: Ensure you are using http:// and not https://.

**Template Not Found**: Ensure your index.html is inside a folder named templates.

**Port 5000 in use**: If another app is using the port, change the port in app.py (last line of code):

app.run(debug=True, port=5001)