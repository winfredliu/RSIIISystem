import os
import random
import zipfile
import datetime
import numpy as np
from PIL import Image


def chooseFilePath(detail=""):
    path = input("请输入" + detail + "图片的路径:").replace("\\", "/").replace('"', '')
    return path


def chooseSavePath():
    print("输出图片将存储在\"output\"文件夹中！")
    dir = "./output/"
    fileName = input("请输入存储文件名:").strip()
    while len(fileName) <= 0 or fileName.lower() == ".bmp":
        print("存储名字不合规！")
        fileName = input("请重新输入存储名字:").strip()
    if fileName[-4:].lower() != ".bmp":
        fileName += ".bmp"
    path = dir + fileName
    return path


def image_save(imageArray, saveName='test', saveType='png'):
    print(imageArray, type(imageArray))
    imageArray[imageArray > 0] = 255
    arr = np.array(imageArray, dtype='uint8')
    arr = Image.fromarray(arr)
    arr.save(saveName + '.' + saveType, saveType)


def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


def zipFiles(fileList, fileDir):
    filename = create_uuid() + '.zip'
    # 遍历files文件夹下的文件，压缩发送
    tmp = zipfile.ZipFile(os.path.join('./tmpDir', filename), 'w')
    for i in fileList:
        tmp.write(os.path.join(fileDir, i), i, zipfile.ZIP_DEFLATED)
    return filename


def zipDir(dirPath, outFullName):
    """
    压缩指定文件夹
    :param dirPath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zipTmp = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirNames, fileNames in os.walk(dirPath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fPath = path.replace(dirPath, '')
        for fileName in fileNames:
            zipTmp.write(os.path.join(path, fileName), os.path.join(fPath, fileName))
    zipTmp.close()
    return


def getFileName(filePath):
    tmp = filePath.split('/')[-1]
    return tmp.split('.')[0]


def getFileExtension(filePath):
    return filePath.split('.')[-1]


def getAllDirPath(dirPath):
    dirList = []
    for root, dirs, files in os.walk(dirPath):
        root = root.replace('\\', '/')
        dirList.append(root)
    return dirList


def getFilesPathBySuffix(dirPath, suffix=""):
    if dirPath[-1] == '/':
        dirPath = dirPath[:-1]
    allFilesPath = []
    for root, dirs, files in os.walk(dirPath):
        root = root.replace("\\", "/")
        for filePath in os.listdir(root):
            if not (filePath.lower().endswith(suffix)):
                continue
            if os.path.isdir(root + "/" + filePath):
                continue
            allFilesPath.append(root + "/" + filePath)
    return allFilesPath


# 获取文件大小
def getFileSize(filePath):
    size = os.path.getsize(filePath)
    length = len('%.2f' % size)
    if length <= 6:
        return ('%.2f' % size) + 'B'
    elif 6 < length <= 9:
        return ('%.2f' % (size / 1024)) + 'KB'
    elif 9 < length <= 12:
        return ('%.2f' % (size / 1024 / 1024)) + 'MB'
    else:
        return ('%.2f' % (size / 1024 / 1024 / 1024)) + 'GB'


# 获取图像的信息(长、宽、位深、大小、类型)
def getImgInfo(imgPath):
    img = Image.open(imgPath)
    # 获取长宽
    length, width = img.size
    # 获取位深
    bands = ''.join(img.getbands()).lower()
    if bands == '1':
        bitDepth = 1
    elif bands == 'l' or bands == 'p':
        bitDepth = 8
    elif bands == 'rgb' or bands == 'ycbcr':
        bitDepth = 24
    elif bands == 'i' or bands == 'f' or bands == 'rgba' or bands == 'cmyk':
        bitDepth = 32
    else:
        bitDepth = 32
    # 获取内存大小
    size = getFileSize(imgPath)
    # 获取类型
    imgType = getFileExtension(imgPath)
    return [length, width, bitDepth, size, imgType]


# 创建文件夹
def createDir(dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    return
