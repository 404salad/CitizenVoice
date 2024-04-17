import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='savitha',
    database='dbmsproject'
)

if connection.is_connected():
    print('Connected to MySQL database')
else:
    print('Failed to connect to MySQL database')

    cursor = connection.cursor()
    


d1={"karnataka":[15.3173, 75.7139],"gujarat":[22.6708,71.5724],"tamilnadu":[11.1271,78.6569],"maharashtra":[19.7515,75.7139]}

state_name = st.text_input("Enter the state name:")


if state_name.lower() in d1:
    
    state_lat_lon = d1[state_name.lower()]

    df = pd.DataFrame(
        np.random.randn(20, 2) * 10 / [50, 50] + state_lat_lon,
        columns=['lat', 'lon'])



    st.map(df)