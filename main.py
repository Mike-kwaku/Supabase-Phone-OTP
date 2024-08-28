import os
import streamlit as st
import streamlit.components.v1 as components
import json 

from supabase import create_client, Client

st.title("Health Portal")   

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

def login_otp(phone):   
    response = supabase.auth.sign_in_with_otp({"phone": phone})
    st.write("Check your phone for your token code")

def verify_otp(phone, token_code, type):
    response = supabase.auth.verify_otp({"phone": phone, "token_code": token_code, "type": type})
    if response.user:   
      st.session_state.user = response.user
      st.success("welcome")
    else:
        st.warning("Token expired or Invalid token.")
  

col1, col2 = st.columns(2)
with col1:
        with st.expander('Generate OTP'):
            phone = st.text_input('Phone', key='enter phone number')
            generate_btn = st.button('Generate OTP', on_click=login_otp, args=(phone))
                                     
with col2:
        with st.expander('Verify OTP'):
            phone = st.text_input('Phone', key='phone number')
            token = st.text_input('Token', key='Token')
            type = st.text_input('Type', key='Type')
            verify_btn = st.button('Verify OTP', on_click=verify_otp, args=(phone, token, type))
