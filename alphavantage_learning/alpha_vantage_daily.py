from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file, ColumnDataSource
import numpy as np
from bokeh.io import curdoc
from datetime import date
from dateutil.relativedelta import *

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)

def data_to_CDS(stock_ticker, start_date):
    delta_days = (date.today() - start_date).days
    ts = TimeSeries(key='VVKDMK4DCJUF1NQP', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=stock_ticker)
    adjusted_data = data['close'].tail(delta_days)
    source = ColumnDataSource(data=dict(
        date=np.array(adjusted_data.index, dtype=np.datetime64),
        price=adjusted_data.values
    ))
    return source

ts = TimeSeries(key='VVKDMK4DCJUF1NQP', output_format='pandas')
data, meta_data = ts.get_daily(symbol='MSFT')
#print(data['close'].tail(7))
#print(type(data.index[0]))
source = ColumnDataSource(data)
#print(source.data['close'].index)

#print(type(source2.data['date'][0]))
#print(source2.data['price'])

source = data_to_CDS('MSFT', delta_year)
f = figure(x_axis_type="datetime")
f.line('date', 'price', source=source, line_width=2)

curdoc().add_root(f)
