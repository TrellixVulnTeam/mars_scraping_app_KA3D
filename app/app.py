from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://heroku_81hbmzd3:d0iriero1tpa7uv2bc159sgp06@ds145146.mlab.com:45146/heroku_81hbmzd3"
mongo = PyMongo(app)


@app.route("/")
def index():
    all_data = mongo.db.all_data.find_one()
    return render_template("index.html", all_data=all_data)


@app.route("/scrape")
def scraper():
    all_data = mongo.db.all_data
    all_data_data = scrape_mars.scrape()
    all_data.update({}, all_data_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
