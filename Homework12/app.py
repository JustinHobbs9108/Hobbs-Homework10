from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()

    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_data2 = scrape_mars.scrape_mars_news()
    mars_data2 = scrape_mars.scrape_mars_img()
    mars_data2 = scrape_mars.scrape_mars_facts()
    mars_data2 = scrape_mars.scrape_mars_weather()
    mars_data2 = scrape_mars.scrape_mars_hemispheres()
    mars_data.update({}, mars_data2, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)