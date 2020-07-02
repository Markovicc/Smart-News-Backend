from models import *
import pandas as pd
import datetime
from parser import get_feeds
from parser import get_feed_complete
from media_set import Mediji

from media_set import media_list
import time
import os
from apscheduler.schedulers.background  import BackgroundScheduler

def import_data():

    last_hour = datetime.datetime.now() - datetime.timedelta(hours=12)
    feed_list = get_feeds(Mediji, last_hour)
    df = pd.DataFrame(feed_list)
    df.Vreme = pd.to_datetime(df.Vreme)


    for index, row in df.iterrows():
        print(row['Naslov'])

    df_list = get_feed_complete(media_list, df)

    rss_news = df.merge(df_list)

    df_svet = rss_news[rss_news.Link.str.contains('/[Ss]vet|nav_category=78')].copy()
    df_svet['Rubrika']='Svet'
    df_sport = rss_news[rss_news.Link.str.contains('[Ss]port')].copy()
    df_sport['Rubrika']='Sport'
    df_srb = rss_news[~(rss_news.Link.str.contains('[Ss]port') | rss_news.Link.str.contains('[Ss]vet|nav_category=78'))].copy()
    df_srb['Rubrika']='Srbija'
    df_con = pd.concat([df_srb,df_svet,df_sport])



    for index, row in df_con[~df_con.Link.str.contains('English')].iterrows():

        if row['Medij'] == 'Danas':
            article = NewsFeed(
            medij = row['Medij'],
            naslov = row['Naslov'],
            uvod = row['Uvod'][:len(row['Uvod'])-len(row['Naslov'])-48],
            link = row['Link'],
            komentari = row['Komentari'],
            vreme = row['Vreme'],
            foto = row['Foto'],
            rubrika=row['Rubrika']
            )

        else:
            article = NewsFeed(
            medij = row['Medij'],
            naslov = row['Naslov'],
            uvod = row['Uvod'],
            link = row['Link'],
            komentari = row['Komentari'],
            vreme = row['Vreme'],
            foto = row['Foto'],
            rubrika=row['Rubrika']
            )

        db.session.add(article)


    db.session.query(NewsFeed).filter(NewsFeed.vreme <= last_hour).delete()
    db.session.commit()



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(import_data, 'cron', hour='7-23', minute='1', timezone='Europe/Belgrade')
    scheduler.start()
    print('Waiting to exit')
    while True:
        time.sleep(1)
