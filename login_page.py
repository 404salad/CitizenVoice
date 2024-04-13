import mysql.connector
import streamlit as st
import pandas as pd
import random

# Function to authenticate user
def authenticate(username, password):
    cursor.execute("SELECT * FROM User WHERE UserId = %s and PasswordHash = %s", (username, password))
    data = cursor.fetchall()
    return data

# Function to retrieve StateId based on StateName
def get_state_id(state_name):
    cursor.execute("SELECT StateId FROM State WHERE StateName = %s", (state_name,))
    data = cursor.fetchone()
    if data:
        return data[0]
    else:
        return None

# Function to insert grievance into the database
def insert_grievance(state_id, user_id, category, description, date_submitted, department_id):
    grievance_id = random.randint(1000, 9999)  # Generating a random grievance ID
    status = "Pending"  # Setting initial status as Pending
    cursor.execute("INSERT INTO Grievance (GrievanceId, StateId, DepartmentId, UserId, Category, Description, Status, DateSubmitted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (grievance_id, state_id, department_id, user_id, category, description, status, date_submitted))
    connection.commit()

# Streamlit GUI
def main():
    st.title("User Authentication and Grievance Submission")

    # Initialize session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # Navigation menu
    page = st.sidebar.radio("Navigation", ["Login", "Submit Grievance"])

    if page == "Login":
        st.title("User Authentication")

        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Button to authenticate user
        if st.button("Login"):
            if username and password:
                result = authenticate(username, password)
                if len(result) > 0:
                    st.success("Authentication successful!")
                    st.session_state.user_id = username  # Setting user_id to the logged-in username
                else:
                    st.error("Authentication failed. Invalid username or password.")
            else:
                st.warning("Please enter username and password.")

    elif page == "Submit Grievance":
        st.title("Submit Grievance")
        if st.session_state.user_id:
            st.write("Welcome, " + st.session_state.user_id + "!")
            # Grievance submission form
            state_name = st.text_input("State Name")
            category = st.selectbox("Category", ["Road Issues", "Water Issues"])
            description = st.text_area("Description")
            date_submitted = st.date_input("Date Submitted")

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
        else:
            st.write("Please login to submit a grievance.")

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
