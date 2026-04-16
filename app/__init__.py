# -*- coding: utf-8 -*-

"""
*******************************************************************************
* Copyright (c) 2026 Company Name. All rights reserved.
*
* File: __init__.py
* Author: Odeleye Oluwafemi Joseph
* Created: 2026-03-27
* Version: 0.1.0
*
* Description:
#
*     This module implements an API for the frontend to be able read and write
#     link code both to store a destructive url for 10 mins. 
*     There's also a plan to shorten the url
# 
* Features:
*     - Code to generate after url is inputted
*     - Shorten url generated a
*
* License: MIT License (see LICENSE file for details)
*******************************************************************************
"""

# py -3 -m venv .venv && source .venv/Scripts/activate && python -m pip install --upgrade pip flask flask-sqlalchemy

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
import datetime
import logging


# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'djxnsbehejv8s9d8f7s6d5f4g3h2j1k0l9m8n7o6p5q4r3t2u1v0w9x8y7z6a5b4c3d2e1f0g9h8i7j6k5l4m3n2o1p0q9r8s7t6u5v4w3x2y1z0'

logging.basicConfig(level=logging.INFO)


# Initialize the database
db = SQLAlchemy(app)

# create a model for the url
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    shortened_url = db.Column(db.String(2048), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<URL {self.original_url} -> {self.shortened_url}>'

# Create the database tables if they don't exist
if not os.path.exists('instance/links.db'):   
    with app.app_context():
            db.create_all()
            db.session.commit() # Commit the changes
            print("Database tables created!")

# Define the API endpoints
@app.route('/')
def index():
        # return frontend template
        app.logger.info("Received request for the homepage.")
        return render_template('index.html')
        # return jsonify({'message': 'Welcome to the URL Shortener API!'})

# Endpoint to generate a code for a given URL and store it in the database
@app.route('/api/generate-code', methods=['POST','GET'])
def urtl():
    if request.method == 'POST':
        # retrieve the url from the request
        url = request.json.get('url')
        # gennerate a code for the url after inserting it into the database
        generated_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        new_url = URL(original_url=url, shortened_url=url, code=generated_code)
        db.session.add(new_url)
        db.session.commit()

        now = datetime.datetime.utcnow()
        app.logger.info(f"Generated code {generated_code} for URL: {url} at {now}")    
        # logic to return the url
        return jsonify({'message': 'URL returned successfully!', 'url': url, 'code': generated_code, 'created_at': now}), 200
    
    else:
        return jsonify({'message': 'Please send a POST request with the URL to shorten.'})
    
# Endpoint to retrieve the original URL using the code and check for expiration
@app.route('/api/retrieve/<code>', methods=['GET'])
def retrieve_url(code):
    url_entry = URL.query.filter_by(code=code).first()

    if url_entry:
        expiry_time = url_entry.created_at + datetime.timedelta(minutes=10)
        
        if (datetime.datetime.utcnow() - expiry_time).total_seconds() > 0:  # Check if expired (10 minutes)
            db.session.delete(url_entry)
            db.session.commit()
            app.logger.info(f"URL with code {code} has expired and was deleted.")
            return jsonify({'message': 'URL has expired and has been deleted.'}), 410
        return jsonify({'original_url': url_entry.original_url, 'expires_in': expiry_time}), 200  
    # Expires in 10 minutes (600 seconds)
    else:
        app.logger.info(f"URL with code {code} not found.")
        return jsonify({'message': 'URL not found for the provided code.'}), 404
    
    
# check for expired urls and delete them every minute
@app.before_request
def delete_expired_urls():
    now = datetime.datetime.utcnow()
    expired_urls = URL.query.filter(URL.created_at < (now - datetime.timedelta(minutes=10))).all()
    app.logger.info(f"Checking for expired URLs at {now}. Found {len(expired_urls)} expired URLs.")
    for url in expired_urls:
        db.session.delete(url)
        app.logger.info(f"Deleted expired URL: {url.original_url} with code: {url.code}")
    
    db.session.commit()
    app.logger.info("Expired URLs deletion completed.")



  

if __name__ == "__main__":
     app.logger.info("Starting the Flask application...")
     app.run(debug=False)


