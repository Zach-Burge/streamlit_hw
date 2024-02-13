import streamlit as st
import requests

st.title("Hello World!")
name = st.text_input("What is your name?")
age = st.number_input("Enter your age:", step=1)

if st.button("Enter"):
    chalice_endpoint = st.secrets["endpoint"]
    endpoint = f"{chalice_endpoint}/{age}/{name}"
    response = requests.get(endpoint)
    result = response.json()
    st.title(f"{result['name']} will be {result['age_incremented']}")
