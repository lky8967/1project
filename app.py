
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
import mongopy

ca = certifi.where()

client = MongoClient(mongopy.password, tlsCAFile=ca)
db = client.dbsparta






@app.route('/')
def home():
    return render_template('main.html')






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

