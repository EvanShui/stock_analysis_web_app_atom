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

stock_ticker = "atvi"

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
sources_list = np.array([data_to_CDS(stock_ticker, date) for date in dates])
source_wrapper = ColumnDataSource(data=dict(arg=sources_list))
#print(sources_list)
tools_lst = "pan,wheel_zoom,box_zoom,reset"
date_titles = ["week", "month", "3 months", "6 months", "year", "5 years"]
figures_list = [figure(width=700, height=500, tools=tools_lst,
           title=title) for title in date_titles]
fig_source_list = zip(figures_list, sources_list)
for fig, source in fig_source_list:
    plot(fig,source)

fig_date_titles_list = zip(figures_list, date_titles)

tab_list = [Panel(child=fig, title=date_title) for fig,date_title in fig_date_titles_list]
#print(tab_list[0]._property_values['child']._property_values['y_range'])
tabs = Tabs(tabs=tab_list)
print(tabs._property_values['tabs'][0]._property_values['child'])

#print(figures_list)

y2=[10,9,8,7,6]

def web_scraper(x_coord):
    opener = urllib.request.build_opener()
    #url for search query
    url = "https://www.google.com/search?source=hp&q=" + str(x_coord)
    return url

def button_click():
    output.text += "hello"

button_callback = CustomJS(args=dict(text_input=text_input, output=output,source_wrapper=source_wrapper),code="""
     //var plot_data = source.data;
     var ticker = text_input.value;
     //iterate through source wrapper class, edit all of the y-values, go from there.
     var sources_list = source_wrapper.data['arg']
     console.log(sources_list.length)
     for (var i = 0; i < sources_list.length; i++){
        console.log(sources_list[i])
     }

     jQuery.ajax({
        type: 'POST',
        url: '/update_y_data',
        data: {"ticker_sent": ticker},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
            //output.text += ticker
            //plot_data['y'] = json_from_server[ticker];
            //source.trigger('change');
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """)

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

button.js_on_event(ButtonClick, CustomJS(code="console.log('hello')"))
button2.js_on_event(ButtonClick, button_callback)
#prepare some data


#create a figure object
f=figure()

#create line plot
f.line('x','y',source=source)
f.js_on_event('tap', tap_callback)

lay_out = column(row(column(text_input,output), column(button,button2)), tabs)

js,div=components(lay_out, INLINE)

cdn_js=INLINE.render_js()
cdn_css=INLINE.render_css()


#write the plot in the figure object
#show(f)
