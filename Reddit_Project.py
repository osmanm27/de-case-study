#!/usr/bin/env python
# coding: utf-8

import praw
import pandas as pd
from pandas.io import gbq
import requests
import json
import csv
import time
import datetime
import Reddit_data_credentials
import gcp_credentials



def get_data_json():
    """ Create Reddit Instance and use the PRAW API to get top daily submissions """
    reddit = praw.Reddit(
    client_id=Reddit_data_credentials.my_client_id,
    client_secret=Reddit_data_credentials.my_client_secret,
    user_agent=Reddit_data_credentials.my_user_agent)

    daily_data = []
    dubai_subreddit = reddit.subreddit('dubai')
    for post in dubai_subreddit.top('day'):
        daily_data.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    daily_data = pd.DataFrame(daily_data,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    return daily_data

daily_data = get_data_json()

def convert_date(red_data):
    """Convert date column from float64 to datetime and handle dates """
    red_data['created'] =  pd.to_datetime(red_data['created'], unit='s')
    red_data['Day'] = red_data['created'].dt.day
    red_data['Month'] = red_data['created'].dt.month
    red_data['Year'] = red_data['created'].dt.year


def get_hist_data(query, after, before, sub):
    """ Use the pushshift API to get historical reddit submissions between a given date range """
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


query='dubai'
after='1580515200'
before='1582848000'
sub='dubai'

monthly_data = get_hist_data(query, after, before, sub)

title_list=[]
score_list=[]
id_list=[]
subreddit_list=[]
url_list=[]
num_comments_list=[]
created_list=[]

for each in monthly_data:
    title_list.append(each['title'])
    score_list.append(each['score'])
    id_list.append(each['id'])
    subreddit_list.append(each['subreddit'])
    url_list.append(each['url'])
    num_comments_list.append(each['num_comments'])
    created_list.append(each['created_utc'])

df = pd.DataFrame({'title':title_list, 'score':score_list, 'id':id_list, 'subreddit':subreddit_list, 'url':url_list, 'num_comments':num_comments_list, 'created':created_list})

project_id=gcp_credentials.project_id
convert_date(daily_data)
convert_date(df)

def load_daily_data():
    """ Load daily_data into Big Query """
    daily_data.to_gbq(destination_table='Reddit.daily_data',project_id=project_id, if_exists='replace')
    
load_daily_data()

def build_monthly_data():
    """ Load monthly_data into Big Query """
    df.to_gbq(destination_table='Reddit.monthly_data', project_id=project_id, if_exists='replace')
    
build_monthly_data()

def get_summ_table():
    """ This function will output:
        1. Top 5 highest upvotes in the daily data
        2. Top 5 highest commented posts in the daily data
        And then upload this into a seperate table in Big Query"""
    max_upvotes = daily_data.nlargest(5, columns=['score'])
    max_comments = daily_data.nlargest(5, columns=['num_comments'])
    sub_activity = df.groupby('Day')['title'].count()
    sub_activity = pd.DataFrame(sub_activity).reset_index()
    sub_activity.index = range(1,len(sub_activity)+1)
    sub_activity.rename(columns={'Day': 'day_of_month', 'title': 'sub_activity_count'}, inplace=True)
    max_upvotes.to_gbq(destination_table='summary_tables.max_upvotes', project_id=project_id, if_exists='replace')
    max_comments.to_gbq(destination_table='summary_tables.max_comments', project_id=project_id, if_exists='replace')
    sub_activity.to_gbq(destination_table='summary_tables.sub_activity', project_id=project_id, if_exists='replace')
    
get_summ_table()

