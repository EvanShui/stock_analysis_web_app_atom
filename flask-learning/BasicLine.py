#Making a basic Bokeh line graph

#importing Bokeh
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool, Div, Button
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool, Div, Button
from bokeh.models.widgets import Button, Panel, Tabs, TextInput, Paragraph, CheckboxButtonGroup
from bokeh.layouts import layout, row, column, widgetbox
from bokeh.resources import INLINE
from bokeh.events import ButtonClick
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import json

x=[1,2,3,4,5]
y=[6,7,8,9,10]

source = ColumnDataSource(data=dict(x=x,y=y))

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

text_input = TextInput()
button = Button(label="main")
button2 = Button()
output=Paragraph()
output.text = "goodbye"

y2=[10,9,8,7,6]

def web_scraper(x_coord):
    opener = urllib.request.build_opener()
    #url for search query
    url = "https://www.google.com/search?source=hp&q=" + str(x_coord)
    return url

def button_click():
    output.text += "hello"

button_callback = CustomJS(args=dict(text_input=text_input, output=output, source=source),code="""
     var plot_data = source.data;
     var ticker = text_input.value;
     jQuery.ajax({
        type: 'POST',
        url: '/update_y_data',
        data: {"ticker_sent": ticker},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
            output.text += ticker
            plot_data['y'] = json_from_server[ticker];
            source.trigger('change');
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """)

tap_callback = CustomJS(args=dict(output=output), code="""
    var x_coordinate = cb_obj['x']
    console.log("hello")
    jQuery.ajax({
        type: 'POST',
        url: '/get_data',
        data: {"x_coord": x_coordinate},
        dataType: 'json',
        success: function (json_from_server) {
            //assigns the list that was sent from the flask route /get_new_data
            var url = json_from_server[x_coordinate]
            //iterates through the list and adds each element (the search query title)
            //to div
            console.log("loading")
            output.text += url
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """)

button.js_on_event(ButtonClick, CustomJS(code="console.log('hello')"))
button2.js_on_event(ButtonClick, button_callback)
#prepare some data


#create a figure object
f=figure()

#create line plot
f.line('x','y',source=source)
f.js_on_event('tap', tap_callback)

lay_out = column(row(column(text_input,output), column(button,button2)), f)

js,div=components(lay_out, INLINE)

cdn_js=INLINE.render_js()
cdn_css=INLINE.render_css()


#write the plot in the figure object
#show(f)
