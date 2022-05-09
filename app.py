
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi


ca = certifi.where()
import mongopy


client = MongoClient(mongopy.password, tlsCAFile=ca)
db = client.dbsparta





@app.route('/')
def home():
    return render_template('main.html')


@app.route("/freezer_created", methods=["POST"])
def freezer_created():
    name_receive = request.form['name_give']
    freezer_list = list(db.freezer.find({}, {'_id': False}))
    count = len(freezer_list) + 1

    doc = {
        'name':name_receive,
        'num':count
    }

    db.freezer.insert_one(doc)
    return jsonify({'msg':'저장완료 !'})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
