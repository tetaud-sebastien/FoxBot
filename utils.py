#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import plotly.graph_objects as go
from datetime import datetime
import os
import smtplib
import ssl



class ExchangeLog():
    """Log to an exchange from a given JSON config file by using ccxt library

    """

    def __init__(self, exchange_id, conf_path):

        """Extract exchange name, api credential, type of account
        """

        self.exchange_id = exchange_id
        self.conf_path = conf_path
        print("Log to %s ..." %(self.exchange_id))
        if os.path.isfile(self.conf_path):
            
            self.exchange_conf = pd.read_json(conf_path)
            self.api_key = self.exchange_conf['exchange'][self.exchange_id]['api_source_key']
            self.secret_key = self.exchange_conf['exchange'][self.exchange_id]['api_source_secret']
            self.exchange_type = self.exchange_conf['exchange'][self.exchange_id]['type']         
        else:
            print('Could not find the config file to log')

    def log(self):

        """log to the exchange with the credentials from the config file.

        Returns:
            [class]: return an intentiate class of the logged exchange
        """

        exchange_class = getattr(ccxt, self.exchange_id)
        exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'timeout': 50000,
            'enableRateLimit': True,
            'options': {
                'defaultType': self.exchange_type,
            },
        })
        print("Succesfully logged to %s" %(self.exchange_id))
        return exchange


def fetch_ohlcv(exchange, symbol, candle):
    
    candles= exchange.fetch_ohlcv (symbol, candle) 
    df=pd.DataFrame(candles)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Date']= df.apply(lambda row: datetime.fromtimestamp(int(str(row['Date'])[:10])), axis = 1)
    df = df.set_index('Date')
    return df


def basicPlot(ohlc, symbol, candle):
    
    

    fig = go.Figure(data=[go.Candlestick(x=ohlc.index,
                open=ohlc['Open'],
                high=ohlc['High'],
                low=ohlc['Low'],
                close=ohlc['Close'])])
    fig.update_layout(
        title= symbol + " - " + candle,
        xaxis_title="Date",
        yaxis_title="Price [$]",
        legend_title="Legend Title")


    fig.update_layout(autosize=True)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


def send_notification(text, conf_path):

    if os.path.isfile(conf_path):
        conf = pd.read_json(conf_path)
        email = conf['email']['email_adress']
        password = conf['email']['email_password']

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sent_from = email
    to = [email]
    subject = f'Sneaky Bot'
    body = text
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sent_from, password)
            server.sendmail(sent_from, to, message)

    except Exception as e:
        print(e)


def check_nb_open_orders(exchange, side, symbol):
    
    list_open_orders = exchange.fetch_open_orders(symbol=symbol)
    list_order_symbol = []
    for i in range(len(list_open_orders)):
    
        if list_open_orders[i]['symbol'] == symbol and list_open_orders[i]['info']['side']==side:
            list_order_symbol.append(list_open_orders[i])
            
    nb_open_orders = len(list_order_symbol)
    return nb_open_orders





