import streamlit as st


st.title("NEXX database handler")
if st.button("Image upload"):
    st.switch_page("pages/image_upload.py")
if st.button("Text upload"):
    st.switch_page("pages/text_upload.py")