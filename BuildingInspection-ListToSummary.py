#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/19/2023
@author: francoisascani
"""

import os
import streamlit as st
import openai
import datetime

# Streamlit app
###############

# from https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso#option-2-individual-password-for-each-user
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            #del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    
    if 'kept_username' not in st.session_state:
        st.session_state['kept_username'] = st.session_state['username']

    st.set_page_config(page_title="Hello! I am James, your building inspector assistant")
    st.title("Hello! I am James, your building inspector assistant")
    st.text('Type your comments and click to generate a summary')
    
    # Collect list of things
    ########################
    
    # Initialize a counter 
    if 'count' not in st.session_state:
        st.session_state.count = 0

    # Initialize the list of comments
    if 'count' not in st.session_state:
        st.session_state.comments = list()

    def new_comment():
        st.session_state.count += 1
        st.session_state.comments.append(st_session_state.new_comment)

    container = st.container()
    #container.text_input('Write your comment', on_change=new_comment, key='comment-' + str(st.session_state.count))
    container.text_input('Write your comment', on_change=new_comment, key='new_comment')
    
    st.text(st.session_state.count)
    st.text(st.session_state.comments)

    # st.form to submit eveything at once, see https://docs.streamlit.io/library/api-reference/control-flow/st.form
    
    # Construct the prompt
    ######################

    