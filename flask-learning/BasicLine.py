#Making a basic Bokeh line graph

#importing Bokeh
import pandas_datareader.data as web
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
from alpha_vantage.timeseries import TimeSeries
import math
from bokeh.models.widgets import RadioButtonGroup
import time

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

stock_ticker = "nflx"

def get_data(stock_ticker):
    ts = TimeSeries(key='VVKDMK4DCJUF1NQP', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=stock_ticker, outputsize='full')
    return data,meta_data

data,meta_data = get_data(stock_ticker)

x=[1,2,3,4,5]
y=[6,7,8,9,10]

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months,delta_year, delta_5_year, date.today()]

map_ints = map(lambda date: time.mktime(date.timetuple()) * 1000, dates)
date_ints = [date_int for date_int in map_ints]

tools_lst = "pan,wheel_zoom,box_zoom,reset"
date_titles = ["week", "month", "3 months", "6 months", "1 year", "3 years"]

text_input = TextInput()
button = Button(label="main")
button2 = Button()
output=Paragraph()
output.text = "goodbye"

def data_to_CDS(stock_ticker, data, start_date):
    delta_days = np.busday_count(start_date, date.today())
    print(delta_days)
    data['ticker'] = stock_ticker
    adjusted_data = data.tail(delta_days)
    source = ColumnDataSource(data=dict(
        date=np.array(adjusted_data['close'].index, dtype=np.datetime64),
        price=adjusted_data['close'].values,
        index=adjusted_data['ticker']
    ))
    return source

def data_to_CDS_y(data, start_date):
    delta_days = np.busday_count(start_date, date.today())
    print("y",delta_days)
    adjusted_data = data['close'].tail(delta_days)
    return (np.array(adjusted_data.index, dtype=np.datetime64).tolist(), np.array(adjusted_data.values).tolist())

p = figure(x_axis_type="datetime", tools=tools_lst)
source = data_to_CDS(stock_ticker, data, delta_5_year)
p.line('date', 'price', source=source, line_width=2)

def web_scraper(x_coord):
    opener = urllib.request.build_opener()
    #url for search query
    url = "https://www.google.com/search?source=hp&q=" + str(x_coord)
    return url

def button_click():
    output.text += "hello"

button_callback = CustomJS(args=dict(text_input=text_input, output=output, source=source),code="""
     //var plot_data = source.data;
     var ticker = text_input.value;
     jQuery.ajax({
        type: 'POST',
        url: '/update_y_data',
        data: {"ticker_sent": ticker},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
            var updated_price_list = json_from_server[ticker];
            //source.data['date'] = json_from_server[ticker][0]
            source.data['price'] = json_from_server[ticker][1];
            source.trigger('change');
            var actual_ticker = %r;
            console.log(actual_ticker)
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """ % (stock_ticker))

tap_callback = CustomJS(args=dict(output=output), code="""
    var x_coordinate = cb_obj['x']
    console.log("hello")
    jQuery.ajax({
        type: 'POST',
        url: '/get_data',
        data: {"x_coord": x_coordinate},
        dataType: 'json',
        success: function (json_from_server) {
            //assigns the list that was sent from the flask route /get_new_data
            var url = json_from_server[x_coordinate]
            //iterates through the list and adds each element (the search query title)
            //to div
            console.log("loading")
            output.text += url
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """)


radio_button_callback = CustomJS(args=dict(fig=p), code="""
            var date_ints = %s;
            var active_button = cb_obj.active
            var stock_ticker = %r;
            console.log(active_button)
            fig.x_range.start = date_ints[active_button]
            fig.x_range.end = date_ints[6]
            jQuery.ajax({
                type: 'POST',
                url: '/resize_y_range',
                data: {"index": active_button},
                dataType: 'json',
                success: function (json_from_server) {
                    var test = json_from_server[active_button]
                    console.log("loading")
                    console.log(test)
                },
                error: function() {
                    alert("Oh no, something went wrong. Search for an error " +
                          "message in Flask log and browser developer tools.");
                }
            });
        """ % (date_ints, stock_ticker))

button2.js_on_event(ButtonClick, button_callback)

radio_button_group = RadioButtonGroup(
        labels=["1w", "1m", "3m", "6m", "1y", "5y"], active=5, callback=radio_button_callback)
lay_out = column(radio_button_group, row(text_input, button2), p)

js,div=components(lay_out, INLINE)

cdn_js=INLINE.render_js()
cdn_css=INLINE.render_css()

#write the plot in the figure object
#show(f)
