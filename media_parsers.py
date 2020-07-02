import requests
from bs4 import BeautifulSoup as bs
import time


def Sputnjik_parser(link_list):
    BASELINK = 'https://rs-lat.sputniknews.com'
    list_dict =[]

    for link in link_list:
        response = requests.get(link)
        soup = bs(response.content,'html.parser')
        comtag = {}
        comtag['Link'] = link
        try:
            comtag['Komentari'] = int(soup.find(class_='b-counters-icon b-counters-icon_comments').text)
        except:
            comtag['Komentari'] = 0
        try:
            comtag['Foto'] = str(BASELINK + soup.find('meta', property='og:image')['content'])
        except:
            pass

        list_dict.append(comtag)
    return list_dict

def RTS_parser(link_list):
    list_dict =[]

    for link in link_list:
        response = requests.get(link)
        soup = bs(response.content,'html.parser')
        comtag = {}
        comtag['Link'] = link
        try:
            comtag['Komentari'] = int(soup.find(id='comment').find('span').text)
        except:
            comtag['Komentari'] = 0
        try:
            comtag['Foto'] = str(soup.find('meta', property='og:image')['content'])
        except:
            comtag['Foto'] = None

        list_dict.append(comtag)
    return list_dict

def Danas_parser(link_list):
    list_dict =[]

    for link in link_list:
        response = requests.get(link)
        soup = bs(response.content,'html.parser')
        comtag = {}
        comtag['Link'] = link
        try:
            comtag['Komentari'] = int(soup.find(class_='comment').text)
        except:
            comtag['Komentari'] = 0
        try:
            comtag['Foto'] = str(soup.find('meta', property='og:image')['content'])
        except:
            comtag['Foto'] = None
        list_dict.append(comtag)
    return list_dict




def N1_parser(link_list):
    list_dict =[]
    for link in link_list:
        response = requests.get(link)
        soup = bs(response.content,'html.parser')
        comtag = {}
        comtag['Link'] = link
        try:
            comtag['Komentari'] = int(soup.find(class_='comments-item').find('a').text)
        except:
            comtag['Komentari'] = 0
        try:
            comtag['Foto'] = str(soup.find('meta', itemprop='image')['content'])
        except:
            comtag['Foto'] = None
        list_dict.append(comtag)
    return list_dict

def B92_parser(link_list):
    list_dict =[]
    for link in link_list:
        response = requests.get(link)
        soup = bs(response.content,'html.parser')
        comtag = {}
        comtag['Link'] = link
        try:
            comtag['Komentari'] = int(soup.find(class_='comments').find('a').text)
        except:
            comtag['Komentari'] = 0
        try:
            comtag['Foto'] = soup.find('meta', property='og:image')['content']
        except:
            comtag['Foto'] = None
        list_dict.append(comtag)
    return list_dict
