import numpy as np
import cryptpandas as crp
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import requests

from flask import Flask, jsonify
import os

pos_dict = {'strat_1': 0.1}
app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/get_latest_data', methods=['GET'])
def get_latest_data():
    # Add CORS headers to allow requests from any origin
    response = jsonify(str(pos_dict))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# def post_to_google_form(pos_dict):
#     FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUYMkI5ce18RL2aF5C8I7mPxF7haH23VEVz7PQrvz0Do0NrQ/formResponse"
    
#     # Prepare form data
#     form_data = {
#         "emailAddress": "dswdavid1@gmail.com",
#         "entry.1985358237": str(pos_dict)
#     }
    
#     try:
#         response = requests.post(FORM_URL, data=form_data)
#         if response.status_code == 200:
#             print("Form submitted successfully!")
#         else:
#             print(f"Failed to submit form. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error submitting form: {str(e)}")