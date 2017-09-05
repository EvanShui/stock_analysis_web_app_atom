#flask app
from flask import Flask, render_template
from datetime import datetime
from BasicLine import js,div, cdn_js, cdn_css
from bokeh.embed import autoload_server
from bokeh.client import pull_session

#instantiate the flask append
app = Flask(__name__)

#create index page function
@app.route("/")
def index():
    session=pull_session(app_path="http://localhost:5006/random_generator")
    bokeh_script=autoload_server(None,app_path="http://localhost:5006/random_generator",session_id=session.id)
    return render_template("index.html", js=js, div=div, cdn_js=cdn_js, cdn_css=cdn_css, current_date=datetime.now())

#run the app
if __name__ == "__main__":
    app.run(debug=True) #set debug false when making web app live
