from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os
import psycopg2

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = os.environ['MONGODB_URI']
mongo = PyMongo(app)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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
