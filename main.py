from tkinter import *
from pycoingecko import CoinGeckoAPI
import pprint
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.crypto
chart = db.chart

cg = CoinGeckoAPI()

root = Tk()
root.geometry("1200x500")
root.option_add("*Font", (None, 30))

bet = 1
Y = []
total = 0.0
T = []
P = []
X = cg.get_coin_market_chart_by_id('bitcoin', 'usd', '4000') # chart.find_one() 
z, current_price = X['prices'][-1]
priv_asset = 'bitcoin'

def change(var):
    total_label.config(text="{:.2f}".format(T[-long.get()-1]))
    a, b = X['prices'][-long.get()-1]
    price_label.config(text="{:.15f}".format(b))
    date_label.config(text=datetime.strftime(datetime.fromtimestamp(a/1000), '%Y/%m/%d'))

def refresh():
    global priv_asset
    global X
    global T
    global Y
    global P
    X = []
    T = []
    Y = []
    P = []
    X = cg.get_coin_market_chart_by_id(selectetKatVar.get(), 'usd', '4000')
    z, current_price = X['prices'][-1]
    if priv_asset != selectetKatVar.get():
        enter_bet.delete(0, END)
        enter_bet.insert(0, "1")
        enter_price.delete(0, END)
        enter_price.insert(0, "{:.8f}".format(current_price))
        priv_asset = selectetKatVar.get()
    for i in X['prices']:
        x, price = i
        spot = float(enter_bet.get())/price
        Y.append(spot)
        P.append(price)
    l = len(Y)
    for i in range(l):
        sum = 0
        for k in range(l-i):
            sum = sum + Y[i+k]
        T.append(sum*float(enter_price.get()))

    global long
    long.destroy()
    total_label.pack_forget()
    price_label.pack_forget()
    date_label.pack_forget()
    long = Scale(root, 
            from_=len(X['prices'])-1, 
            to=0, 
            orient=HORIZONTAL, 
            length=1100, 
            width=30, 
            cursor='dot', 
            sliderlength=30, 
            repeatdelay=30, 
            command=change)
    long.set(0)
    long.pack()
    total_label.pack()
    price_label.pack()
    date_label.pack()

def showChart():
    plt.hist(P, 3414)
    plt.show() 

for i in X['prices']:
    x, price = i
    spot = bet/price
    Y.append(spot)
    P.append(price)

l = len(Y)
for i in range(l):
    sum = 0
    for k in range(l-i):
        sum = sum + Y[i+k]
    T.append(sum*current_price)

print("Totals len", len(T))

assets = [
    'bitcoin',
    'ethereum',
    'cardano',
    'polkadot',
    'solana',
    'dogecoin',
    'shiba-inu'
]

selectetKatVar = StringVar(root)
selectetKatVar.set(assets[0])

asset = OptionMenu(root, selectetKatVar,
                         *assets)
asset.pack()
enter_bet = Entry(root, width=4)
enter_bet.pack()
enter_bet.insert(0, 1)
enter_price = Entry(root, width=12)
enter_price.pack()
enter_price.insert(0, "{:.2f}".format(current_price))
refresh_button = Button(root, text='Refresh', command=refresh)
refresh_button.pack()

long = Scale(root, 
            from_=len(X['prices'])-1, 
            to=0, 
            orient=HORIZONTAL, 
            length=1100, 
            width=30, 
            cursor='dot', 
            sliderlength=30, 
            repeatdelay=30, 
            command=change)
long.set(0)
long.pack()

total_label = Label(root, text='')
total_label.pack()
price_label = Label(root, text='')
price_label.pack()
date_label = Label(root, text='')
date_label.pack()
chart_button = Button(root, text='Chart', command=showChart)
chart_button.pack()

mainloop()