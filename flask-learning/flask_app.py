#flask app
from flask import Flask, render_template
from datetime import datetime
from BasicLine import js, div, cdn_js, cdn_css
from BasicLine import web_scraper
from flask import Flask, render_template, jsonify, request, url_for
import json

#instantiate the flask append
app = Flask(__name__)

@app.route("/update_y_data", methods=['POST'])
def get_y_data():
    app.logger.info(
        "Browser sent the following via AJAX: %s", json.dumps(request.form))
    ticker = request.form['ticker_sent']
    app.logger.info(
        "ticker %r", (ticker))
    return jsonify({ticker:[10, 9, 8, 7, 6]})

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
