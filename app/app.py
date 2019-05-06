# from flask import Flask, render_template, redirect

# from flask_pymongo import PyMongo
# import scrape_mars

# app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
# mongo = PyMongo(app)


# @app.route('/')
# def home():
   
#     all_data = mongo.db.mars_data_from_scrape.find_one()
#     return render_template("index.html", all_data=all_data)

   

# @app.route("/scrape")
# def scraper():
#     all_data = mongo.db.all_data
#     scrape_mars_data = scrape_mars.scrape()  
#     all_data.update({}, scrape_mars_data, upsert=True)

#     return redirect('/', code=302)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
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
