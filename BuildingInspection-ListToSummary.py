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
    st.text("Type your comments and click 'generate summary'")
    
    # Collect list of things
    ########################
    
    # Initialize a counter 
    if 'count' not in st.session_state:
        st.session_state.count = 0

    # Initialize the list of comments
    if 'comments' not in st.session_state:
        st.session_state.comments = list()

    # Initialize new_comment
    if 'new_comment' not in st.session_state:
        st.session_state.new_comment = ''

    def new_comment():
        st.session_state.count += 1
        st.session_state.comments.append(st.session_state.new_comment)
        st.session_state.new_comment = '' # Reset new commment

    # Clear button
    clear_comments = st.button('clear all')

    if clear_comments:
        st.session_state.comments = list()
        st.session_state.new_comment = ''

    container = st.container()
    container.text_input('Write one comment at a time', on_change=new_comment, key='new_comment')
    
    # For testing
    #st.text(st.session_state.count)
    #st.text(st.session_state.comments)

    # Print a nice markdown list
    markdown_comments = "\n".join(["- " + item for item in st.session_state.comments])
    st.text(markdown_comments)

    # Construct the prompt
    ######################

    preamble = '''
    Summarize (and correct for standard English) a list of inputs for a professional
    building inspector. For example, if the inputs were:

    "- Bedroom 1
    - Walls lining paper and poor
    - Floor is tiled and good
    - Ceiling and some walls lining paper and good
    - Damp stain to ceiling
    - Windows are PVCu double glazed, we tested one, seem good
    - One glazed pane was cracked
    - Floor is carpet and poor"

    you would generate the following summary:

    "Upon inspection of Bedroom 1, the walls were observed to be lined with paper, and
    it was determined that they are in poor condition. The floor is tiled and appeared
    to be in good condition. The ceiling and some of the walls are also lined with paper,
    which appears to be in good condition. However, a damp stain was noted on the ceiling,
    which requires further investigation to determine the cause and extent of the issue.
    The windows are PVCu double-glazed, and one window was tested and appears to be in good condition.
    However, it should be noted that one glazed pane was found to be cracked, which may require
    replacement. The floor is covered in carpet, which is in poor condition and may require replacement.
    
    Overall, some remedial works may be necessary to address the issues identified in Bedroom 1,
    including investigating the damp stain, replacing the damaged glazed pane, and improving the
    condition of the walls and flooring."

    Below is the list of inputs to use to generate the summary:
    
    '''

    end_prompt = '''
    
    Start the summary (don't forget the conclusion "Overall,..."):
    '''

    prompt = preamble + markdown_comments + end_prompt

    # For testing
    st.text(prompt)

    # Run the prompt thru the OpenAI API
    ####################################

    # Set the OpenAI API key
    openai.api_key = st.secrets["openai_api_key"]

    # Add the generate summary button
    generate = st.button('generate summary')

    def generate_summary(prompt):
        '''
        Use a pre-trained NLP to summarize the bullet points.

        Parameters
        ----------
        prompt : str
            Prompt
        
        Returns
        -------
        answer : str
            Answer from the model
        '''

        # Ask the question with the context with GPT3 text-davinci-003
        COMPLETIONS_MODEL = "text-davinci-003"

        response = openai.Completion.create(
            prompt=prompt,
            temperature=0.1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=COMPLETIONS_MODEL
        )

        summary = response["choices"][0]["text"].strip(" \n")

        return summary

    if generate:
        summary = generate_summary(prompt)
        st.markdown(summary)


    # Add the generate summary button
    st.button('save to Google sheet')
