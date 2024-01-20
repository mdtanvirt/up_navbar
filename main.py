import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    header {visibility: hidden}
    div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#st.header('Top Nav Bar')

col1, col2 = st.columns([6,.3])
with col1:
    tab1, tab2, tab3 = st.tabs(["Files", "Nothing", "Reports"])
    tab1.title("This is File page")
    tab2.title("This is Nothing")
    tab3.title("This is Report page")

#col2.subheader("coleumn two")
with col2:
    tab_user = st.tabs(["User Icon"])