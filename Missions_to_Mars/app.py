from scrape_mars import scrape
from flask import Flask, render_template, flash, redirect
import pymongo, os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def home():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    collection = client.mars.mars_data

    data = collection.find_one()
    client.close()

    if data is None:
        return redirect("/scrape")

    return render_template("index.html", data=data)

@app.route("/scrape")
def scrape_page():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    db = client.mars
    db.mars_data.drop()

    db.mars_data.insert_one(scrape())

    client.close()
    flash("All data has been successfully scraped!!")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)