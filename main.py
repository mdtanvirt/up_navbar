import streamlit as st
import numpy as np
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    header {visibility: hidden}
    div.block-container {padding-top:1rem;}
    p{
    margin: 0 !important;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" >
            
  <a class="navbar-brand" style="font-size: 25px; color: #009698; display: inline-block; font-weight: 600;" href="#">LOGO-ICON</a>
            
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
            
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Strategies</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Reports</span></a>
      </li>
    </ul>
    <div style="position: absolute; right: 10px; display:flex; gap:10px;">
        <span> <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Sign In</a></span>
        <span> <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Sign Up</a></span>
        <!--<form class="form-inline my-2 my-lg-0" >
            <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" style="color: #fff; background-color: #28a745;" type="submit">Search</button>
        </form>-->
    </div>
    
  </div>
            
</nav>
""", unsafe_allow_html=True)


colItem1, colItem2 = st.columns([3,3])
# Create an empty container
with colItem1:
    placeholder = st.empty()

    actual_email = "email"
    actual_password = "password"

    # Insert a form in the container
    with placeholder.form("SignUp"):
        st.image("ai-prompt.webp")
        st.markdown("<p style='color: #009698;'><style: Do not have any account. Please click Sign up button to register.</p>", unsafe_allow_html=True)
        submit = st.form_submit_button("SignUp")


with colItem2:
                      
    placeholder = st.empty()

    actual_email = "email"
    actual_password = "password"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("<p style='color: #009698;'>Enter your credentials to login</p>", unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit and email == actual_email and password == actual_password:
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.success("Login successful")
        elif submit and email != actual_email and password != actual_password:
            st.error("Login failed")
        else:
            pass


leftAln, centerAln, rightAln = st.columns([3,3, 3])

with leftAln:
    st.write(" ")

with centerAln:
    st.write("Copyright © 2024 ABC Company LTD. All rights reserved.")

with rightAln:
    st.write(" ")