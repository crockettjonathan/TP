#import required libaries
import pandas as pd
from pathlib import Path
import sqlite3

# Get the directory where the current script is located
current_dir = Path(__file__).resolve().parent

# define connection to DB
db_path = current_dir.parent / "trust.db"
conn=sqlite3.connect(db_path)

#Close connection to the DB
conn.close()