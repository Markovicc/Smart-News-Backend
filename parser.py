import feedparser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import re
from media_parsers import *


def get_feeds(medialist, lsth):
    lista = []
    for media in medialist:
        response = feedparser.parse(media['link'])
        for entry in response.entries:
            if pd.to_datetime(entry.published) >= lsth:
                rez = {}
                rez['Medij'] = media['ime']
                rez['Naslov'] = bs(entry.title,'html.parser').get_text()
                rez['Uvod'] = bs(entry.summary, 'html.parser').get_text()
                rez['Link'] = entry.link
                rez['Vreme'] = entry.published
                lista.append(rez)
    return lista


def get_feed_complete(lst, dfm):
    for media in lst:

        media_links = dfm[dfm.Medij== media].Link.tolist()
        if media == 'Danas':
            danas = pd.DataFrame(Danas_parser(media_links))

        if media == 'N1':
            n1 = pd.DataFrame(N1_parser(media_links))

        #if media == 'Sputnjik':
        #    sputnjik = pd.DataFrame(Sputnjik_parser(media_links))

        if media == 'RTS':
            rts = pd.DataFrame(RTS_parser(media_links))

        if media == 'B92':
            b92 = pd.DataFrame(B92_parser(media_links))

    return pd.concat([danas, n1, rts, b92])
