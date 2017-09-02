#-| bokeh serve
#-|

import pandas as pd
from bokeh.io import curdoc,output_file, show
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import *

#Widgets

ticker = TextInput(title='Ticker Symbol',value='IBM')
button=Button(label='Lookup',button_type='success')
log = Paragraph(text="""log""",
width=200, height=100)
cb_group = CheckboxButtonGroup(labels=['Close', 'Adj Close'],active=[0,1])
cb_group.labels.append('Placebo')

#Plot

p = figure(title='',width=500, height=250, x_axis_type='datetime')

source = ColumnDataSource({'x': [], 'y1': [],'y2': []})

lineClose=p.line('x','y1',source=source, color='navy', alpha=0.5)
lineAdj=p.line('x','y2',source=source, color='red', alpha=0.5)

lines=[lineClose,lineAdj]

#Event handling

def error(msg):
    log.text=msg

def update_data():
    try:
        src='http://ichart.yahoo.com/table.csv?s={symb}&a=0&b=1&c=2011&d=0&e=1&f=2016'.format(symb=ticker.value)
        df=pd.read_csv(src,parse_dates=['Date'])
        source.data=({'x': df['Date'], 'y1': df['Close'],'y2': df['Adj Close']})
    except:
        error('Error ticker')

def update_plot(new):

    switch=cb_group.active
    for x in range(0,len(lines)):
        if x in switch:
            lines[x].visible=True
        else:
            lines[x].visible=False

    error('<CheckboxButtonGroup>.active = '+str(switch))

button.on_click(update_data)
cb_group.on_click(update_plot)


inputs=widgetbox(ticker,button,cb_group,log)

curdoc().add_root(row(inputs,p,width=800))
curdoc().title = 'Bokeh Checkbox Example'
button.clicks=1
