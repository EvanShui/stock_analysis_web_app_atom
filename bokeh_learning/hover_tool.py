#importing libraries
from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool
from bokeh.models.widgets import Panel, Tabs, TextInput, Button, Paragraph, CheckboxButtonGroup
from datetime import date, timedelta
from dateutil.relativedelta import *
from bokeh.layouts import layout, row, column
from bokeh import events
import numpy as np
import pandas as pd
import requests
from bokeh.palettes import Spectral4

#string datetime -> CDS
#creates a dataframe object which includes stock info about the given stock ticker
#such as closing and opening price between the datetime object that is passed
#to the function and the current date. Returns a column data source object that
#contains all of said data.
def data_to_CDS(stock_ticker, start_date):
    df = data.DataReader(name=stock_ticker, data_source="google", start=start_date, end=date.today())
    df['stock_ticker'] = stock_ticker
    source = ColumnDataSource(data=dict(
        date=np.array(df['Close'].index, dtype=np.datetime64),
        price=np.array(df['Close'].values),
        ticker=np.array(df['stock_ticker'])
    ))
    return source

stock_ticker="atvi"
delta_year = date.today() + relativedelta(years=-1)
source = data_to_CDS(stock_ticker, delta_year)
figure = figure(x_axis_type='datetime', width=1200, height=400, tools="tap", title="year")
figure.line('date','price',source=source,line_width=2)
figure.add_tools(HoverTool(tooltips=[
    ("date", "@date{%F}"),
    ("Price", "$@price{0.2f}"),
    ("index", "$index"),
    ("stock_ticker", "@ticker")
    ],
    formatters={
        "date": "datetime"
    },
    mode="vline"
))
