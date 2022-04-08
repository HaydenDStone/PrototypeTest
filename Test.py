import streamlit as st

#Import libraries tools:
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from gensim.parsing.preprocessing import remove_stopwords

def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text) #Remove @mentions
  text = re.sub(r'#', '', text) #Remove "#"
  text = re.sub(r'RT[\s]+', '', text) #Removing RT
  text = re.sub(r'https?:\/\/\S+', '', text) #Removing hyper links
  text = remove_stopwords(text) #Remove stopwords
  return text

def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity

def getAnalysis(score):
  if score <0:
    return 'Negative'
  elif score ==0:
    return 'Neutral'
  else:
    return 'Positive'

def getResults(input):
  search_word = input
  filter_retweets_search = search_word + " -filter:retweets"
  date_since = '2022-02-24'
  tweet_num = 100

  consumerKey = "CYwMqAxxI7gd68RKc2yyRadbq"
  consumerSecret = "xueDpZFStAOKW1whDcjwlHXte8OLW3RRtLXrH3UlVwez1ww5Ki"
  accessToken = "1149167522064850944-aam9TmQ3XN4BXTYMItpq4PHX8BK3ii"
  accessTokenSecret = "PslrAHTv8t8Y5i9qq745UfD88R9gmYVcHyCI40FDngRRf"

  authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
  authenticate.set_access_token(accessToken, accessTokenSecret)
  api = tweepy.API(authenticate, wait_on_rate_limit=True)

  posts = tweepy.Cursor(api.search_tweets,
              q= filter_retweets_search,
              lang="en" 
              ).items(tweet_num)
#Dataframe
  df = pd.DataFrame([tweet.text for tweet in posts], columns=['Tweets'])

  df['Tweets'] = df['Tweets'].apply(cleanTxt)

  df.head()

  df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
  df['Polarity'] = df['Tweets'].apply(getPolarity)
  df['Analysis'] = df['Polarity'].apply(getAnalysis)

  st.dataframe(df.style.highlight_max(axis=0, color='#3B54A1'))

#VISUALIZATION
#Plot the polarity and subjectivity:
  fig = plt.figure(figsize=(8,6))
  for i in range(0, df.shape[0]):
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='#3B54A1')

  plt.title('Sentiment Analysis using Twitter hashtags')
  plt.xlabel('Polarity')
  plt.ylabel("Subjectivity")
  plt.show( )

  st.write(fig)

  #Get the percentage of positive tweets:
  ptweets = df[df.Analysis == 'Positive']
  ptweets = ptweets['Tweets']

  st.write('Percentage of positive tweets: ')
  st.write(round( (ptweets.shape[0] / df.shape[0]) *100, 1 ))


  #Get the percentage of negative tweets:
  ntweets = df[df.Analysis == 'Negative']
  ntweets = ntweets['Tweets']

  st.write('Percentage of negative tweets: ')
  st.write(round( (ntweets.shape[0] / df.shape[0]) *100, 1 ))

  #Get the percentage of neutral tweets:
  netweets = df[df.Analysis == 'Neutral']
  netweets = netweets['Tweets']

  st.write('Percentage of neutral tweets: ')
  st.write(round( (netweets.shape[0] / df.shape[0]) *100, 1 ))

  #Show the value counts:

  df['Analysis'].value_counts()

  #plot and visualize the counts:
  plt.title("Sentiment Analysis")
  plt.xlabel('Sentiment')
  plt.ylabel('Count')
  df['Analysis'].value_counts().plot(kind='bar')
  plt.show()


def main():

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
    if submit_keyword:
      getResults(search_keyword)

  else:
    st.subheader("About")
    st.write("The **_Media Sentiment Analysis App_** lets you analyze data extracted from different media sources")
    st.write("All you have to do is type a keyword into the search bar and you will be able to see information related to what term you just typed!")
    st.write("This information will be presented in the form of wordCloud and graphs for better a visualization experience")

   
if __name__ == '__main__':
	main()