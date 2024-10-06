import streamlit as st
from cash_functions import *
import page1, page2, page3
st.set_page_config(page_title="Value Calculator ", layout="wide")

##future_State 1 sessoion
if "list_append" not in st.session_state:
    st.session_state.list_append = []
    
##future_State 2 sessoion
if "list_append_b" not in st.session_state:
    st.session_state.list_append_b = []

##NV  sessoion
if "new_list" not in st.session_state:
    st.session_state.new_list = []
if "sumofvalues" not in st.session_state:
    st.session_state.sumofvalues = []
if "d" not in st.session_state:
    st.session_state.d = {}

#terminal value
if "terminal_value" not in st.session_state:
    st.session_state.terminal_value = []
if "formula" not in st.session_state:
    st.session_state.formula = []
if "netcash" not in st.session_state:
    st.session_state.netcash = []
if "total_share" not in st.session_state:
    st.session_state.total_share = []
if "min" not in st.session_state:
    st.session_state.min = []
if "max" not in st.session_state:
    st.session_state.max = []






import streamlit as st
import page1  # Assuming you have a file page1.py

# This must be the very first Streamlit command in the script

# Sidebar Radio for Navigation
genre = st.sidebar.radio(
    "**Select Checkbox to view pages**",
    ["***DCF***", "**Signal**"],
)

# Check selected genre and load the appropriate page
if genre == "***DCF***":
    page1.main()  # Make sure page1 has a main() function to handle DCF logic
if genre == '**Signal**':
    page3.main()
