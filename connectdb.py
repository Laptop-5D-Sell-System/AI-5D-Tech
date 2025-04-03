import pyodbc
import sys
import pandas as pd 
import json
from decimal import Decimal
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'NQD-Desktop\\MSSQLSERVER01'
DATABASE_NAME = '5D-TECH'
USER_NAME = "5d-tech"
PASSWORD = 'x1@'

# Connection string
connection_string = f"""
DRIVER={DRIVER_NAME};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
UID={USER_NAME};
PWD={PASSWORD};
TrustServerCertificate=yes;
"""

# Create connection
def connect_db(connection_string):
	conn = pyodbc.connect(connection_string)
	cursor = conn.cursor()
	return conn, cursor

# Close connection
def close_db(conn, cursor):
	cursor.close()
	conn.close()

# Query to db
def query(query):
    try:
        conn, cursor = connect_db(connection_string)
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as ex:
        return f"Có lỗi xảy ra:  + {ex}"
    finally:
        if 'conn' in locals() and 'cursor' in locals(): 
            close_db(conn, cursor)
	

data_from_sql = query("SELECT * FROM tbl_Products")
columns = ["id", "name", "description", "price", "product_image", "stock_quantity", "category_id", "created_at", "updated_at"]

# Chuyển tuples thành list of dicts
data_json = [
    dict(zip(columns, [float(value) if isinstance(value, Decimal) else value for value in row])) 
    for row in data_from_sql
]
