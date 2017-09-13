from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import Range1d
from alpha_vantage.timeseries import TimeSeries
import numpy as np
from bokeh.io import curdoc
from dateutil.relativedelta import *
from datetime import date
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import RadioButtonGroup
import time
from bokeh import events
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool, Div, Button
from bokeh.models.widgets import Panel, Tabs, TextInput, Button, Paragraph, CheckboxButtonGroup

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year, date.today()]

button = Button(label="hello")

map_ints = map(lambda date: time.mktime(date.timetuple()) * 1000, dates)
date_ints = [date_int for date_int in map_ints]
print(date_ints)

# create a new plot with a range set with a tuple
p = figure(x_axis_type="datetime")


def get_data(stock_ticker):
    ts = TimeSeries(key='VVKDMK4DCJUF1NQP', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=stock_ticker, outputsize='full')
    return data,meta_data

data,meta_data = get_data("ATVI")

def data_to_CDS(data, start_date):
    delta_days = np.busday_count(start_date, date.today())
    print(delta_days)
    adjusted_data = data['close'].tail(delta_days)
    source = ColumnDataSource(data=dict(
        date=np.array(adjusted_data.index, dtype=np.datetime64),
        price=adjusted_data.values
    ))
    return source

def my_radio_handler(new):
    print (type(new))

button_callback = CustomJS(args=dict(fig=p), code="""
            var date_ints = %s;
            console.log(cb_obj.active)
            var active_button = cb_obj.active
            //console.log(active_button)
            fig.x_range.start = date_ints[active_button]
            fig.x_range.end = date_ints[6]
            //console.log(date_ints)
        """ % (date_ints))

source = data_to_CDS(data, delta_5_year)
p.line('date', 'price', source=source, line_width=2)

radio_button_group = RadioButtonGroup(
        labels=["1w", "1m", "3m", "6m", "1y", "5y"], active=0, callback=button_callback)

# set a range using a Range1d
#button.js_on_event(events.ButtonClick, button_callback(date_ints=date_ints))
#button.js_on_event(events.ButtonClick, button_callback(date_ints=date_ints))
#radio_button_group.js_on_event('active', radio_button_callback)
#radio_button_group.on_click(my_radio_handler)
#p.x_range = Range1d(0, 5)
#p.circle([1, 2, 3, 4, 5, 25], [2, 5, 8, 2, 7, 50], size=10)

curdoc().add_root(button)
curdoc().add_root(radio_button_group)
curdoc().add_root(p)
