import streamlit as st
import requests

st.title("Hello World!")
name = st.text_input("What is your name?")
age = st.number_input("Enter your age:", step=1)

if st.button("Enter"):
    chalice_endpoint = st.secrets["endpoint"]
    data = {'age': age, 'name': name}
    response = requests.post(chalice_endpoint, json=data)
    result = response.json()
    
    # Front end formatting
    st.title(f"{result['name']} will be {result['new_age']}")
    st.title("JSON Request")
    st.text(data)
    st.title("JSON Response")
    st.text(result)
