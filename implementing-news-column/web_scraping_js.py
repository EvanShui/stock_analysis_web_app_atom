from bokeh.plotting import figure
from bokeh.io import output_file, show, curdoc
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh import events
from bokeh.layouts import column, row
from bokeh.models.callbacks import CustomJS
import sys
import time
import threading
#prepare some data
x=[1,2,3,4,5]
y=[6,7,8,9,10]
#create a figure object
f=figure()
f.add_tools

#create line plot
f.line(x,y)
point_attributes = ['x', 'y']

source = ColumnDataSource(data=dict(x=[100],y=[100]))

def js_event_callback(event):
    print("one", event)
    #print(event.x)
    return CustomJS(args=dict(source=source),code="""
        var article_list = []
        x = cb_obj['x']
        y = cb_obj['y']
        console.log(source['data']['x'][0])
        console.log(source['data']['y'][0])
        source['data']['x'][0] = x;
        source['data']['y'][0] = y;
        source.trigger('change');
        console.log(source['data']['x'][0])
        console.log(source['data']['y'][0])
        source.change.emit()
    """)

def python_event_callback(event):
    print(source.data['x'][0])
    print(source.data['y'][0])

f.js_on_event(events.Tap, js_event_callback(event=events.Tap))
f.on_event(events.Tap, python_event_callback)

layout = column(f)

curdoc().add_root(layout)
