import json

from flask import Flask, jsonify, request
from jinja2 import Template
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, Select
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.layouts import column
from bokeh.util.string import encode_utf8
from bokeh import events
import math

app = Flask(__name__)

N_DATAPOINTS = 20
DEFAULT_VARIABLE = 'bar'
MY_DATABASE = {
    'foo': [i**1 for i in range(N_DATAPOINTS)],
    'bar': [i**2 for i in range(N_DATAPOINTS)],
    'baz': [i**3 for i in range(N_DATAPOINTS)]}


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
    app.logger.info(
        "x_coord %r", (variable_to_return))
    return jsonify({variable_to_return: (variable_to_return) + 5})

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

    plot = figure(title="Flask + JQuery AJAX in Bokeh CustomJS")
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    tap_callback = CustomJS(code="""
    var x_coordinate = cb_obj['x']
    jQuery.ajax({
        type: 'POST',
        url: '/get_coord',
        data: {"x_coord": x_coordinate},
        dataType: 'json',
        success: function (json_from_server) {
            alert(JSON.stringify(json_from_server));
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

    layout = column(select, plot)
    script, div = components(layout)
    html = SIMPLE_HTML_TEMPLATE.render(
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css())

    return encode_utf8(html)

app.run(debug=True, host="127.0.0.1", port=5002)
