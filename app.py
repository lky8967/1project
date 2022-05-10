from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import datetime

from werkzeug.utils import secure_filename

from datetime import datetime, timedelta

UPLOAD_FOLDER ='./save_image/' #저장경로 '현재 앱 경로/저장할 경로'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

#IMAGE_PATH = #'------s/' #사진 저장된 경로

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024

from pymongo import MongoClient
client = MongoClient('mongodb+srv://tset:sparta@cluster0.a1jkl.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


## API 역할을 하는 부분
@app.route('/owtest/save', methods=['POST'])
def foodsaving():
    id = make_id()
##음식 정보
    name_receive = request.form['name_give']
    group_receive = request.form['group_give']
    date_receive = request.form['date_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

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

#
  #  i = 1
 #   for image in images:
  #      imagename = str(id) + "_" + str(i) + '.jpg'
  #      imagename = secure_filename(imagename)  # 이름 검사
 #       image.save(save_to, imagename)  # 저장
  #      i += 1

        # extension = image.filename.rsplit('.', 1)[1].lower() # 확장자 추출
        # for compare_extension in ALLOWED_EXTENSIONS:
        #     if ( compare_extension == extension): # 허용되는 확장자 검사
        #         imagename = str(id) + "_" + str(i) + extension
        #         imagename = secure_filename(imagename) # 이름 검사
        #         image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename)) # 저장
        #         i += 1

    food_list = list(db.owtest.find({}, {'_id': False}))
    count = len(food_list) + 1

##음식정보 입력
    doc = {
        'id': id,
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

#등록한 음식 ID 생성
def make_id():
    t = datetime.now()

    #년, 월, 일, 시, 분, 초, 밀리초(앞2자리) 순서대로
    id = str(t.year)[2:4] +\
         t.strftime("%m") +\
         t.strftime("%d") +\
         t.strftime("%H") +\
         t.strftime("%M") +\
         t.strftime("%M") +\
         t.strftime("%S")


    return int(id) #정수로 변환
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)