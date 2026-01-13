#import required libaries
import pandas as pd
from pathlib import Path
import sqlite3

#Read in CSV and review for nulls

# Get the directory of the notebook (in Jupyter)
#current_dir = Path.cwd()

# Get the directory where the current script is located (non jupyter)
current_dir = Path(__file__).resolve().parent

# Define path to the sibling folder and source data
csv_path = current_dir.parent / "010_source_data" / "tp_reviews.csv"

# 
tp_reviews=pd.read_csv(csv_path)

# replace spaces in the column names with an underscore for best practice naming conventions in DB
tp_reviews.columns = tp_reviews.columns.str.replace(' ', '_')

# define connection to DB
db_path = current_dir.parent / "100_prod" / "trust.db"
conn=sqlite3.connect(db_path)

#create table in DB
tp_reviews.to_sql('sql_tp_reviews',conn,if_exists='replace',index=False)

#Remove duplicates and create deduplicated data within the database
tp_reviews_dedup=tp_reviews.drop_duplicates(subset=['Review_Id'])
tp_reviews_dedup.to_sql('sql_tp_reviews_dedup',conn,if_exists='replace',index=False)

###optional code to drop original data if not required for reference purposes
#cursor = conn.cursor()
#sql_query = f"DROP TABLE IF EXISTS {sql_tp_reviews}"
#cursor.execute(sql_query)
#conn.commit()

#Close connection to the DB
conn.close()