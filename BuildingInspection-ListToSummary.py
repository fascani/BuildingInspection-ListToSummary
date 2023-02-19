#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/19/2023
@author: francoisascani
"""

import os
import streamlit as st
import openai
from transformers import GPT2TokenizerFast
from sentence_transformers import SentenceTransformer
import datetime
from streamlit_chat import message

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

    # (adapted from https://medium.com/@avra42/build-your-own-chatbot-with-openai-gpt-3-and-streamlit-6f1330876846)
    st.set_page_config(page_title="James, you building inspector assistant")
    set.text('Type your list of comments and click generate to generate a summary')
    
    # Collect list of things
    ########################
    
    # Construct the prompt
    ######################

    # Set the tokenizer
    
    def construct_prompt(query, df, method):
        '''
        Construct the prompt to answer the query. The prompt is composed of the
        query (from the user) and a context containing  the biographical entries
        the most relevant (similar) to the query.
        Parameters
        ----------
        query : str
            Query.
        df : Pandas dataframe
            Biographical info with embeddings.
        method : str
            Method indicates which model to use, either 'openai' for using the OpenAI
        API for 'text-embedding-ada-002', or 'huggingface' for using locally
        'paraphrase-MiniLM-L6-v2'. In the former case, the output is only a string
        that will be used via the API. In the latter case, it is an actual model
        object.
        Returns
        -------
        prompt : str
            Prompt.
        '''

        MAX_SECTION_LEN = get_max_num_tokens()
        SEPARATOR = "\n* "
        tokenizer = load_tokenizer()
        separator_len = len(tokenizer.tokenize(SEPARATOR))

        chosen_sections = []
        chosen_sections_len = 0

        # Order posts_df by their similarity with the query
        df = order_entries_by_similarity(query, df, method)

        for section_index in range(len(df)):
            # Add contexts until we run out of space.        
            document_section = df.loc[section_index]

            chosen_sections_len += document_section.num_tokens + separator_len
            if chosen_sections_len > MAX_SECTION_LEN:
                break

            chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))

        # header = """
        #This question is asked by an interviewer or somebody who wants to know
        #more about me, Francois Ascani. Answer politely using the following context
        #but don't be afraid to have a candid, good-nature, and joking tone as
        #this is exactly who I am. Context:\n
        #"""
        #prompt = header + "".join(chosen_sections) + "\n\n Q: " + query + "\n A:"
        
        header = """
        Answer as Francois, a French-American scientist who likes to be humorous
        and speak candidly.
        You: Where did you grow up?
        Francois: I grew up in France and, even after 23 years in the US, I still
        have a strong accent!
        You: Describe a current project
        Francois: Well, I am currently working on estimating the customer lifetime
        value of our customers. I should say finally! as I have been proposing
        doing that for more than 5 years now. But it is never too late! And I had
        time to perfect the approach so here is your silver lining :)
        Context:\n
        """
        prompt = header + "".join(chosen_sections) + "\n\n Q: " + query + "\n A:"

        return prompt

    def ListToSummary(query):
        '''
        Use a pre-trained NLP method to answer a question given a database
        of information.
        The function also records the query, the prompt, and the answer in
        the database.
        Parameters
        ----------
        query : str
            Query
        df : Pandas dataframe
            Biographical info with embeddings.
        method : str
            Method indicates which model to use, either 'openai' for using the OpenAI
        API for 'text-embedding-ada-002', or 'huggingface' for using locally
        'paraphrase-MiniLM-L6-v2'. In the former case, the output is only a string
        that will be used via the API. In the latter case, it is an actual model
        object.
        Returns
        -------
        answer : str
            Answer from the model.
        prompt : str
            Actual prompt built.
        '''

        # Construct the prompt
        #prompt = construct_prompt(query, df, method)

        # Ask the question with the context with GPT3 text-davinci-003
        #COMPLETIONS_MODEL = "text-davinci-003"

        response = openai.Completion.create(
            prompt=prompt,
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=COMPLETIONS_MODEL
        )

        answer = response["choices"][0]["text"].strip(" \n")

        return answer, prompt
    
    
