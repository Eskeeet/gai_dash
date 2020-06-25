#!/usr/bin/env python
# coding: utf-8

# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime 
from datetime import timedelta
import pandas as pd 
import numpy as np 
import plotly.graph_objs as go 
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import re
import plotly 
from plotly.offline import plot 
import random
import yfinance as yf
#import pymongo
import dns

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import csv





app = dash.Dash('abc')
server=app.server

colors = {     
    'background': '#111111',     
    'text': '#7FDBFF' } 

app.layout = html.Div([
    html.H1(
            children='Stock Graphs',
            style={'textAlign': 'center','color': colors['text']}
    ),
        html.Img(
           src='https://images.squarespace-cdn.com/content/5c036cd54eddec1d4ff1c1eb/1557908564936-YSBRPFCGYV2CE43OHI7F/GlobalAI_logo.jpg?content-type=image%2Fpng',
           style = {'height':'11%','width':'11%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'color':colors['background']
           },
           className='two columns'),
    html.Br(),
    html.Br(),
    html.Div([
                html.H4(
                    'Select Company Stock',
                    style={'textAlign':'left','color':colors['text']}
                ),
        dcc.Dropdown(
        id='my-tickers',
        options=[
            {'label': 'MSFT', 'value': 'MSFT'},
            {'label': 'BABA', 'value': 'BABA'},
            {'label': 'SPY', 'value': 'SPY'},
            {'label': 'Coke', 'value': 'COKE'}
        ],
        value='MSFT',
    )],
        style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}

            ),
    html.Div([
                html.H4(
                    'Select Date Range',
                    style={'textAlign':'left','color':colors['text']}
                ),
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=datetime(2015,1,1),
                    max_date_allowed=datetime.today(),
                    start_date=datetime(2018,1,1),
                    end_date=datetime.today()
                )
            ],
             style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ),
    html.Div([
        dbc.Button(
            html.H4(
                'Get the Result',
                style={'textAlign':'center','color':colors['text']}
                    ),
                   id='button',
                   color='dark',
                   n_clicks=0,
                   className='mr-1')
        ],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),
    html.Div([dcc.Graph(id='candle')]),
    html.Div([dcc.Graph(id='totalreturn')]),
    html.Div([dcc.Graph(id='corheat')])

    
], style={'backgroundColor': colors['background'],'width': '500'}
)

@app.callback([Output('candle', 'figure'),
               Output('totalreturn', 'figure'),
               Output('corheat', 'figure')
              ], 
              [Input('button', 'n_clicks')],
              [State('my-tickers', 'value'),
               State('date-range', 'start_date'),
               State('date-range', 'end_date')])
def update_graph(n_clicks,selected_dropdown_value,start_date,end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    dfcomb = pd.DataFrame(yf.download([selected_dropdown_value,'SPY'],start,end)['Adj Close']).reset_index()
    df = pd.DataFrame(yf.download(selected_dropdown_value,start,end)).reset_index()
    df1 = pd.DataFrame(yf.download(selected_dropdown_value,start,end))['Adj Close'].reset_index()
    dfspy = pd.DataFrame(yf.download('SPY',start,end)['Adj Close']).reset_index()


    temp1 = (df1['Adj Close'].iloc[-1]/df1['Adj Close'].iloc[0]) * 100 - 100
    temp2 = (dfspy['Adj Close'].iloc[-1]/dfspy['Adj Close'].iloc[0]) * 100 - 100
    df['MA30'] = df.Close.rolling(30).mean()
    df['MA100'] = df.Close.rolling(100).mean()
    
    cd = go.Figure(data = [go.Candlestick(
        yaxis='y2',
        x = df.Date,
        open = df.Open,
        high = df.High,
        low = df.Low,
        close = df.Close,
        name = selected_dropdown_value + ' Candlestick'
        ), go.Scatter(
        yaxis='y2',
        x = df.Date,
        y = df.MA30,
#         mode = 'lines',
        name = 'MA30',
        line = {'color': 'rgb(219, 64, 82)','width': 1}
        ), go.Scatter(
        yaxis='y2',
        x = df.Date,
        y = df.MA100,
#         mode = 'lines',
        name = 'MA100',
        line = {'color': 'green','width': 1}
        ), go.Bar(
        x=df.Date, 
        y=df.Volume,                          
        yaxis='y', 
        name='Volume',
#         mode = "markers",
        marker = {'color': colors['text']}
        )],
            
        layout= {'paper_bgcolor':'rgba(0,0,0,0)',
                 'plot_bgcolor':'rgba(0,0,0,0)',
                 'yaxis':{ 'domain': [0, 0.2] },
                 'yaxis2':{ 'domain' : [0.2, 0.8] },
                 'title':"Candlestick With MA And Volume",
                 'font':{'size':18, 'color':colors['text']}
                }
              )
    barr = go.Figure(data = [go.Bar(
        x = [selected_dropdown_value, 'SPY'],
        y = [temp1,temp2],
        
        )],
        layout = {'yaxis':{'title':"Return Percentage"},
                  'paper_bgcolor':'rgba(0,0,0,0)',
                  'plot_bgcolor':'rgba(0,0,0,0)',
                  'title':"Return: STOCK VS SPY",
                  'font':{'size':18, 'color':colors['text']}
                 }
        )
    corheat = go.Figure(data = [go.Heatmap(
        x = [selected_dropdown_value, 'SPY'],
        y = [selected_dropdown_value, 'SPY'],
        z=dfcomb.corr(),
        colorscale='Jet'
        
        )],
        layout = {'paper_bgcolor':'rgba(0,0,0,0)',
                  'plot_bgcolor':'rgba(0,0,0,0)',
                  'title':"Correlation Between STOCK AND SPY",
                  'font':{'size':18, 'color':colors['text']}
                 }
        )
    return cd,barr, corheat





if __name__ == '__main__':
    app.run_server()




