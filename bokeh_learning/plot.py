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
figures_list = [figure(x_axis_type='datetime', width=1300, height=400, tools=tools_lst,
           title=title) for title in date_titles]
fig_source_tuple_list = zip(figures_list, sources_list)
fig_date_titles_list = zip(figures_list, date_titles)
fig_datetime_list = zip(figures_list, dates)

#creates the figure object which serves as a foundation for the plot
figure = figure(x_axis_type='datetime', width=1200, height=400, tools="tap", title="year")

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
def click_trigger(hovertool, attributes=[], stock_string=[]):
    return CustomJS(args=dict(hovertool=hovertool), code="""
        var attrs = %s; var string = %s;
        var myDate = new Date(Math.trunc(cb_obj[attrs[0]]));
        var year = myDate.getYear();
        var month = myDate.getMonth() + 1;
        var day = myDate.getDate() + 1;
        var price = cb_obj[attrs[1]];
        var fkme = Object.entries(hovertool)
        var company = hovertool["attributes"][1].tooltips[3][2]
        console.log(Object.entries(hovertool))
        window.open("https://www.google.com/search?q=" + day + month + string)
    """ % (attributes, stock_string))

# ->
# updates the checkbox_group to include the strings written in the text_input box_zoom
def button_update():
    global spectra_index_counter
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

#added the features so that when the user's mouse hovers over a data point, it
#will display date, price, index, and the stock ticker
temp_list = []
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

for fig in figures_list:
    print(fig.tools[-1])

for fig in figures_list:
    # Triggers the click_trigger function when the mouse clicks on the graph
    fig.js_on_event(events.Tap, click_trigger(fig.tools[-1], attributes=point_attributes, stock_string=["hello"]))

#triggers the button_update function once the button is clicked
button.on_click(button_update)

#triggers the plot_update function once any of the checkbox buttons are clicked
checkbox_button_group.on_click(plot_update)

tab_list = [Panel(child=fig, title=date_title) for fig, date_title in fig_date_titles_list]
tabs = Tabs(tabs=tab_list)


widgets = column(row(text_input, button),output)
lay_out = column(widgets,checkbox_button_group)

# Adds the figure object to the document which will be sent to the Bokeh server
curdoc().add_root(lay_out)
curdoc().add_root(tabs)
