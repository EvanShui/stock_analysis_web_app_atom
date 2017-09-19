#importing libraries
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

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

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

#constants

#creating the flask app
app = Flask(__name__)

#to be used in tangent with the click_trigger function to pass the x and y
#coordinates of the mouse.
point_attributes = ['x','y','sx','sy']

#the stock ticker that is used to test for stock
stock_ticker="atvi"

#a list of titles for all of the tabs
date_titles = ["week", "month", "3 months", "6 months", "year", "5 years"]

#a list of tool that will be displayed along side the figure
tools_lst = "pan,wheel_zoom,box_zoom,reset"

#a list of dimensions for the divs
div_dim_lst = [500] * 6

#a list of line instances
instances_list = []

#a counter to iterate through the different colors of the spectra palette
spectra_index_counter = 1

##date constants
#delta 7 days will be designated date for testing multiple graphs single figure
delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)

##widgets
text_input=TextInput(value="ticker")
button=Button(label="Submit")
output=Paragraph()
checkbox_button_group = CheckboxButtonGroup(labels=["ATVI"],active=[0])

#list of dates to iterate through to create graphs for different time periods
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]

#sets the source variable to the CDS object containing stock data
#sets the CDS_ticker variable to the CDS object containing the stock_ticker
sources_list = [data_to_CDS(stock_ticker, date) for date in dates]

#sets the figure_list variable to a list of Figure objects each one contains
#a title from the date_titles list
figures_list = [figure(x_axis_type='datetime', width=700, height=500, tools=tools_lst,
           title=title) for title in date_titles]
fig_source_tuple_list = zip(figures_list, sources_list)
fig_date_titles_list = zip(figures_list, date_titles)
fig_datetime_list = zip(figures_list, dates)

#added the features so that when the user's mouse hovers over a data point, it
#will display date, price, index, and the stock ticker
temp_list = []

# Figure CDS ->
# Plots the data as a scatter plot and a line graph on the figure p.
def plot(p, source):
    return (p.line('date', 'price', source=source, line_width=2))
    #p.circle('date', 'price', size=5, source=source, fill_color='white')

# CDS list -> CustomJS
# Returns a CustomJS object that once implemented, will open up a new tab
# in the browser window once the Events.tap event is fired. Once triggered,
# the tab's search query includes the date that the mouse was hovering over
# as well as the stock_ticker of the graph

# ->
# toggles the visibility of the chosen stock data when the checkbox group is clicked on
def plot_update(new):
    switch=checkbox_button_group.active #[0]
    for x in range(0,len(instances_list)):
        if x in switch:
            for instance in instances_list[x]:
                instance.visible = True
        else:
            for instance in instances_list[x]:
                instance.visible = False

def web_scraper(day, month, year):
    lst = []
    opener = urllib.request.build_opener()
    #url for search query
    url = "http://www.marketwatch.com/search?q=ATVI&m=Ticker&rpp=15&mp=2005&bd=true&bd=false&bdv=" + str(month) + "%2F" + str(day) + "%2F20" + str(year) + "&rs=true"
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    #use beauitful soup to find all divs with the r class, which essentially
    #is the same as finding all of the divs that contain each individiaul search
    soup_tuple_list = zip(soup.findAll(class_="searchresult"), soup.findAll(class_="deemphasized")[1:-1])
    #iterating through a tags which includes title and links
    for article, date in soup_tuple_list:
        try:
            time = date.contents[1][5:]
            time = re.findall(r'\|.[A-Za-z ]*', time)[0]
            info = date.contents[0].string + time
            article.a['target']="_blank"
            lst.append((article.a.encode("utf-8"),info))
        except:
            #article.a['target']="_blank"
            #lst.append((article.a.encode("utf-8")))
            #print(article.a.encode("utf-8"))
            continue
    return lst

@app.route("/data",methods=['POST'])
def get_coord():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    #the data retrieved is in the form of a string, turn it into float to perform arithmetic operations
    variable_to_return = float(request.form['x_coord'])
    day = request.form['day']
    month = request.form['month']
    year = request.form['year']
    #creates the list of data given the x-coordinate of the mouse and assigns the resulting list
    list_to_return = web_scraper(day, month, year)
    app.logger.info(
        "x_coord %r", (variable_to_return))
    app.logger.info(
        "date %d %d %d", (day, month, year))
    #app.logger.info(
    #    "list %r",(list_to_return))
    #returns a list in form of json
    return jsonify({variable_to_return: list_to_return})


@app.route("/")
def home():
    for fig, source in fig_source_tuple_list:
        fig.add_tools(HoverTool(tooltips=[
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
        #calls the plot function to graph the source data
        temp_list.append(plot(fig, source))
    instances_list.append(temp_list)
    # ->
    # updates the checkbox_group to include the strings written in the text_input box_zoom
    def button_update():
        global spectra_index_counter
        output.text += "triggered"
        temp_list = []
        output.text += text_input.value
        checkbox_button_group.active.append(checkbox_button_group.active[-1] + 1)
        checkbox_button_group.labels.append(text_input.value.upper())
        for indexer in range(0,len(dates)):
            stock_data = data_to_CDS(text_input.value, dates[indexer])
            line_instance = figures_list[indexer].line('date','price',
                source=stock_data, line_width=2, color=Spectral4[spectra_index_counter],
                alpha=0.8, legend=stock_data.data['ticker'][0])
            temp_list.append(line_instance)
            figures_list[indexer].add_tools(HoverTool(renderers=[line_instance],
                tooltips=[
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
        instances_list.append(temp_list)
        output.text += str(len(instances_list))
        spectra_index_counter += 1

    def tap_callback(div_arg):
        return CustomJS(args=dict(div=div_arg),code="""
        var x_coordinate = cb_obj['x']
        var myDate = new Date(Math.trunc(cb_obj['x']));
        var year = myDate.getYear() - 100;
        var month = myDate.getMonth() + 1;
        var day = myDate.getDate() + 1;
        console.log("hello")
        jQuery.ajax({
            type: 'POST',
            headers: {"Content-Type": "application/json"},
            url: '/data',
            data: {"x_coord": x_coordinate, "day":day, "month":month,"year":year},
            dataType: 'json',
            success: function (json_from_server) {
                //console.log(JSON.stringify(json_from_server));
                //console.log(json_from_server[x_coordinate])
                //assigns the list that was sent from the flask route /get_new_data
                div.text = ""
                var list = json_from_server[x_coordinate]
                //iterates through the list and adds each element (the search query title)
                //to div
                for(var i =0; i < list.length; i++){
                    var article = list[i][0]
                    var info = list[i][1]
                    var line = "<p>" + article + "<br>" + info + "</p>"
                    var lines = div.text.concat(line)
                    div.text = lines
                }
                console.log("loading")
            },
            error: function() {

                alert("Oh no, something went wrong. Search for an error " +
                      "message in Flask log and browser developer tools.");
            }
        });
        """)

    #tab_list = [Panel(child=lay_arg, title=date_title) for lay_arg, date_title in layout_date_titles_list]
    tab_list = [Panel(child=fig, title=date_title) for fig,date_title in fig_date_titles_list]
    print(tab_list)
    tabs = Tabs(tabs=tab_list)
    #generating another URL for flask, this time to search the x-coordinate of
    #the mouse and send back the results
    div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
    remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
    are <i>200</i> and <i>100</i> respectively.""", width=800, height=500)
    for fig in figures_list:
        fig.js_on_event('tap', tap_callback(div))
    #triggers the button_update function once the button is clicked
    button.js_on_event(events.ButtonClick, button_update)

    #triggers the plot_update function once any of the checkbox buttons are clicked
    checkbox_button_group.js_on_event(events.ButtonClick, plot_update)

    widgets = column(row(text_input, button),output, checkbox_button_group)

    lay_out = column(widgets, row(tabs,div))
    script, div = components(lay_out, INLINE)
    return render_template('index.html',
                           script=script,
                           div=div,
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css())

if __name__ == "__main__":
    app.run(debug=True)
