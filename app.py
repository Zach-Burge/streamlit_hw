import streamlit as st
import requests

st.title("Hello World!")
name = st.text_input("What is your name?")
age = st.number_input("Enter your age:", step=1)

if st.button("Enter"):
    chalice_endpoint = st.secrets["endpoint"]
    data = {'name': name, 'age': age}
    response = requests.post(chalice_endpoint, json=data)
    result = response.json()
    # result_data = result['result']
    st.title(f"{result['name']} will be {result['new_age']}")
