import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

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
        <form class="form-inline my-2 my-lg-0" >
            <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" style="color: #fff; background-color: #28a745;" type="submit">Search</button>
        </form>
        <span> <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Chat</a></span>
        <span> <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Setting</a></span>
        <span> <a class="nav-link" style="color: #009698; display: inline-block;" href="#">Sign Out</a></span>
    </div>
    
  </div>
            
</nav>
""", unsafe_allow_html=True)

if st.button("View data"):
    st.switch_page("pages/simulator.py")