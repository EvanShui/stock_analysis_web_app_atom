#flask app
from flask import Flask, render_template
from datetime import datetime
import BasicLine
from BasicLine import js, div, cdn_js, cdn_css, dates, stock_ticker
from BasicLine import web_scraper, data_to_CDS_y, get_data
from flask import Flask, render_template, jsonify, request, url_for
import json

#instantiate the flask append
app = Flask(__name__)

@app.route("/resize_y_range", methods=['POST'])
def resize_y_range():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    date_index = request.form['index']
    app.logger.info(
        "Resize basicline ticker: %s", BasicLine.stock_ticker)
    return jsonify({date_index:[5,4,3,2,1]})

@app.route("/update_y_data", methods=['POST'])
def get_y_data():
    global stock_ticker
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    ticker = request.form['ticker_sent']
    test_ticker = "atvi"
    app.logger.info(
        "Original basicline ticker: %s", BasicLine.stock_ticker)
    BasicLine.stock_ticker = test_ticker
    app.logger.info(
        "New basicline ticker: %s", BasicLine.stock_ticker)
    data, meta_data = get_data(test_ticker)
    sources_y_list = data_to_CDS_y(data, dates[5])
    #app.logger.info(
    #    "ticker %r", (sources_y_list))
    #app.logger.info(
    #    "sources_list %r", (sources_list))
    return jsonify({ticker:(sources_y_list[0], sources_y_list[1])})

@app.route("/get_data",methods=['POST'])
def get_coord():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    #the data retrieved is in the form of a string, turn it into float to perform arithmetic operations
    x_coordinate = float(request.form['x_coord'])
    #creates the list of data given the x-coordinate of the mouse and assigns the resulting list
    web_url = web_scraper(x_coordinate)
    app.logger.info(
        "x_coord %r", (x_coordinate))
    #returns a list in form of json
    return jsonify({x_coordinate: web_url})

#create index page function
@app.route("/")
def index():
    return render_template("index.html", js=js, div=div, cdn_js=cdn_js, cdn_css=cdn_css)

#run the app
if __name__ == "__main__":
    app.run(debug=True) #set debug false when making web app live
