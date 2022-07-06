# 导入第三方库
import cv2
import paddle
from utils.aUtils import *
import matplotlib.pyplot as plt
from paddlers import transforms as T
from paddlers.tasks.utils.visualize import visualize_detection


# tools
def read_image(path):
    im = cv2.imread(path)
    im = im[..., ::-1]
    return im


def pltImgSave(im, savePath):
    plt.axis('off')  # 关掉坐标轴为 off
    plt.gcf().set_size_inches(512 / 100, 512 / 100)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.imshow(im)
    plt.savefig(savePath)
    return True


# ------------------------------模型推理
# 变化检测模型推理
def CDPredict(imgPath01, imgPath02, cdModel):
    return cdModel.predict(img_file=(imgPath01, imgPath02))


# 地物分类模型推理
def GOCPredict(imgPath, gocModel):
    return gocModel.predict(img_file=imgPath)


# 目标检测模型推理
def ODPredict(imgPath, odModel):
    INPUT_SIZE = 608
    im = read_image(imgPath)
    im = cv2.resize(im[..., ::-1], (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_CUBIC)
    eval_transforms = T.Compose([
        # 使用双三次插值将输入影像缩放到固定大小
        T.Resize(
            target_size=INPUT_SIZE, interp='CUBIC'
        ),
        # 验证阶段与训练阶段的归一化方式必须相同
        T.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
    ])
    return {'im': im, 'pred': odModel.predict(im, eval_transforms)}


# 目标提取模型推理
def TEPredict(imgPath, teModel):
    return teModel.predict(img_file=imgPath)


# ------------------------------模型推理结果保存
# 变化检测模
def CDResultSave(result, saveName01, saveName02, saveDir='./tmpDir/'):
    if saveDir == './tmpDir/':
        savePath01 = saveDir + saveName01
        savePath02 = saveDir + saveName02
    else:
        saveDir = saveDir + 'output/'
        createDir(saveDir)
        createDir(saveDir + 'result/')
        createDir(saveDir + 'show/')
        savePath01 = saveDir + 'result/' + saveName01
        savePath02 = saveDir + 'show/' + saveName02
    # 保存原始结果图像数据
    tmp = result[0]['label_map']
    tmp[tmp > 0] = 255
    arr = np.array(tmp, dtype='uint8')
    arr = Image.fromarray(arr)
    print('arr:', arr.size)
    arr.save(savePath01)
    # 保存处理后，更容易被人眼观察的结果数据
    # plt保存结果数据
    pltImgSave(arr, savePath02)
    return [saveName01, saveName02, saveDir]


# 地物分类
def GOCResultSave(result, saveName01, saveName02, saveDir='./tmpDir/'):
    if saveDir == './tmpDir/':
        savePath01 = saveDir + saveName01
        savePath02 = saveDir + saveName02
    else:
        saveDir = saveDir + 'output/'
        createDir(saveDir)
        createDir(saveDir + 'result/')
        createDir(saveDir + 'show/')
        savePath01 = saveDir + 'result/' + saveName01
        savePath02 = saveDir + 'show/' + saveName02
    # 保存原始结果图像数据
    arr = Image.fromarray(result['label_map'])
    arr.save(savePath01)
    # 保存处理后，更容易被人眼观察的结果数据
    im = np.array(arr)
    lut = np.zeros((256, 3), dtype=np.uint8)
    lut[0] = [255, 0, 0]
    lut[1] = [30, 255, 142]
    lut[2] = [60, 0, 255]
    lut[3] = [255, 222, 0]
    lut[4] = [0, 0, 0]
    if isinstance(im, str):
        im = cv2.imread(im, cv2.IMREAD_COLOR)
    if lut is not None:
        if im.ndim == 3:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = lut[im]
    else:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    # plt保存结果数据
    pltImgSave(im, savePath02)
    return [saveName01, saveName02, saveDir]


# 目标检测
def ODResultSave(result, saveName01, saveName02, saveDir='./tmpDir/'):
    if saveDir == './tmpDir/':
        savePath01 = saveDir + saveName01
        savePath02 = saveDir + saveName02
    else:
        saveDir = saveDir + 'output/'
        createDir(saveDir)
        createDir(saveDir + 'result/')
        createDir(saveDir + 'show/')
        savePath01 = saveDir + 'result/' + saveName01
        savePath02 = saveDir + 'show/' + saveName02
    im = result['im']
    pred = result['pred']
    # 保存原始结果数据
    f = open(savePath01, 'w')
    f.write(str(pred))
    f.close()
    # 保存处理后，更容易被人眼观察的结果数据
    # 绘制目标框
    with paddle.no_grad():
        # 用绿色画出预测目标框
        if len(pred) > 0:
            im = visualize_detection(
                np.array(im), pred,
                color=np.asarray([[0, 255, 0]], dtype=np.uint8),
                threshold=0.4, save_dir=None
            )
        # plt保存结果数据
        pltImgSave(im, savePath02)
    # 计算目标数量
    num = 0
    for i in pred:
        if i['score'] > 0.4:
            num += 1
    return [saveName01, saveName02, saveDir, num]


# 目标提取
def TEResultSave(result, saveName01, saveName02, saveDir='./tmpDir/'):
    if saveDir == './tmpDir/':
        savePath01 = saveDir + saveName01
        savePath02 = saveDir + saveName02
    else:
        saveDir = saveDir + 'output/'
        createDir(saveDir)
        createDir(saveDir + 'result/')
        createDir(saveDir + 'show/')
        savePath01 = saveDir + 'result/' + saveName01
        savePath02 = saveDir + 'show/' + saveName02
    # 保存原始结果图像数据
    arr = Image.fromarray(result['label_map'])
    arr.save(savePath01)
    # 保存处理后，更容易被人眼观察的结果数据
    im = np.array(arr)
    quantize = True
    if isinstance(im, str):
        im = arr
    if quantize:
        im = (im * 255).astype('uint8')
    if im.ndim == 2:
        im = np.tile(im[..., np.newaxis], [1, 1, 3])
    # plt保存结果数据
    pltImgSave(im, savePath02)
    return [saveName01, saveName02, saveDir]
