from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import output_notebook
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from datetime import date, timedelta
from dateutil.relativedelta import *
from bokeh import events
import numpy as np
import pandas as pd
import requests

def new_window():
    return CustomJS(code="""
        window.open("https://www.google.com/search?q=")
    """)

def data_to_CDS(stock_ticker, start_date):
    df = data.DataReader(name=stock_ticker, data_source="google", start=start_date, end=date.today())
    df['stock_ticker'] = stock_ticker
    source = ColumnDataSource(data=dict(
        date=np.array(df['Close'].index, dtype=np.datetime64),
        price=np.array(df['Close'].values),
        stock=np.array(df['stock_ticker'])
    ))
    return source


def plot(p, source):
    p.line('date', 'price', source=source, line_width=2)
    p.circle('date', 'price', size=5, source=source, fill_color='white')


def string_to_datetime(string):
    return datetime.datetime.fromtimestamp(string / 1e3)

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]

date_titles = ["week", "month", "3 months", "6 months", "year", "5 years"]
start = datetime.datetime(2016, 3, 1)
#url ="https://www.google.com/search?q="

sources_list = [data_to_CDS(stock_ticker, date) for date in dates]
figures_list = [figure(x_axis_type='datetime', width=1500, height=400, tools="tap",
           title=title) for title in date_titles]
fig_source_tuple_list = zip(figures_list, sources_list)
fig_date_tuple_list = zip(figures_list, date_titles)

for fig, source in fig_source_tuple_list:
    fig.add_tools(HoverTool(tooltips=[
        ("date", "@date{%F}"),
        ("Price", "$@price{0.2f}"),
        ("index", "$index"),
        ("stock_ticker", "@stock")
    ],
        formatters={
            "date": "datetime"
        },
        mode="vline"
    ))
    plot(fig, source)
    #fig.select(type=TapTool).callback = OpenURL(url=url)


tab_list = [Panel(child=fig, title=date_title) for fig, date_title in fig_date_tuple_list]
tabs = Tabs(tabs=tab_list)
#output_file("python_analyzer.html")
#show(tabs)
point_attributes = ['x','y','sx','sy']








def test_window(attributes=[]):
    return CustomJS(args=dict(tick=stock_ticker_CDS), code="""
        var attrs = %s;
        var myDate = new Date(Math.trunc(cb_obj[attrs[0]]) * 1000);
        var price = cb_obj[attrs[1]]
        var tick = cb_obj[attrs[3]]
        window.open("https://www.google.com/search?q=" + myDate + price)
    """ % (attributes))

for fig in figures_list:
    fig.js_on_event(events.Tap, test_window(attributes=point_attributes))

output_file("python_analyzer.html")
show(tabs)
