import pandas as pd
from bokeh.io import curdoc
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show
from pandas_datareader import data, wb
from bokeh.models import CustomJS
from datetime import date
import datetime
from bokeh import events
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxButtonGroup
from bokeh.layouts import layout, row, column

def update_data():
    stock_data = data.DataReader(name=text_input.value, data_source="google", start=start_date, end=date.today())
    stock_list.append(p.line(stock_data.index, stock_data['Close'], line_width=2, color="blue", alpha=0.8, legend=text_input.value))
    checkbox_button_group.labels.append(text_input.value)

def update_plot(new):
    switch=checkbox_button_group.active
    for x in range(0,len(stock_list)):
        if x in switch:
            stock_list[x].visible=True
        else:
            stock_list[x].visible=False

text_input=TextInput(value="word")
button=Button(label="Generate Text")
boolean = True
lst = ["APPL"]
checkbox_button_group = CheckboxButtonGroup(labels=lst, active=[0,1,2,3])

start_date = datetime.datetime(2016, 3, 1)
AAPL = data.DataReader(name="aapl", data_source="google", start=start_date, end=date.today())
IBM = data.DataReader(name="IBM", data_source="google", start=start_date, end=date.today())
MSFT = data.DataReader(name="MSFT", data_source="google", start=start_date, end=date.today())
GOOG = data.DataReader(name="GOOG", data_source="google", start=start_date, end=date.today())
stock_list =[]

p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
p.title.text = 'Click on legend entries to hide the corresponding lines'

#for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
stock_list.append(p.line(AAPL.index, AAPL['Close'], line_width=2, color="blue", alpha=0.8, legend="AAPL"))

button.on_click(update_data)
checkbox_button_group.on_click(update_plot)
widgets = row(text_input, button)
lay_out = column(widgets, checkbox_button_group)

curdoc().add_root(lay_out)
curdoc().add_root(row(p))
