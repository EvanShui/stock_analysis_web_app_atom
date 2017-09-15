#Making a basic Bokeh line graph

#importing Bokeh
from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool, Div, Button
from bokeh.models.widgets import Panel, Tabs, TextInput, Button, Paragraph, CheckboxButtonGroup
from datetime import date, timedelta
from dateutil.relativedelta import *
from bokeh.layouts import layout, row, column, widgetbox
from bokeh import events
import numpy as np
import pandas as pd
import requests
from bokeh.palettes import Spectral4
import json
from flask import Flask, render_template, jsonify, request, url_for
from jinja2 import Template
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import math
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import re
from bokeh.resources import INLINE
from bokeh.events import ButtonClick

stock_ticker = "nflx"

x=[1,2,3,4,5]
y=[6,7,8,9,10]

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

text_input = TextInput()
button = Button(label="main")
button2 = Button()
output=Paragraph()
output.text = "goodbye"

def data_to_CDS(stock_ticker, start_date):
    df = data.DataReader(name=stock_ticker, data_source="google", start=start_date, end=date.today())
    df['stock_ticker'] = stock_ticker
    source = ColumnDataSource(data=dict(
        date=np.array(df['Close'].index, dtype=np.datetime64),
        price=np.array(df['Close'].values),
        ticker=np.array(df['stock_ticker'])
    ))
    return source

def plot(p, source):
    return (p.line('date', 'price', source=source, line_width=2))

source = ColumnDataSource(data=dict(x=x,y=y))
sources_list = [data_to_CDS(stock_ticker, date) for date in dates]
print(dates)
source_wrapper = ColumnDataSource(data=dict(arg=sources_list))
#print(sources_list)
tools_lst = "pan,wheel_zoom,box_zoom,reset"
date_titles = ["week", "month", "3 months", "6 months", "1 year", "5 years"]
figures_list = [figure(x_axis_type='datetime', width=700, height=500, tools=tools_lst,
           title=title) for title in date_titles]
print(figures_list)
fig_source_list = zip(figures_list, sources_list)
fig_date_titles_list = zip(figures_list, date_titles)
for fig, source in fig_source_list:
    plot(fig,source)
tab_list = [Panel(child=fig, title=date_title) for fig, date_title in fig_date_titles_list]
#tab_list = [Panel(child=figures_list[0], title=date_titles[0]), Panel(child=figures_list[1], title=date_titles[1])]
#print(tab_list[0]._property_values['child']._property_values['y_range'])
tabs = Tabs(tabs=tab_list)

curdoc().add_root(tabs)
