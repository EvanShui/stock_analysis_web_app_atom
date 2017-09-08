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

app = Flask(__name__)

N_DATAPOINTS = 20
DEFAULT_VARIABLE = 'bar'
MY_DATABASE = {
    'foo': [i**1 for i in range(N_DATAPOINTS)],
    'bar': [i**2 for i in range(N_DATAPOINTS)],
    'baz': [i**3 for i in range(N_DATAPOINTS)]}

def web_scraper(arg):
    lst = []
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = "https://www.google.com/search?source=hp&q=" + str(int(arg))
    print(url)
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    for x in soup.findAll(class_="r"):
        lst.append(x.a.contents[0].encode("utf-8"))
    return lst

@app.route("/get_new_data", methods=['POST'])
def get_new_data():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    app.logger.info(
        "Variable to return %r", variable_to_return)
    app.logger.info(
        "data %r", MY_DATABASE[variable_to_return]
    )
    return jsonify({variable_to_return: MY_DATABASE[variable_to_return]})

@app.route("/get_coord",methods=['POST'])
def get_coord():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    variable_to_return = float(request.form['x_coord'])
    list_to_return = web_scraper(variable_to_return)
    app.logger.info(
        "x_coord %r", (variable_to_return))
    app.logger.info(
        "list %r",(list_to_return))
    return jsonify({variable_to_return: list_to_return})

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


@app.route("/")
def simple():
    x = range(N_DATAPOINTS)
    y = MY_DATABASE[DEFAULT_VARIABLE]

    source = ColumnDataSource(data=dict(x=x, y=y))
    div = Div(text="""
    <h1> Hello </h1>
    <h2> Good </h2>
    <h3> Bye </h3>
    """, width=200, height=100)

    plot = figure(title="Flask + JQuery AJAX in Bokeh CustomJS")
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
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
            list = json_from_server[x_coordinate]
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
    plot.js_on_event('tap', tap_callback)
    select = Select(title="Select variable to visualize",
                    value=DEFAULT_VARIABLE,
                    options=list(MY_DATABASE.keys()),
                    callback=callback)

    layout = column(select, row(plot, div))
    script, div = components(layout)
    html = SIMPLE_HTML_TEMPLATE.render(
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css())
    return encode_utf8(html)

app.run(debug=True, host="127.0.0.1", port=5002)
