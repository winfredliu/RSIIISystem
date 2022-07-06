# serverAPI --> API Server
from utils.database import *
from flask import request
from flask import Flask, jsonify, json

# 日志打印格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[%(funcName)s-->'
                           'line:%(lineno)d] - %(levelname)s: %(message)s')

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(process)d-%(threadName)s - '
#                            '%(pathname)s-%(filename)s[%(funcName)s-->'
#                            'line:%(lineno)d] - %(levelname)s: %(message)s')

# app设置
app = Flask(__name__)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/')
def index():
    return "Welcome to RSIIISystem's API Server!"


@app.route('/api/client/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    infoList = findUserByPhoneAndPwd(data['phone'], data['password'])
    if len(infoList) == 0:
        return jsonify({'status': 0, "code": 1000, 'message': '账号或密码错误'})
    else:
        uid = infoList[0][0]
        username = infoList[0][1]
        phone = infoList[0][2]
        email = infoList[0][3]
        token = '12345'
        return jsonify({'status': 200, 'code': 0, 'message': '登录成功',
                        'data': {'id': uid, 'username': username, 'phone': phone, 'email': email, 'token': token}})


@app.route('/api/client/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    username = data['username']
    phone = data['phone']
    email = data['email']
    password = data['password']
    if len(findUserByPhone(phone)) > 0:
        return jsonify({'status': 200, 'code': 1000, 'message': '手机号已被他人注册!'})
    if addUser(username, phone, email, password) == 1:
        return jsonify({'status': 200, 'code': 0, 'message': '注册成功'})
    else:
        return jsonify({'status': 200, 'code': 1000, 'message': '注册失败'})


@app.route('/api/client/updatePwd', methods=['POST'])
def updatePwd():
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    phone = data['phone']
    newPwd = data['password']
    if updatePassword(phone, newPwd) == 1:
        return jsonify({'status': 200, 'code': 0, 'message': '密码重置成功'})
    else:
        return jsonify({'status': 200, 'code': 1000, 'message': '该账号不存在'})


@app.route('/api/client/update', methods=['POST'])
def update():
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    uid = data['uid']
    username = data['username']
    phone = data['phone']
    email = data['email']
    oldPwd = data['oldPwd']
    newPwd = data['newPwd']
    if updateUser(uid, username, phone, email, oldPwd, newPwd) == 1:
        return jsonify({'status': 200, 'code': 0, 'message': '修改成功'})
    else:
        return jsonify({'status': 200, 'code': 1000, 'message': '原密码有误'})


if __name__ == "__main__":
    app.run(debug=False, threaded=True, host='localhost', port=5000)
