from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
import hashlib
import mongopy
from datetime import datetime, timedelta

import certifi
ca = certifi.where()

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

from werkzeug.utils import secure_filename

UPLOAD_FOLDER ='./save_image/' #저장경로 '현재 앱 경로/저장할 경로'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

#IMAGE_PATH = #'------s/' #사진 저장된 경로

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024

from pymongo import MongoClient
client = MongoClient(mongopy.password, tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         # 'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
         'exp': datetime.utcnow() + timedelta(seconds=60)  # 테스트용 60초
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,   # 아이디
        "password": password_hash,      # 비밀번호
        "nickname": username_receive,   # 닉네임
        "profile_pic": "",              # 프로필 사진 파일 이름
        "profile_pic_real": "static/profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_nickname_dup', methods=['POST'])
def check_nickname_dup():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})




## API 역할을 하는 부분
@app.route('/owtest/save', methods=['POST'])
def foodsaving():
    token_receive = request.cookies.get('mytoken')

    try:
    ##유저 정보 확인
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
    ##음식 정보
        name_receive = request.form['name_give']
        group_receive = request.form['group_give']
        date_receive = request.form['date_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']


        foodid = make_id()

    ##이미지 받기

        file = request.files["file_give"]

        extension = file.filename.split('.')[-1]

    ##등록시간
        today = datetime.now()
        mytime1 = today.strftime('%Y-%m-%d %H:%M')  # 작성시각
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  # 파일업로드시각
        filename = f'file-{mytime}' #파일이름지정

    ##이미지 저장
        save_to = f'static/{filename}.{extension}'
        file.save(save_to)



        food_list = list(db.owtest.find({}, {'_id': False}))
        count = len(food_list) + 1

    ##음식정보 입력
        doc = {
            "username": user_info["username"], ##유저 id입력
            #"profile_name": user_info["nickname"], ##유저 닉네임입력
            'foodid': foodid,
            'name': name_receive,
            'num': count,
            'group': group_receive,
            'date':date_receive,
            'star':star_receive,
            'comment':comment_receive,
            'mytime1': f'{mytime1}',
            'file': f'{filename}.{extension}'
        }

        db.owtest.insert_one(doc)

        return jsonify({'msg':'저장이 완료되었습니다!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

#등록한 음식 ID 생성
def make_id():
    t = datetime.now()

    #년, 월, 일, 시, 분, 초, 밀리초(앞2자리) 순서대로
    foodid = str(t.year)[2:4] +\
         t.strftime("%m") +\
         t.strftime("%d") +\
         t.strftime("%H") +\
         t.strftime("%M") +\
         t.strftime("%M") +\
         t.strftime("%S")

    return int(foodid) #정수로 변환


@app.route("/fridge", methods=["POST"])
def fridge_post():
    name_receive = request.form['name_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'star': star_receive,
        'comment': comment_receive
    }
    db.fridge.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/fridge", methods=["GET"])
def fridge_get():
    item_list = list(db.fridge.find({}, {'_id': False}))
    return jsonify({'fridge':item_list})







if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
