from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping 

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

mars_db = mongo.db.mars

app.route('/')
def index():
    data_from_db = mars_db.find_one()
    return render_template('index.html', mars = data_from_db)

@app.route("/scrape")
def scrape():
    scraped_data = scraping.scrape()
    mars_db.update({}, scraped_data, upsert=True)
    return redirect('/')

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)


