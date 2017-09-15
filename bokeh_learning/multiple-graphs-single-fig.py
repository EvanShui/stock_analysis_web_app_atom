import pandas as pd
from bokeh.io import curdoc
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from pandas_datareader import data, wb
from bokeh.models import CustomJS, HoverTool
from datetime import date
import datetime
from bokeh import events
from bokeh.models.widgets import TextInput, Button, Paragraph, CheckboxButtonGroup
from bokeh.layouts import layout, row, column
import numpy as np
from bokeh.palettes import Spectral4

def error(msg):
    output.text += msg
        var company = hovertool["attributes"][1].tooltips[3][2]
        window.open("https://www.google.com/search?q=" + day + month + string)

def update_data():
        global spectra_index_counter
        stock_data = data_to_CDS(text_input.value, start_date)
        temp = p.line('date', 'price', source=stock_data, line_width=2, color=Spectral4[spectra_index_counter], alpha=0.8, legend=stock_data.data['ticker'][0])
        spectra_index_counter += 1
        stock_list.append(temp)
        checkbox_button_group.labels.append(stock_data.data['ticker'][0])
        p.add_tools(HoverTool(renderers=[temp],
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
    #except:
    #    error("ticker not found")

def update_plot(new):
    switch=checkbox_button_group.active
    for x in range(0,len(stock_list)):
        if x in switch:
            stock_list[x].visible=True
        else:
            stock_list[x].visible=False

def data_to_CDS(stock_ticker, start_date):
    df = data.DataReader(name=stock_ticker, data_source="google", start=start_date, end=date.today())
    df['stock_ticker'] = stock_ticker.upper()
    source = ColumnDataSource(data=dict(
        date=np.array(df['Close'].index, dtype=np.datetime64),
        price=np.array(df['Close'].values),
        ticker=np.array(df['stock_ticker'])
    ))
    return source

text_input=TextInput(value="word")
button=Button(label="Generate Text")
boolean = True
output = Paragraph()
checkbox_button_group = CheckboxButtonGroup(labels=["APPL"], active=[0,1,2,3])

start_date = datetime.datetime(2016, 3, 1)
AAPL = data_to_CDS("aapl", start_date)
IBM = data.DataReader(name="IBM", data_source="google", start=start_date, end=date.today())
MSFT = data.DataReader(name="MSFT", data_source="google", start=start_date, end=date.today())
GOOG = data.DataReader(name="GOOG", data_source="google", start=start_date, end=date.today())
spectra_index_counter = 0
stock_list =[]

p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
p.title.text = 'Click on legend entries to hide the corresponding lines'
#for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
aapl_line = p.line('date', 'price', source=AAPL, line_width=2, color=Spectral4[spectra_index_counter], alpha=0.8, legend="AAPL")
spectra_index_counter += 1
stock_list.append(aapl_line)

p.add_tools(HoverTool(renderers=[aapl_line],
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



button.on_click(update_data)
checkbox_button_group.on_click(update_plot)
widgets = column(row(text_input, button), output)
lay_out = column(widgets, checkbox_button_group)

curdoc().add_root(lay_out)
curdoc().add_root(row(p))
