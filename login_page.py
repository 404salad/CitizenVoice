import mysql.connector
import streamlit as st
import pandas as pd

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

# Function to authenticate user
def authenticate(username, password):
    cursor.execute("SELECT * FROM User WHERE UserId = %s and PasswordHash = %s", (username, password))
    data = cursor.fetchall()
    return data

# Streamlit GUI
def main():
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
            else:
                st.error("Authentication failed. Invalid username or password.")
        else:
            st.warning("Please enter username and password.")

if __name__ == "__main__":
    main()
