## web app to display Mars info
# to run, in terminal: python app.py
# if port is occuppied, in terminal: lsof -i tcp:5000, then: kill -9 <programID>

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up the app
app = Flask(__name__)

# set up a mongo connection - connect using a uniform resource identifier
# app reaches mongo thru the localhost server using port 27017 and db named "mars_app"
# https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
mongo = PyMongo(app)


# define the home route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one() # use PyMongo to find the "Mars" collection in the database
    return render_template("index.html", mars=mars) # return the HTML template in index.html file, use the "mars" collection in MongoDB


# scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars # new variable to hold the database
    mars_data = scraping.scrape_all() # scrape new data using scraping.py
    mars.update_one({}, {"$set":mars_data}, upsert=True) # update the first matching document in the db with newly scraped data, 
        # or insert new data if doesn't already exist
    return redirect('/', code=302) # navigate back to home to see updated content


# run the app
if __name__ == "__main__":
   app.run(debug=True)
