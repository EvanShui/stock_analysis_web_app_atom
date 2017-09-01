#importing libraries
from pandas_datareader import data, wb
import datetime
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool
from bokeh.models.widgets import Panel, Tabs
from datetime import date, timedelta
from dateutil.relativedelta import *
from bokeh import events
import numpy as np
import pandas as pd
import requests

#constants

#to be used in tangent with the click_trigger function to pass the x and y
#coordinates of the mouse.
point_attributes = ['x','y','sx','sy']

#the stock ticker that is used to test for stock
stock_ticker="atvi"

#a list of titles for all of the tabs
date_titles = ["week", "month", "3 months", "6 months", "year", "5 years"]

#a list of tool that will be displayed along side the figure
tools_lst = "pan,wheel_zoom,box_zoom,reset"

##date constants
delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)


#list of dates to iterate through to create graphs for different time periods
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]


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
        stock=np.array(df['stock_ticker'])
    ))
    source_ticker = ColumnDataSource(data=dict(stock=np.array(df['stock_ticker'])))
    return source


# Figure CDS ->
# Plots the data as a scatter plot and a line graph on the figure p.
def plot(p, source):
    p.line('date', 'price', source=source, line_width=2)
    p.circle('date', 'price', size=5, source=source, fill_color='white')


# CDS list -> CustomJS
# Returns a CustomJS object that once implemented, will open up a new tab
# in the browser window once the Events.tap event is fired. Once triggered,
# the tab's search query includes the date that the mouse was hovering over
# as well as the stock_ticker of the graph
def click_trigger(attributes=[], stock_string=[]):
    return CustomJS(code="""
        var attrs = %s; var string = %s;
        var myDate = new Date(Math.trunc(cb_obj[attrs[0]]));
        var year = myDate.getYear();
        var month = myDate.getMonth() + 1;
        var day = myDate.getDate() + 1;
        var price = cb_obj[attrs[1]];
        window.open("https://www.google.com/search?q=" + day + month + string)
    """ % (attributes, stock_string))

#sets the source variable to the CDS object containing stock data
#sets the CDS_ticker variable to the CDS object containing the stock_ticker
#source, CDS_ticker = data_to_CDS(stock_ticker, delta_year)
sources_list = [data_to_CDS(stock_ticker, date) for date in dates]
figures_list = [figure(x_axis_type='datetime', width=1300, height=400, tools=tools_lst,
           title=title) for title in date_titles]
fig_source_tuple_list = zip(figures_list, sources_list)
fig_date_tuple_list = zip(figures_list, date_titles)

#creates the figure object which serves as a foundation for the plot
figure = figure(x_axis_type='datetime', width=1200, height=400, tools="tap", title="year")

#added the features so that when the user's mouse hovers over a data point, it
#will display date, price, index, and the stock ticker
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
    #calls the plot function to graph the source data
    plot(fig, source)

for fig in figures_list:
    # Triggers the click_trigger function when the mouse clicks on the graph
    fig.js_on_event(events.Tap, click_trigger(attributes=point_attributes, stock_string=["hello"]))

tab_list = [Panel(child=fig, title=date_title) for fig, date_title in fig_date_tuple_list]
tabs = Tabs(tabs=tab_list)

# Adds the figure object to the document which will be sent to the Bokeh server
curdoc().add_root(tabs)
