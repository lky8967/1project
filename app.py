from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.dhiik.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta




@app.route('/')
def home():
    return render_template('main.html')





