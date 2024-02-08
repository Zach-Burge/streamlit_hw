import streamlit as st
import requests

st.title("Hello World!")
number = st.number_input("Enter a Number:", step=1)

if st.button("Enter"):
    chalice_endpoint = st.secrets["endpoint"]
    endpoint = f"{chalice_endpoint}{number}"
    response = requests.get(endpoint).json()
    result = response['result']
    st.title(result)
