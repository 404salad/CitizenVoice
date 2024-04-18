import mysql.connector
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from io import StringIO
import random

# Function to authenticate user
def authenticate(username, password):
    cursor.execute("SELECT * FROM user WHERE UserId = %s and PasswordHash = %s", (username, password))
    data = cursor.fetchall()
    return data

# Function to retrieve StateId based on StateName
def get_state_id(state_name):
    cursor.execute("SELECT StateId FROM state WHERE StateName = %s", (state_name,))
    data = cursor.fetchone()
    if data:
        return data[0]
    else:
        return None

# Function to insert grievance into the database
def insert_grievance(state_id, user_id, category, description, date_submitted, department_id):
    grievance_id = random.randint(1000, 9999)  # Generating a random grievance ID
    status = "Pending"  # Setting initial status as Pending
    cursor.execute("INSERT INTO grievance (GrievanceId, StateId, DepartmentId, UserId, Category, Description, Status, DateSubmitted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (grievance_id, state_id, department_id, user_id, category, description, status, date_submitted))
    connection.commit()


def get_grievance_data_with_map(cursor):
    """
  Fetches grievance data by state, generates random points, and displays them on a map.

  Args:
      cursor: A database cursor object.

  Returns:
      None
  """
    state_coords = {"karnataka": [15.3173, 75.7139], "gujarat": [22.6708, 71.5724], "tamil nadu": [11.1271, 78.6569],
                    "maharashtra": [19.7515, 75.7139]}

    # Get grievance data
    cursor.execute("""SELECT s.StateName, COUNT(g.GrievanceId) AS GrievanceCount
                      FROM grievance g
                      INNER JOIN state s ON g.StateId = s.StateId
                      GROUP BY s.StateName, g.status
                      HAVING g.status='pending'
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
    st.map(all_data)

def fetch_user_grievances(user_id):
    # Your code to fetch grievances associated with the given user_id from the database
    # Replace this with your actual database query
    # Sample code assuming you have a database connection named `cursor`
    cursor.execute(f"SELECT * FROM grievance WHERE UserId = '{user_id}'")
    user_grievances = cursor.fetchall()

    # Convert the fetched data into a list of dictionaries for easy display
    grievances_list = []
    for grievance in user_grievances:
        grievance_dict = {
            "GrievanceId": grievance[0],
            "Status": grievance[6],
            "Description": grievance[5],
            # Add more fields as needed
        }
        grievances_list.append(grievance_dict)

    return grievances_list
    
    


# Streamlit GUI
def main():
    # Initialize session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id == "root":
        st.title("CitizenVoice — Admin")

    # Navigation menu
    page = st.sidebar.radio("Navigation", ["Login", "Submit Grievance", "View Grievances"])

    if page != "Login" and st.session_state.user_id:
        get_grievance_data_with_map(cursor)

    if page == "Login":
        st.header("User Authentication")

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Button to authenticate user
        if st.button("Login"):
            if username and password:
                # if the user is root user they are allowed to view complaints
                if username == "root" and password == "root":
                    st.session_state.user_id = "root"

                else:
                    result = authenticate(username, password)
                    if len(result) > 0:
                        st.success("Authentication successful!")
                        st.session_state.user_id = username  # Setting user_id to the logged-in username
                    else:
                        st.error("Authentication failed. Invalid username or password.")
            else:
                st.warning("Please enter username and password.")

        if st.button("Logout"):
            st.session_state.user_id = None

    elif page == "Submit Grievance":
        st.header("Submit Grievance")
        if st.session_state.user_id:
            st.write("Welcome, " + st.session_state.user_id + "!")
            # Grievance submission form
            state_name = st.text_input("State Name")
            category = st.selectbox("Category", ["Road Issues", "Water Issues"])
            description = st.text_area("Description")
            date_submitted = st.date_input("Date Submitted")
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                # To read file as bytes:q   
                # bytes_data = uploaded_file.getvalue()
                st.write(uploaded_file.type + " uploaded")

            if st.button("Submit Grievance"):
                if state_name and category and description and date_submitted:
                    state_id = get_state_id(state_name)
                    if state_id:
                        if category == "Road Issues":
                            department_id = "UD"
                        else:
                            department_id = "PW"
                        insert_grievance(state_id, st.session_state.user_id, category, description, date_submitted, department_id)
                        st.success("Grievance submitted successfully!")
                    else:
                        st.error("State not found. Please enter a valid State Name.")
                else:
                    st.error("Please fill in all the fields.")
            if st.button("Show My Grievances"):
                # Fetch grievances associated with the current user
                user_id = st.session_state.user_id
                user_grievances = fetch_user_grievances(user_id)

                if user_grievances:
                    st.write("Your Grievances:")
                    for grievance in user_grievances:
                        st.write(f"ID: {grievance['GrievanceId']}, Status: {grievance['Status']}, Description: {grievance['Description']}")
                else:
                    st.write("No grievances found for you.")        
        else:
            st.error("Please login to submit a grievance.")
            
            

    elif page == "View Grievances":
        st.title('Admin View')
        if not st.session_state.user_id=="root":
            st.error("Please login as admin to view grievances")
            return
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
        admin_comment = st.text_area('Enter Admin Comment (Optional)')

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

                # Fetching user ID associated with the grievance
                query = f"SELECT UserId FROM grievance WHERE GrievanceId = {grievance_id}"
                cursor.execute(query)
                commenter_id = cursor.fetchall()

                # Inserting comment into the comment table
                comment_id = random.randint(1000, 9999)
                comment_query = f"INSERT INTO comment (CommentId, GrievanceId, UserId, Comment, DateCommented) VALUES ({comment_id}, {grievance_id}, '{commenter_id[0][0]}', '{admin_comment}', '{date.today()}');"
                cursor.execute(comment_query)
                connection.commit()

                st.success(f"Grievance {grievance_id} in {selected_state} has been resolved.")
            else:
                st.error("Please enter a grievance ID.")

        # Button to submit admin comment
        if st.button('Submit Admin Comment'):
            if grievance_id and admin_comment:
                # Fetching user ID associated with the grievance
                query = f"SELECT UserId FROM grievance WHERE GrievanceId = {grievance_id}"
                cursor.execute(query)
                commenter_id = cursor.fetchall()

                # Inserting comment into the comment table
                comment_id = random.randint(1000, 9999)
                comment_query = f"INSERT INTO comment (CommentId, GrievanceId, UserId, Comment, DateCommented) VALUES ({comment_id}, {grievance_id}, '{commenter_id[0][0]}', '{admin_comment}', '{date.today()}');"
                cursor.execute(comment_query)
                connection.commit()

                st.success("Admin comment submitted successfully.")
            else:
                st.error("Please enter a grievance ID and comment.")


if __name__ == "__main__":
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='savitha',
        database='dbmsproject'
    )

    # Check if the connection is successful
    if connection.is_connected():
        print('Connected to MySQL database')
    else:
        print('Failed to connect to MySQL database')

    cursor = connection.cursor()

    main()
