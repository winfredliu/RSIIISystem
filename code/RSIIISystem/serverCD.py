# serverCD --> ChangeDetection Server
import time
import logging
import paddlers as pdrs
from utils import model
from flask_cors import *
from utils.aUtils import *
from flask import send_from_directory
from flask import Flask, jsonify, json
from flask import request, make_response
from werkzeug.utils import secure_filename

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
CORS(app, supports_credentials=True, resources=r"/*")
# 全局变量
cdModel = pdrs.deploy.Predictor('./model/exportedModel/changeDetection')
progressNum = {}
TMPDIR_FOLDER = 'tmpDir'
app.config['TMPDIR_FOLDER'] = TMPDIR_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))


# 模型预热
# cdModel.predict(img_file=('./model/warmData/changeDetection/A.png',
#                           './model/warmData/changeDetection/B.png'),
#                 warmup_iters=100)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


# 变化检测
@app.route('/')
def index():
    return "Welcome to RSIIISystem's CD Server!"


# 数据上传
@app.route('/changeDetection/uploadImgA', methods=['POST'])
def cUploadImgA():
    fileDir = os.path.join(basedir, app.config['TMPDIR_FOLDER'])
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    f = request.files['file']
    logging.info(str(datetime.datetime.now()) + ' - ' + f.filename)
    if f:
        fileName = secure_filename(f.filename)
        extension = fileName.rsplit('.', 1)[1]
        newFilename = create_uuid() + '.' + extension
        savePath = os.path.join(fileDir, newFilename)
        f.save(savePath)
        imgAUrl = "http://localhost:5001/changeDetection/getImage/" + newFilename
        return jsonify({"success": 0, "msg": "上传成功",
                        "imgAUrl": imgAUrl, "infoListImgA": [getImgInfo(savePath)]})
    else:
        return jsonify({"error": 1000, "msg": "上传失败"})


@app.route('/changeDetection/uploadImgB', methods=['POST'])
def cUploadImgB():
    fileDir = os.path.join(basedir, app.config['TMPDIR_FOLDER'])
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    f = request.files['file']
    logging.info(str(datetime.datetime.now()) + ' - ' + f.filename)
    if f:
        fileName = secure_filename(f.filename)
        extension = fileName.rsplit('.', 1)[1]
        newFilename = create_uuid() + '.' + extension
        savePath = os.path.join(fileDir, newFilename)
        f.save(savePath)
        imgBUrl = "http://localhost:5001/changeDetection/getImage/" + newFilename
        return jsonify({"success": 0, "msg": "上传成功",
                        "imgBUrl": imgBUrl, "infoListImgB": [getImgInfo(savePath)]})
    else:
        return jsonify({"error": 1000, "msg": "上传失败"})


@app.route('/changeDetection/uploadZip', methods=['POST'])
def cUploadZip():
    fileDir = os.path.join(basedir, app.config['TMPDIR_FOLDER'])
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    f = request.files['file']
    logging.info(str(datetime.datetime.now()) + ' - ' + f.filename)
    if f:
        fileName = secure_filename(f.filename)
        zipRandomId = fileName.split('_')[0]
        extension = fileName.rsplit('.', 1)[1]
        newFilename = zipRandomId + '.' + extension
        f.save(os.path.join(fileDir, newFilename))

        # 创建文件夹
        dirName = create_uuid()
        dirPath = './tmpDir/' + dirName + '/'
        # 没有就创建该文件夹
        createDir(dirPath)
        # 解压文件
        zipfile.ZipFile('./tmpDir/' + newFilename).extractall(dirPath)
        # 获取文件路径列表
        dirList = getAllDirPath(dirPath)
        print(dirList)
        imgAList = getFilesPathBySuffix(dirList[2])
        imgBList = getFilesPathBySuffix(dirList[3])
        print(imgAList)
        print(imgBList)
        # 模型预测
        if len(imgAList) != len(imgBList) or len(imgAList) == 0:
            return jsonify({"error": 1000, "msg": "压缩包不符合要求"})

        extension = 'png'

        # cdModel = pdrs.deploy.Predictor('./model/exportedModel/changeDetection')

        length = len(imgAList)
        for i in range(length):
            result = model.CDPredict(imgAList[i], imgBList[i], cdModel)
            name = getFileName(imgAList[i]) + "_" + getFileName(imgBList[i])
            tmpList = model.CDResultSave(result, name + '.' + extension,
                                         name + '_show.' + extension, dirPath)
            # 将处理进度保存到全局变量中
            progressNum[zipRandomId] = int((i + 1) * 100 / length)
        print(tmpList)
        # 结果压缩
        baseurl = "http://localhost:5001/changeDetection/download/"
        # 压缩结果数据
        zipName = create_uuid() + '.zip'
        zipDir(tmpList[2], './tmpDir/' + zipName)
        zipUrl = baseurl + zipName
        # 返回响应结果
        print("批处理完成")
        return jsonify({"success": 0, "msg": "处理完成", "zipUrl": zipUrl})
    else:
        return jsonify({"error": 1000, "msg": "上传失败"})


@app.route('/changeDetection/getProgressNum', methods=['POST'])
def cGetProgressNum():
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    zipRandomId = data['zipRandomId']
    return jsonify({'status': 200, 'code': 0, "message": "获取成功",
                    "progressNum": (0 if progressNum.get(zipRandomId) is None else int(progressNum.get(zipRandomId)))})


# 数据处理
@app.route('/changeDetection/handle', methods=['POST'])
def cHandle():
    time_start = time.time()  # 计时开始
    data = json.loads(request.get_data())
    # 日志打印
    logging.info(data)
    extension = 'png'
    # cdModel = pdrs.deploy.Predictor('./model/exportedModel/changeDetection')
    result = model.CDPredict('./tmpDir/' + data['imgAName'], './tmpDir/' + data['imgBName'], cdModel)
    name = create_uuid()
    saveName01 = name + '.' + extension
    saveName02 = name + '_show.' + extension
    resultNameList = model.CDResultSave(result, saveName01, saveName02)
    print(resultNameList)
    baseurl1 = "http://localhost:5001/changeDetection/getImage/"
    baseurl2 = "http://localhost:5001/changeDetection/download/"
    srcListResult = [baseurl1 + resultNameList[0], baseurl1 + resultNameList[1]]
    resultImgPath = os.path.join('./tmpDir/', resultNameList[0])
    # 将结果压缩为压缩包
    resultZipUrl = baseurl2 + zipFiles(resultNameList[:-1], './tmpDir')
    time_end = time.time()  # 计时结束
    infoListResult = getImgInfo(resultImgPath)
    infoListResult.append(('%.2f' % (time_end - time_start)) + 's')
    return jsonify({"success": 0, "msg": "处理完毕",
                    "srcListResult": srcListResult,
                    "resultZipUrl": resultZipUrl,
                    "infoListResult": [infoListResult]
                    })


# 结果下载
@app.route('/changeDetection/download/<string:filename>', methods=['GET'])
def cDownload(filename):
    if os.path.isfile(os.path.join('./tmpDir', filename)):
        return send_from_directory('./tmpDir', filename, as_attachment=True)
    else:
        jsonify({"error": 1000, "msg": "下载出错"})


# 展示图片
@app.route('/changeDetection/getImage/<string:filename>', methods=['GET'])
def cGetImage(filename):
    file_dir = os.path.join(basedir, app.config['TMPDIR_FOLDER'])
    if filename is None:
        pass
    else:
        image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/*'
        return response


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='localhost', port=5001)
