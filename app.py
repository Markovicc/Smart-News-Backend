
from flask import Flask,render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import pandas as pd
import os
import requests
import json
from collections import Counter
import time
from word_cleaner import stop_words
from news_cleaner import key_words
import re
from flask_cors import CORS



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def b_vesti():
        return 'vesti'

def get_queries():
    df_fromsql = pd.read_sql_table('newsfeed', db.session.bind)

    return df_fromsql




def get_keywords(db_df):
    keywords = []

    top_words = key_words(db_df[['medij', 'uvod']].drop_duplicates(), stop_words)
    for word in top_words:
        keywords.append([word[0], word[1]])


    key_df = pd.DataFrame(keywords)
    cdf = key_df.rename(columns=({0:'kwords', 1:'numwords'}))\
                    .drop_duplicates().groupby('kwords').sum()\
                    .sort_values('numwords', ascending=False).reset_index()
    return cdf




@app.route('/api/media-keywords/<website>', methods=['GET'])
def make_keyword_api(website):
    db_data = get_queries()

    if website=='Naslovna':
        media_input = db_data.drop_duplicates()
    else:
        media_input = db_data[db_data.rubrika==website].drop_duplicates()

    df_links = get_keywords(media_input)


    most_pop = []

    for index,kws in df_links.kwords.iteritems():
        for index, row in media_input[['uvod','naslov','medij','link','foto']].drop_duplicates().iterrows():
            key_article = {}
            if kws.lower() in row['uvod'].lower():
                key_article['keywo']=kws
                key_article['naslov'] = row['naslov']
                key_article['uvod'] = row['uvod']
                key_article['link'] = row['link']
                key_article['medij'] = row['medij']
                key_article['foto'] = row['foto']


                most_pop.append(key_article)
    df_most_pop = pd.DataFrame(most_pop)


    dedup = df_most_pop.groupby('naslov').head()\
    .sort_values('keywo', ascending=False).reset_index()

    df_most = dedup.groupby(['naslov', 'link','medij','foto', 'uvod']).count()\
    .sort_values('keywo', ascending=False).reset_index().copy()


    head_df = df_most[:1]


    return jsonify({'headlines':df_most[:25].to_dict(orient='records')})


@app.route('/api/most-comments/<website>',methods=['GET'])
def make_comments_api(website):
    db_data = get_queries()

    if website=='Naslovna':
        media_input = db_data.drop_duplicates()
    else:
        media_input = db_data[db_data.rubrika==website].drop_duplicates()

    komentari = media_input[['medij','naslov', 'uvod','komentari','foto','link']]\
    .groupby('naslov').max().drop_duplicates()\
    .sort_values('komentari', ascending=False)\
    .head(20).reset_index()

    return jsonify({'comments':komentari.to_dict(orient='records')})


@app.route('/api/timeline/<website>',methods=['GET'])
def get_last_api(website):
    db_data = get_queries()

    if website=='Naslovna':
        media_input = db_data
    else:
        media_input = db_data[db_data.rubrika==website]

    timeline = media_input[['medij','naslov', 'uvod','vreme','foto','link']]\
    .sort_values('vreme', ascending=False)[:5]

    return jsonify({'timeline':timeline.to_dict(orient='records')})






if __name__ == '__main__':
    app.run()
