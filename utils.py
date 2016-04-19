import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
import matplotlib as mpl
import pandas as pd
import requests
from pokereval import PokerEval
pokereval=PokerEval()
from bs4 import  BeautifulSoup
from ipywidgets import interact, fixed
import ipywidgets as widgets
from IPython.display import HTML, YouTubeVideo, Image, display
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)
plt.rc('lines', linewidth=5)
plt.rc('figure', figsize=[14.0, 10.0])
#plt.rc('font', family=["Microsoft JhengHei"])
plt.rcParams['text.usetex']=False
def pretty_card(c):
    return c[0]+'$\\'+{'h': 'heart', 'd':'diamond', 's':'spade', 'c':'club'}[c[1].lower()]+'suit$'
def pretty_cards(cards):
    return " ".join(map(pretty_card, cards))
def str2cards(s):
    if type(s) is str:
        return [s[i:i+2] for i in range(0, len(s),2)]
    else:
        return list(s)

def poker_eval(pockets, board, **kw):
    pockets = [str2cards(x) for x in pockets]
    board = str2cards(board)
    img_style = "float: left; width: 12%; margin-right: 1%; margin-bottom: 0em;margin-top: 0em"
    result = pokereval.poker_eval(game='holdem', fill_pockets=1, pockets=pockets, board=board, **kw)
    sizes = [x['ev'] for x in result['eval']]
    labels = [pretty_cards(x) for x in pockets]
    prop = fm.FontProperties()
    prop.set_size(30)
    explode = (0.1,)+(0,)*(len(pockets)-1)
    pie = plt.pie(sizes, labels=labels, shadow=True, autopct="%2.2f%%", startangle=90, explode=explode)
    plt.axis("equal")
    plt.setp(pie[2], fontproperties=prop)
    display(HTML("<div>"+"".join('<img src="cards/%s.png" style="%s" />'%(b, img_style) for b in board if b!="__")+"</div>"))
    return sizes

def preflop(*pockets, **kw):
    return poker_eval(pockets=list(pockets), board=["__"]*5, **kw)

def show_html(html, noclass=False):
    if noclass and 'class' in html.attrs:
        html=BeautifulSoup(str(html)).body.contents[0]
        del html.attrs['class']
    display(HTML(str(html)))

def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    for s in soup.findAll('span', attrs={'class':'sortkey'}):
        s.extract()
    return soup

def show_bio(name):
    url = 'http://en.wikipedia.org/wiki/'
    table = get_html(url+name).find('table', attrs={'class':'vcard'})
    table.attrs['style']='width: 80%'
    for img in table.findAll('img'):
        img.parent.attrs['class']='zoom_img'
    show_html(table)