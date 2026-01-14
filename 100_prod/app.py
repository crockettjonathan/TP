##import libraries
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, Response, jsonify
import io
from datetime import datetime # Required for timestamp
from pathlib import Path

#Get the directory of the notebook (in Jupyter)
current_dir = Path.cwd()

#define connection to DB
db_path = current_dir.parent / "100_prod" / "trust.db"

app = Flask(__name__)

#define function for db connection
def get_db_connection():
    return sqlite3.connect(db_path)

#define function to select required columns and column to filter on based on selection on the front end
def get_query_config(category, sub_category):
    """
    Define column order here. 
    The order in these strings determines the order in the UI and CSV.
    """
    if category == "Business":
        #Business Order: 
        cols = ["Business_Name", "Reviewer_Name", "Review_Title", "Review_Rating", "Review_Content", "Review_IP_Address", "Reviewer_Country", "Review_Date", "Review_Id"]
        filter_col = "Business_Name"
    elif category == "User" and sub_category == "Reviews":
        #User Reviews Order: 
        cols = ["Reviewer_Name", "Business_Name", "Review_Title", "Review_Rating", "Review_Content", "Review_IP_Address", "Reviewer_Country", "Review_Date", "Review_Id"]
        filter_col = "Reviewer_Name"
    else: # User -> Account Info
        #Account Info Order: 
        cols = ["Reviewer_Name", "Reviewer_Country", "Email_Address", "Review_IP_Address", "Reviewer_Id"]
        filter_col = "Reviewer_Name"
        
    return cols, filter_col

#define function to refence html for interface
@app.route('/')
def index():
    return render_template('index.html')

#define function data to be returned for the front end preview
@app.route('/preview', methods=['POST'])
def preview_data():
    #Build query based on form data
    data = request.json
    cols_list, filter_col = get_query_config(data['category'], data.get('sub_category'))
    
    conn = get_db_connection()
    cols_str = ", ".join(cols_list)
    query = f"SELECT {cols_str} FROM sql_tp_reviews_dedup WHERE {filter_col} LIKE ? LIMIT 50"
    
    try:
        #Query data based on query built above
        df = pd.read_sql_query(query, conn, params=(f"%{data['search_term']}%",))
        conn.close()
        
        # Force the exact order from your config list (so as not to simply use index)
        df = df[cols_list]
        
        #Return the column names and the data separately to guarantee order
        return jsonify({
            "columns": cols_list,
            "rows": df.values.tolist() #Converts data to a simple list of lists
        })
    except Exception as e:
        if conn: conn.close()
        return jsonify({"error": str(e)}), 400

#define function 
@app.route('/export', methods=['POST'])
def export_data():
    #Capture form data
    category = request.form.get('category')
    sub_category = request.form.get('sub_category') or "None"
    search_term = request.form.get('search_term')
    
    #Get Ordered Column List and Filter Column
    cols_list, filter_col = get_query_config(category, sub_category)
    
    #Build SQL Query using the specific column order
    cols_str = ", ".join(cols_list)
    query = f"SELECT {cols_str} FROM sql_tp_reviews_dedup WHERE {filter_col} LIKE ?"
    
    conn = get_db_connection()
    try:
        #Load into DataFrame
        df = pd.read_sql_query(query, conn, params=(f"%{search_term}%",))
    finally:
        conn.close()

    #Final Re-index (Double safety to ensure order matches cols_list)
    df = df[cols_list]

    #Filename Construction (so is unique and doesn't have any spaces in the file name (pet peeve))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_cat = category.replace(" ", "_")
    clean_sub = sub_category.replace(" ", "_")
    clean_search = search_term.replace(" ", "_")
    filename = f"{timestamp}_{clean_cat}_{clean_sub}_{clean_search}.csv"

    #Stream CSV Response
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    #return csv using naming convention and ordered defined above
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

if __name__ == '__main__':
    app.run(debug=True)