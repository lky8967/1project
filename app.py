<<<<<<< HEAD

=======
>>>>>>> 9ba8e79f059cd87345aa46da9fd3bd9d120dcb6b
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
<<<<<<< HEAD
import mongopy

ca = certifi.where()
=======
ca = certifi.where()
import mongopy
>>>>>>> 9ba8e79f059cd87345aa46da9fd3bd9d120dcb6b

client = MongoClient(mongopy.password, tlsCAFile=ca)
db = client.dbsparta


<<<<<<< HEAD




@app.route('/')
def home():
    return render_template('main.html')


=======
@app.route('/')
def created():
    return render_template('created.html')

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
>>>>>>> 9ba8e79f059cd87345aa46da9fd3bd9d120dcb6b




if __name__ == '__main__':
<<<<<<< HEAD
    app.run('0.0.0.0', port=5000, debug=True)

=======
    app.run('0.0.0.0', port=5000, debug=True)
>>>>>>> 9ba8e79f059cd87345aa46da9fd3bd9d120dcb6b
