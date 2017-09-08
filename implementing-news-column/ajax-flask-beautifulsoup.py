#importing libraries
import json
from bokeh.models import CustomJS, Div, Button
from flask import Flask, jsonify, request
from jinja2 import Template
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, Select
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.layouts import column, row
from bokeh.util.string import encode_utf8
from bokeh import events
import math
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request

#creating the flaks app
app = Flask(__name__)


#generating data for bokeh plot
N_DATAPOINTS = 20
#the y-value points will correspond to the values associated with the 'bar' key
DEFAULT_VARIABLE = 'bar'
#dictionary for the y-coordinate values for bokeh plot
MY_DATABASE = {
    'foo': [i**1 for i in range(N_DATAPOINTS)],
    'bar': [i**2 for i in range(N_DATAPOINTS)],
    'baz': [i**3 for i in range(N_DATAPOINTS)]}

# str -> lst
# Hard coded to specifically scrape the google website and returns a list of
# the website titles from the google search results given a string to initate
# the search query
def web_scraper(arg):
    lst = []
    opener = urllib.request.build_opener()
    #use Mozilla because can't access chrome due to insufficient privileges
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    #url for search query
    url = "https://www.google.com/search?source=hp&q=" + str(int(arg))
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    #use beauitful soup to find all divs with the r class, which essentially
    #is the same as finding all of the divs that contain each individiaul search
    #result
    for x in soup.findAll(class_="r"):
    #appends the title of each individual search result to a list
        lst.append(x.a.contents[0].encode("utf-8"))
    return lst

#generating URL for flask planning on using ajax.post method to retrieve and send back data
@app.route("/get_new_data", methods=['POST'])
#creating function associated to url generated
def get_new_data():
    #reporting incoming data for debugging purposes
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    #assigning incoming data from javascript via request call (either foo bar or baz)
    variable_to_return = request.form['please_return_data_of_this_variable']
    #more reporting data for debugging purposes
    app.logger.info(
        "Variable to return %r", variable_to_return)
    app.logger.info(
        "data %r", MY_DATABASE[variable_to_return])
    #retrieves a list of data given the key that was retrieved and assigned to variable_to_return
    return jsonify({variable_to_return: MY_DATABASE[variable_to_return]})

#generating another URL for flask, this time to search the x-coordinate of
#the mouse and send back the results
@app.route("/get_coord",methods=['POST'])
def get_coord():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    #the data retrieved is in the form of a string, turn it into float to perform arithmetic operations
    variable_to_return = float(request.form['x_coord'])
    #creates the list of data given the x-coordinate of the mouse and assigns the resulting list
    list_to_return = web_scraper(variable_to_return)
    app.logger.info(
        "x_coord %r", (variable_to_return))
    app.logger.info(
        "list %r",(list_to_return))
    #returns a list in form of json
    return jsonify({variable_to_return: list_to_return})

#HTML template to build the flask app
SIMPLE_HTML_TEMPLATE = Template('''
<!DOCTYPE html>
<html>
    <head>
        <script src="https://code.jquery.com/jquery-3.1.0.min.js"></script>
        {{ js_resources }}
        {{ css_resources }}
    </head>
    <body>
    {{ plot_div }}
    {{ plot_script }}
    </body>
</html>
''')

#main app route
@app.route("/")
#essentially the main function of this program to create bokeh diagrams
def simple():
    x = range(N_DATAPOINTS)
    y = MY_DATABASE[DEFAULT_VARIABLE]

    source = ColumnDataSource(data=dict(x=x, y=y))

    #the div object that will be injected into the main html template, the
    #titles of the search results will be added here
    div = Div(text="""
    <h1> Hello </h1>
    <h2> Good </h2>
    <h3> Bye </h3>
    """, width=200, height=100)

    #creating the figure object
    plot = figure(title="Flask + JQuery AJAX in Bokeh CustomJS")
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    #callback to be executed once mouse clicks on bokeh plot
    #passing the div object into CustomJS for manipulation
    tap_callback = CustomJS(args=dict(div=div),code="""
    var x_coordinate = cb_obj['x']
    jQuery.ajax({
        type: 'POST',
        url: '/get_coord',
        data: {"x_coord": x_coordinate},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
            console.log(json_from_server[x_coordinate][0])
            //assigns the list that was sent from the flask route /get_new_data
            list = json_from_server[x_coordinate]
            //iterates through the list and adds each element (the search query title)
            //to div
            for(var i =0; i < list.length; i++){
                var line = "<p>" + list[i] + "</p>\\n"
                var text = div.text.concat(line)
                var lines = text.split("\\n")
                div.text = lines.join("\\n")
            }

        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });
    """)

    #callback for the selection widget
    callback = CustomJS(args=dict(source=source), code="""
    var selected_value = cb_obj.value;
    var plot_data = source.data;

    jQuery.ajax({
        type: 'POST',
        url: '/get_new_data',
        data: {"please_return_data_of_this_variable": selected_value},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
            plot_data['y'] = json_from_server[selected_value];
            source.trigger('change');
        },
        error: function() {
            alert("Oh no, something went wrong. Search for an error " +
                  "message in Flask log and browser developer tools.");
        }
    });

    """)
    #event call for mouse clicks
    plot.js_on_event('tap', tap_callback)

    #select widget
    select = Select(title="Select variable to visualize",
                    value=DEFAULT_VARIABLE,
                    options=list(MY_DATABASE.keys()),
                    callback=callback)

    #constructing the html / css / js components of the bokeh graph
    layout = column(select, row(plot, div))
    script, div = components(layout)
    html = SIMPLE_HTML_TEMPLATE.render(
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css())
    #returns the rendered html template with the bokeh graph
    return encode_utf8(html)
    
#runs on local server @ port 5002
app.run(debug=True, host="127.0.0.1", port=5002)
