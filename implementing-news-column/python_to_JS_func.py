from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh import events
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import numpy as np

output_file("callback.html")

x = [x*0.005 for x in range(0, 200)]
y = x
url = ["https://www.google.com/search?source=hp&q="]

url_results = ColumnDataSource(data=dict(url=(url), articles=['a']))

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

def callback(source=source, window=None):
    data = source.data
    f = cb_obj.value
    x, y = data['x'], data['y']
    for i in range(len(x)):
        y[i] = window.Math.pow(x[i], f)
    source.change.emit()

def convert(url):
    opener = urllib.request.build_opener()
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    return 1

def callback_coord(source=url_results, window=None):
    mouse = cb_obj
    data = source.data
    print(data['url'][0])
    print(mouse['x'])
    print(mouse['y'])
    print(convert("https://www.google.com/search?source=hp&q="))

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power",
                callback=CustomJS.from_py_func(callback))

plot.js_on_event(events.Tap, CustomJS.from_py_func(callback_coord))

layout = column(slider, plot)

curdoc().add_root(layout)
