# This Python script connects to a PostgreSQL database and utilizes Pandas to obtain data and create a data frame
# A initialization and configuration file is used to protect the author's login credentials

import psycopg2
import pandas as pd
import sklearn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
# Import the 'config' funtion from the config.py file
from config import config



def get_data():
    # Establish a connection to the database by creating a cursor object

    # Obtain the configuration parameters
    params = config()
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
    # Create a new cursor
    cur = conn.cursor()

    # A function that takes in a PostgreSQL query and outputs a pandas database 
    def create_pandas_table(sql_query, database = conn):
        table = pd.read_sql_query(sql_query, database)
        return table
    
    # Utilize the create_pandas_table function to create a Pandas data frame
    # Store the data as a variable
    data_1 = create_pandas_table("SELECT * FROM erik ORDER BY RANDOM()")
    print(data_1.head(5))

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()
    return(data_1)


def split_data(df):
    train_df, test_df = train_test_split(df, test_size=0.2)
    X_train = train_df.iloc[:,:-1].values
    y_train = train_df.iloc[:,-1].values
    X_test = test_df.iloc[:,:-1].values
    y_test = test_df.iloc[:,-1].values
    return X_train, y_train, X_test, y_test

def linear_model(X_train, y_train, X_test, y_test):
    
    reg = LinearRegression().fit(X_train, y_train)
    print("score: ",reg.score(X_train, y_train))
    print("coeff: ", reg.coef_)
    pred = reg.predict(X_test)
    print("prediction: ",pred)
    print("true_value: ",y_test)
    mse = mean_squared_error(pred,y_test)
    print("mse:: ",mse)
    return mse

def decision_tree(X_train, y_train, X_test, y_test):
    dec_tree = DecisionTreeRegressor(random_state=0).fit(X_train,y_train)
    pred = dec_tree.predict(X_test)
    print("prediction: ",pred)
    print("true_value: ",y_test)
    mse = mean_squared_error(pred,y_test)
    print("mse:: ",mse)
    return mse


if __name__ == "__main__":
    data = get_data()
    X_train, y_train, X_test, y_test = split_data(data)
    mse_linear = linear_model(X_train, y_train, X_test, y_test)
    mse_dec = decision_tree(X_train, y_train, X_test, y_test)

