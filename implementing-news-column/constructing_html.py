from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div
from bokeh.layouts import layout, row, column
from bokeh.models import CustomJS, Div, Button

from bokeh.io import curdoc
from bokeh import events

#importing Bokeh
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.resources import CDN

lst=['a','b','c','d']

def display_event(div, lst=[]):
    return CustomJS(args=dict(div=div), code="""
        var list = %s
        for (var i=0; i<list.length; i++){
            var temp = "<p>" + list[i] + "</p>"
            div.text = div.text.concat(temp)
            console.log(list[i])
        }
        var line = "<h4>word</h4>"
        div.text = div.text.concat(line)
        console.log(0)
    """ % (lst))

#prepare some data
x=[1,2,3,4,5]
y=[6,7,8,9,10]

#prepare the output file
#create a figure object
f=figure()
f.add_tools

#create line plot
f.line(x,y)

div = Div(text="""
<h1> Hello </h1>
<h2> Good </h2>
<h3> Bye </h3>
""", width=200, height=100)
f.js_on_event(events.Tap, display_event(div, lst))
#div._property_values['position']='aboslute'
#div._property_values['left'] = 500
#print(div._property_values['position'] = absolute)
print(div.css_classes)

#overflow:auto;
#position: absolute;
#left: 500px;

layout = column(row(f, div))
curdoc().add_root(layout)
