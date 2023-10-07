from flask import Flask, render_template, request, redirect
import pandas as pd
import random
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, inspect


app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('base.html', name = "Fahima")

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/random')
def randomnumber():
    number_var = random.randint(1, 10000)
    return render_template('random.html', single_number = number_var)



"""

This script uses the pymysql library for connecting to MySQL, 
so you might need to install that (pip install pymysql) if you haven't already.

It also uses python-dotenv for bringing in secrets from your .env file 

The .env should have the following in it:

DB_HOST=your_host
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_PORT=3306
DB_CHARSET=utf8mb4

The default port is set to 3306 for MySQL, but you can override it by 
modifying the DB_PORT in your .env file.

The connection string is MySQL-specific, incorporating the specified port and charset.

"""

load_dotenv()  # Load environment variables from .env file

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

# Create a database engine
db_engine = create_engine(conn_string, pool_size=1, max_overflow=0, echo=False)


def get_tables(engine): 
    """Get list of tables."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def execute_query_to_dataframe(query: str, engine):
    """Execute SQL query and return result as a DataFrame."""
    return read_sql(query, engine)


# Example usage
tables = get_tables(db_engine)
print("Tables in the database:", tables)


sql_query = "SELECT * FROM employee"  # Modify as per your table
df = execute_query_to_dataframe(sql_query, db_engine)

sql_query2 = "SELECT * FROM hospital_department"  # Modify as per your table
df2 = execute_query_to_dataframe(sql_query2, db_engine)

@app.route('/data')
def data(data=df, data2=df2):
    return render_template('data.html', data=data, data2=data2)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )