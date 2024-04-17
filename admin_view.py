import streamlit as st
import mysql.connector
from datetime import date
import pandas as pd

# Connect to MySQL database
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

# Define a cursor for executing SQL queries
cursor = connection.cursor()

# Streamlit app
st.title('Admin View')

# Dropdown to select state
selected_state = st.selectbox('Select State:', ['Gujarat', 'Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu'])

# button for grievances

if st.button('View Grievances'):
    # Convert state name to state ID
    state_mapping = {'Gujarat': 1, 'Maharashtra': 2, 'Karnataka': 3, 'Delhi': 4, 'Tamil Nadu': 5}
    state_id = state_mapping[selected_state]
    
    # Fetch grievances associated with the selected state
    query = f"SELECT * FROM grievance WHERE StateId = {state_id} AND Status = 'pending';"
    cursor.execute(query)
    grievances = cursor.fetchall()
    
    # Display the grievances
    if grievances:
        st.write("Grievances associated with", selected_state)
        # Create a list of dictionaries to hold the grievance information
        grievance_list = []
        for grievance in grievances:
            print(grievance)
            grievance_dict = {
                "Grievance ID": grievance[0],
                "Department ID": grievance[2],
                "User ID": grievance[3],
                "Category": grievance[4],
                "Description": grievance[5],
                "Date Submitted": grievance[7],
                "Date Resolved": grievance[8]
            }
            grievance_list.append(grievance_dict)
        # Display the grievances in a table
        st.table(pd.DataFrame(grievance_list))
    else:
        st.write("No grievances found for", selected_state)


# Text input for grievance ID
grievance_id = st.text_input('Enter Grievance ID:')

# Button to resolve grievance
if st.button('Resolve Grievance'):
    # Check if grievance ID is provided
    if grievance_id:
        # Convert state name to state ID
        state_mapping = {'Gujarat': 1, 'Maharashtra': 2, 'Karnataka': 3, 'Delhi': 4, 'Tamil Nadu': 5}
        state_id = state_mapping[selected_state]
        
        # Update grievance status and date resolved in database
        update_query = f"UPDATE grievance SET status = 'resolved', dateresolved = '{date.today()}' WHERE GrievanceId = {grievance_id} AND StateId = {state_id};"
        cursor.execute(update_query)
        connection.commit()
        
        st.success(f"Grievance {grievance_id} in {selected_state} has been resolved.")
    else:
        st.error("Please enter a grievance ID.")

# Button to view grievances

