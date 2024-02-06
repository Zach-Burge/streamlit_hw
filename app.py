import streamlit as st
import requests

st.title("Hello World!")
st.text_input("Enter a Number:")

if st.button("Source"):
    response = requests.get(st.secrets["endpoint"])
    st.write(response.content)
