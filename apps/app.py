# Import flask and render template, use PyMongo to interact with Mongo db, use scraping code
import pymongo
import scraping
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define route for the html page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# Run flask app
if __name__ == "__main__":
   app.run()