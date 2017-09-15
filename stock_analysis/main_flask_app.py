#flask app
from flask import Flask, render_template
from datetime import datetime
from bokeh.embed import autoload_server
from bokeh.client import pull_session

#instantiate the flask append
app = Flask(__name__)

#main app route
@app.route("/")
#essentially the main function of this program to create bokeh diagrams
def index():
    script = autoload_server("https://demo.bokehplots.com/apps/slider")
    print(script)
    return render_template('index.html',bokeh_script=script)


#run the app
if __name__ == "__main__":
    app.run(debug=True)
