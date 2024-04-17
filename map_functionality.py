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


def get_grievance_data_with_map(cursor):
    """
  Fetches grievance data by state, generates random points, and displays them on a map.

  Args:
      cursor: A database cursor object.

  Returns:
      None
  """

    # Get grievance data
    cursor.execute("""SELECT s.StateName, COUNT(g.GrievanceId) AS GrievanceCount
                    FROM grievance g
                    INNER JOIN state s ON g.StateId = s.StateId
                    GROUP BY s.StateName
                    ORDER BY GrievanceCount DESC;
                """)
    data = cursor.fetchall()

    # Combine all data into a single DataFrame
    all_data = pd.DataFrame(columns=['lat', 'lon'])
    for row in data:
        state_name = row[0]
        count = row[1]

        if state_name.lower() in state_coords:
            state_lat_lon = state_coords[state_name.lower()]
            data_points = pd.DataFrame(
                np.random.randn(count * 4, 2) * count * 10 / [50, 50] + state_lat_lon,
                columns=['lat', 'lon'])
            all_data = pd.concat([all_data, data_points], ignore_index=True)

    # Display data on map
    st.write(data)  # Show grievance data table (optional)
    st.map(all_data)


# Call the function
state_coords = {"karnataka": [15.3173, 75.7139], "gujarat": [22.6708, 71.5724], "tamil nadu": [11.1271, 78.6569],
                "maharashtra": [19.7515, 75.7139]}
get_grievance_data_with_map(cursor)
