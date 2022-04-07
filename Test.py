import streamlit as st

#Import libraries tools:
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

menu = ["Home", "About"]
choice = st.sidebar.selectbox("Menu", menu)

st.title("Media Sentiment Analysis App")

if choice =="Home":
  st.subheader("Home")

  # search
  with st.form(key='searchform'):
    nav1,nav2 = st.columns([2,1])

    with nav1:
        search_keyword =st.text_input("Search with a keyword")
    with nav2:
        st.text("Search")
        submit_keyword = st.form_submit_button()


else:
  st.subheader("About")
  st.write("The **_Media Sentiment Analysis App_** lets you analyze data extracted from different media sources")
  st.write("All you have to do is type a keyword into the search bar and you will be able to see information related to what term you just typed!")
  st.write("This information will be presented in the form of wordCloud and graphs for better a visualization experience")

   
