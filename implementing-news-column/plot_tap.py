#Making a basic Bokeh line graph

#importing Bokeh
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

class ListStream:
    def __init__(self):
        self.data = []
    def write(self, s):
        self.data.append(s)

counter = 0
print_lst= [0,0]
print("global", id(print_lst))

def event_callback(event):
    print("pyton",event)
    print(event.x)
    print(event.y)
    global counter
    counter += 1
    print("local",id(print_lst))
    print_lst.append((event.x,event.y))
    print(id(print_lst))
    for i in print_lst:
        print(i)

def js_event_callback(event, lst=[]):
    print("js", event)
    #print(event.x)
    return CustomJS(code="""
        var list = %s
        var x = list[0]
        var y = list[1]
        console.log(x)
        console.log(y)
    """ % (lst))

#prepare some data
x=[1,2,3,4,5]
y=[6,7,8,9,10]

#prepare the output file
output_file("Line.html")

#create a figure object
f=figure()
f.add_tools

#create line plot
f.line(x,y)
point_attributes = ['x', 'y']


f.js_on_event(events.Tap, js_event_callback(event=events.Tap, lst=print_lst))
f.on_event(events.Tap, event_callback)

layout = column(f)

curdoc().add_root(layout)
