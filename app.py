# Imports
import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

# Create evironment variables
load_dotenv()

# Function to create Flask app (called by Flask automatically)
def create_app():

    # Create Flask app
    app = Flask(__name__)
    
    # Create client for MongoDB and get URI
    client = MongoClient(os.getenv("MONGODB_URI"))

    # Select database for app
    app.db = client.MCB

    # Create route (or endpoint)
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":

            # Get posted message form user
            entry_content = request.form.get("content")

            # Get current date
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

            # Insert data in database
            app.db.entries.insert_one( {"content": entry_content, "date": formatted_date} )
        
        # Select data to send to HTML (list comprehension)
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in app.db.entries.find({})
        ]

        # Render html-template with entries_with_date
        return render_template("home.html", entries=entries_with_date)

    # For Flask, we need to return the app
    return app

