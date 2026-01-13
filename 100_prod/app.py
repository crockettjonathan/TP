import sqlite3
import pandas as pd
from flask import Flask, render_template, request, Response, jsonify
import io
from datetime import datetime # Required for timestamp
from pathlib import Path

# 1a. Get the directory of the notebook (in Jupyter)
current_dir = Path.cwd()
# 1b. Get the directory where the current script is located (non jupyter)
#current_dir = Path(__file__).resolve().parent

#define connection to DB
db_path = current_dir.parent / "100_prod" / "trust.db"

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect(db_path)

def get_query_config(category, sub_category):
    """
    Define column order here. 
    The order in these strings determines the order in the UI and CSV.
    """
    if category == "Business":
        # Business Order: 
        cols = ["Business_Name", "Reviewer_Name", "Review_Title", "Review_Rating", "Review_Content", "Review_IP_Address", "Reviewer_Country", "Review_Date", "Review_Id"]
        filter_col = "Business_Name"
    elif category == "User" and sub_category == "Reviews":
        # User Reviews Order: 
        cols = ["Reviewer_Name", "Business_Name", "Review_Title", "Review_Rating", "Review_Content", "Review_IP_Address", "Reviewer_Country", "Review_Date", "Review_Id"]
        filter_col = "Reviewer_Name"
    else: # User -> Account Info
        # Account Info Order: 
        cols = ["Reviewer_Name", "Reviewer_Country", "Email_Address", "Review_IP_Address", "Reviewer_ID"]
        filter_col = "Reviewer_Name"
        
    return cols, filter_col

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview_data():
    data = request.json
    cols_list, filter_col = get_query_config(data['category'], data.get('sub_category'))
    
    conn = get_db_connection()
    cols_str = ", ".join(cols_list)
    query = f"SELECT {cols_str} FROM sql_tp_reviews_dedup WHERE {filter_col} LIKE ? LIMIT 50"
    
    try:
        df = pd.read_sql_query(query, conn, params=(f"%{data['search_term']}%",))
        conn.close()
        
        # Force the exact order from your config list
        df = df[cols_list]
        
        # We return the column names and the data separately to guarantee order
        return jsonify({
            "columns": cols_list,
            "rows": df.values.tolist() # Converts data to a simple list of lists
        })
    except Exception as e:
        if conn: conn.close()
        return jsonify({"error": str(e)}), 400

@app.route('/export', methods=['POST'])
def export_data():
    # 1. Capture Form Data
    category = request.form.get('category')
    sub_category = request.form.get('sub_category') or "None"
    search_term = request.form.get('search_term')
    
    # 2. Get Ordered Column List and Filter Column
    cols_list, filter_col = get_query_config(category, sub_category)
    
    # 3. Build SQL Query using the specific column order
    cols_str = ", ".join(cols_list)
    query = f"SELECT {cols_str} FROM sql_tp_reviews_dedup WHERE {filter_col} LIKE ?"
    
    conn = get_db_connection()
    try:
        # Load into DataFrame
        df = pd.read_sql_query(query, conn, params=(f"%{search_term}%",))
    finally:
        conn.close()

    # 4. Final Re-index (Double safety to ensure order matches cols_list)
    df = df[cols_list]

    # 5. Filename Construction
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_cat = category.replace(" ", "_")
    clean_sub = sub_category.replace(" ", "_")
    clean_search = search_term.replace(" ", "_")
    filename = f"{timestamp}_{clean_cat}_{clean_sub}_{clean_search}.csv"

    # 6. Stream CSV Response
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

if __name__ == '__main__':
    app.run(debug=True)