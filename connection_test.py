import mysql.connector
import streamlit as st
import pandas as pd
connection  = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'savitha',
    database = 'test'
)

print('connected')

cursor = connection.cursor()

cursor.execute("Select * from Grievance")
data = cursor.fetchall()

st.title('MYSQL Connection')
print(cursor.column_names)
df = pd.DataFrame(data,columns = cursor.column_names)
st.dataframe(df)

import geopandas as gpd  
import matplotlib.pyplot as plt  
import pandas as pd  
india_map = gpd.read_file('india_state_geo.json')  
population_data = df
population_df = pd.DataFrame(population_data)  
india_map = india_map.merge(population_df, left_on='NAME_1', right_on='Status')  
fig, ax = plt.subplots(1, figsize=(12, 8))  
india_map.plot(column='due', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)  
ax.set_title('Complaints left uncleared')  
ax.set_xlabel('Longitude')  
ax.set_ylabel('Latitude')  
plt.savefig("map.png")  



