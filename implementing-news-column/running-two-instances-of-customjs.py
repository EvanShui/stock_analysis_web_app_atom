from bokeh.plotting import figure
from bokeh.io import output_file, show, curdoc
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
def js_event_callback(event):
    print("one", event)
    #print(event.x)
    return CustomJS(code="""
        console.log(0)
        console.log(1)
    """)


def js_event_callback_2(event):
    print("two", event)
    return CustomJS(code="""
        console.log(2)
        console.log(3)
    """)

f.js_on_event(events.Tap, js_event_callback(event=events.Tap))
f.js_on_event(events.Tap, js_event_callback_2(event=events.Tap))

layout = column(f)

curdoc().add_root(layout)
