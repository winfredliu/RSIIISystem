<template>
  <div id="TargetExtraction">
    <div id="Content">
      <!-- VUE弹窗 -->
      <el-dialog
          id="eDialog"
          title="压缩包说明"
          :visible.sync="eDialogVisible"
          width="65%"
          :before-close="eDialogHandleClose"
      >
        <el-steps :active="3" finish-status="process">
          <el-step title="压缩包注意事项" style="width: 280px; padding-left: 50px">
            <template slot="description">
              <p>1、名称任意。</p>
              <p>2、小于100MB。</p>
              <p>3、内部文件命名不能出现中文。</p>
            </template>
          </el-step>
          <el-step title="压缩包目录结构" style="width: 260px; margin-left: -5px">
            <template slot="description">
              <div>
                <p>1、无目录结构。</p>
                <br/>
                <br/>
              </div>
            </template>
          </el-step>
          <el-step title="压缩包内容说明" style="width: 260px; margin-left: -5px">
            <template slot="description">
              <div>
                <p>1、只能含有图像文件。</p>
                <p>2、无其他文件或文件夹。</p>
                <br/>
              </div>
            </template>
          </el-step>
        </el-steps>
        <span slot="footer" class="dialog-footer" style="text-align: center !important;">
        <el-button type="primary" @click="eDialogUploadZip">上传压缩包</el-button>
        <input ref="UZip" style="display: none"
               name="file" type="file" @change="uploadZip"
               accept="application/zip"
        />
      </span>
      </el-dialog>
      <!-- 左边的操作指导栏 -->
      <div id="aLeftSide">
        <el-card
            body-style="padding: 5px"
            style="width: 249px; height: 398px; margin-top: 3px;border-radius:10px;"
        >
          <div slot="header" class="clearfix" style="text-align: center">
            <span class="steps" style="letter-spacing: 7px">操作步骤</span>
          </div>
          <div style="height: 400px;margin-left:40px;" class="stepDiv">
            <el-steps
                direction="vertical"
                :active="stepNum1"
                finish-status="success"
            >
              <el-step style="height: 75px" title="步骤 1">
                <template slot="description">
                  <!-- 上传文件 -->
                  上传待提取的图片
                  <el-button
                      type="primary"
                      icon="el-icon-upload"
                      @click="true_uploadStep"
                      class="elBtn"
                  >上传
                    <input ref="uploadStep"
                           style="display: none"
                           name="file" type="file"
                           @change="updateImg"
                           accept="image/png, image/jpg, image/jpeg"
                    />
                  </el-button>
                </template>
              </el-step>
              <el-step style="height: 75px" title="步骤 2">
                <template slot="description">
                  <!-- 选择目标 -->
                  选择提取目标
                  <el-button
                      type="primary"
                      icon="el-icon-thumb"
                      @click="chooseExtractType"
                      class="elBtn"
                  >目标
                  </el-button>
                </template>
              </el-step>
              <el-step style="height: 95px" title="步骤 3">
                <template slot="description">
                  <!-- 发起请求 -->
                  <p>点击提取按钮,</p>
                  <p>发起目标提取请求</p>
                  <el-button
                      type="primary"
                      icon="el-icon-data-analysis"
                      @click="targetExtraction"
                      class="elBtn"
                  >提取
                  </el-button>
                </template>
              </el-step>
              <!-- 获得图像 -->
              <el-step style="height: 75px" title="步骤 4">
                <template slot="description">
                  <!-- 下载文件 -->
                  下载目标提取结果
                  <el-button
                      type="primary"
                      icon="el-icon-download"
                      @click="downloadResultImg"
                      class="elBtn"
                  >下载
                  </el-button>
                </template>
              </el-step>
              <el-step title="成功获得结果图片" style="height: 200px">
                <template slot="description"></template>
              </el-step>
            </el-steps>
          </div>
        </el-card>
        <el-card
            body-style="padding: 3px"
            style="width: 249px; height: 166px; margin-top: 2px;border-radius:10px;"
        >
          <div slot="header" class="clearfix" style="text-align: center">
            <span class="steps" style="letter-spacing: 7px">批处理</span>
          </div>
          <div style="height: 180px;margin-left:40px;">
            <el-steps
                direction="vertical"
                :active="stepNum2"
                finish-status="success"
            >
              <el-step style="height: 52px;" title="压缩文件上传">
                <template slot="description">
                  <!-- 上传文-->
                  <el-button
                      v-show="uBtnShow"
                      type="primary"
                      icon="el-icon-upload"
                      @click="true_uploadZip"
                      class="elBtn"
                  >上传
                  </el-button>
                  <div v-show="uProShow" style="padding-right: 10px">
                    <p v-show="loadShow">处理中<i class="el-icon-loading"></i></p>
                    <p v-show="!loadShow">处理完毕<i class="el-icon-circle-check" style="color:green"></i></p>
                    <el-progress :percentage="progressNum"></el-progress>
                  </div>
                </template>
              </el-step>
              <el-step style="height: 10px" title="处理结果下载">
                <template slot="description">
                  <!-- 下载文件 -->
                  <el-button
                      type="primary"
                      icon="el-icon-upload"
                      @click="downResultZip"
                      class="elBtn"
                  >下载
                  </el-button>
                </template>
              </el-step>
            </el-steps>
          </div>
        </el-card>
      </div>
      <!-- 右边的图像显示栏 -->
      <div id="aRightSide">
        <!-- 图像框 -->
        <div id="imageBox">
          <el-card
              id="imageCard"
              style="
            border-radius: 8px;
            width: 800px;
            height: 390px;
            margin-bottom: -5px;
          "
          >
            <div class="imagePreview1">
              <div
                  v-loading="loadingImg"
                  element-loading-text="上传图片中"
                  element-loading-spinner="el-icon-loading"
              >
                <el-image
                    :src="imgUrl"
                    class="imageClass"
                    :preview-src-list="srcListImg"
                    style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      <el-button
                          v-show="true"
                          type="primary"
                          icon="el-icon-upload"
                          class="elBtn"
                          v-on:click="true_upload"
                      >
                        上传
                        <input
                            ref="upload"
                            style="display: none"
                            name="file"
                            type="file"
                            @change="updateImg"
                            accept="image/png, image/jpg, image/jpeg"
                        />
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <!-- 图片下方文字 -->
              <div class="imgInfo" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 6px">待目标提取图片</span>
              </div>
            </div>
            <div class="imagePreview2">
              <div
                  v-loading="loadingResult"
                  element-loading-text="处理中,请耐心等待"
                  element-loading-spinner="el-icon-loading"
              >
                <el-image
                    :src="imgResultUrl"
                    class="imageClass"
                    :preview-src-list="srcListResult"
                    style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      <el-button
                          v-show="true"
                          type="primary"
                          icon="el-icon-data-analysis"
                          class="elBtn"
                          v-on:click="targetExtraction"
                      >
                        提取
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <!-- 图片下方文字 -->
              <div class="imgInfo" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 4px"
              >目标提取结果</span>
              </div>
            </div>
          </el-card>
        </div>
        <!-- 卡片放置表格 -->
        <el-card id="elCard">
          <div slot="header" class="clearfix" style="padding: 10px 0px">
            <span>目标提取 - 详情</span>
          </div>
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="输入图像" name="first">
              <!-- 表格存放特征值 -->
              <el-table :data="infoListImg"
                        border
                        class="elTable"
                        v-loading="loadingInfoImg"
                        element-loading-text="数据正在加载中，请耐心等待..."
                        element-loading-spinner="el-icon-loading"
                        lazy
              >
                <el-table-column label="长" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[0] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="宽" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[1] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="位深" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[2] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="大小" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[3] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="类型" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[4] }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="结果图像" name="second">
              <!-- 表格存放特征值 -->
              <el-table :data="infoListResult"
                        border
                        class="elTable"
                        v-loading="loadingInfoResult"
                        element-loading-text="数据正在加载中，请耐心等待..."
                        element-loading-spinner="el-icon-loading"
                        lazy
              >
                <el-table-column label="长" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[0] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="宽" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[1] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="位深" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[2] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="大小" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[3] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="类型" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[4] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="目标名称" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[5] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="处理时长" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[6] }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
      <!--弹框-->
      <div>
        <el-dialog title="表单弹框" :visible.sync="dialogIsVisible" width="30%">
          <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="目标">
              <el-radio-group v-model="form.resource">
                <el-radio label="overpass" class="radioLabel"></el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogIsVisible = false">取 消</el-button>
            <el-button type="primary" @click="typeConfirm">确 定</el-button>
          </span>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {GenNonDuplicateID, getFileSize, getFileSuffix, getUrlName} from "../../util/util";

export default {
  name: "TargetExtraction",
  data() {
    return {
      imgUrl: '',
      imgResultUrl: '',
      srcListImg: [],
      srcListResult: [],
      loadingImg: false,
      loadingResult: false,
      table: false,
      stepNum1: 0,
      stepNum2: 0,
      dialogIsVisible: false,
      form: {},

      activeName: "first",
      infoListImg: [["——", "——", "——", "——", "——"]],
      infoListResult: [["——", "——", "——", "——", "——", "——", "——"]],
      loadingInfoImg: false,
      loadingInfoResult: false,

      eDialogVisible: false,

      uBtnShow: true,
      uProShow: false,
      loadShow: false,
      ifUploadZip: false,

      resultZipUrl: '',
      zipUrl: '',
      zipRandomId: '',

      progressNum: 0,
    };
  },
  created: function () {
    document.title = "目标提取";
  },
  methods: {
    successInfo(message) {
      this.$message({
        message: message,
        type: 'success'
      });
      return true;
    },
    eDialogHandleClose(done) {
      console.log("弹窗关闭");
      done();
    },
    eDialogUploadZip() {
      this.$refs.UZip.click();
    },
    nextStep1(num) {
      if (num == 1 && this.stepNum1 >= 2) {
        num = 2;
      }
      this.stepNum1 = num;
    },
    nextStep2(num) {
      if (num == 1 && this.stepNum2 >= 2) {
        num = 2;
      }
      this.stepNum2 = num;
    },
    true_uploadStep() {
      this.$refs.uploadStep.click();
    },
    true_upload() {
      console.log("upload img");
      this.$refs.upload.click();
    },
    true_uploadZip() {
      this.form = {};
      this.ifUploadZip = true;
      this.dialogIsVisible = true;
    },
    // 上传文件
    updateImg(e) {
      this.loadingImg = true;
      let file = e.target.files[0];

      //判断文件类型是否符合要求
      if (['png', 'jpg', 'jpeg'].indexOf(getFileSuffix(file)) < 0) {
        this.$message({
          message: '文件类型需为png/jpg/jpeg',
          type: 'warning'
        });
        this.loadingImg = false;
        return;
      }
      //判断文件内存大小是否符合要求
      if (getFileSize(file) > 10) {
        this.$message({
          message: '图片内存大小需小于10MB',
          type: 'warning'
        });
        this.loadingImg = false;
        return;
      }

      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据
      //添加请求头
      let config = {
        headers: {"Content-Type": "multipart/form-data"},
        timeout: 1000 * 60
      };
      // 发起上传请求
      axios.post("/targetExtraction/uploadImg", param, config)
          .then((response) => {
            console.log(response);
            this.imgUrl = response.data.imgUrl;
            this.infoListImg = response.data.infoListImg;
            this.srcListImg[0] = this.imgUrl;
            this.loadingImg = false;
            this.form = {}
            this.nextStep1(1);
          })
          .catch((error) => {
            console.log(error.toString());
            this.$confirm('请检查网络连接是否正常!', {
              title: '提示',
              type: 'warning'
            });
            this.loadingImg = false;
          })
    },
    //选择提取目标
    chooseExtractType() {
      if (this.imgUrl == '') {
        this.$message({
          message: '请先上传待进行目标提取的图片',
          type: 'warning'
        });
        return;
      }
      console.log("选择提取目标");
      this.ifUploadZip = false;
      this.dialogIsVisible = true;
    },
    //表单提交
    typeConfirm() {
      if (this.ifUploadZip) {
        this.dialogIsVisible = false;
        console.log(this.form.resource)
        if (this.form.resource != undefined) {
          this.eDialogVisible = true;
        }
        return;
      }
      this.dialogIsVisible = false;
      console.log(this.form);
      this.nextStep1(2);
    },
    //目标提取函数
    targetExtraction() {
      if (!this.form.hasOwnProperty('resource')) {
        this.$message({
          message: '请先选择目标提取目标',
          type: 'warning'
        });
        return;
      }
      this.loadingResult = true;
      console.log("开始目标提取");
      // 发起处理请求
      axios.post("/targetExtraction/handle",
          {objectName: this.form.resource, imgName: getUrlName(this.imgUrl)}, {timeout: 1000 * 60 * 30})
          .then((response) => {
            console.log(response);
            console.log('处理完毕');
            this.imgResultUrl = response.data.srcListResult[1];
            this.srcListResult = response.data.srcListResult;
            this.resultZipUrl = response.data.resultZipUrl;
            this.infoListResult = response.data.infoListResult;
            this.loadingResult = false;
            this.nextStep1(3);
          })
          .catch((error) => {
            console.log(error.toString());
            this.$confirm('请检查网络连接是否正常!', {
              title: '提示',
              type: 'warning'
            });
            this.loadingResult = false;
          })
    },
    // 下载 点击按钮 从远程接口获取文件
    downloadByName(name) {
      // 发起下载请求
      const a = document.createElement('a');
      a.href = '/targetExtraction/download/' + name
      a.download = name
      a.click()
    },
    downloadResultImg() {
      if (this.imgResultUrl == '') {
        this.$message({
          message: '请先进行提取操作',
          type: 'warning'
        });
        return;
      }
      console.log("下载目标提取结果图片")
      this.downloadByName(getUrlName(this.resultZipUrl));
      this.nextStep1(5);
    },
    uploadZip(e) {
      console.log("上传压缩文件");
      this.eDialogVisible = false;
      this.uBtnShow = false;
      this.uProShow = true;
      this.loadShow = true;

      let file = e.target.files[0];

      //判断文件类型是否符合要求
      if (['zip'].indexOf(getFileSuffix(file)) < 0) {
        this.$message({
          message: '文件类型需为zip',
          type: 'warning'
        });
        this.uBtnShow = true;
        this.uProShow = false;
        this.loadShow = false;
        return;
      }

      //判断文件内存大小是否符合要求
      if (getFileSize(file) > 100) {
        this.$message({
          message: '压缩包大小需小于100MB',
          type: 'warning'
        });
        this.uBtnShow = true;
        this.uProShow = false;
        this.loadShow = false;
        return;
      }
      this.zipRandomId = GenNonDuplicateID();
      console.log(this.zipRandomId);
      let param = new FormData(); //创建form对象
      param.append("file", file, this.zipRandomId + '_' + this.form.resource + '_' + file.name); //通过append向form对象添加数据
      //添加请求头
      let config = {
        headers: {"Content-Type": "multipart/form-data"},
      };
      // 发起上传请求
      axios.post("/targetExtraction/uploadZip", param, config)
          .then((response) => {
            console.log(response);
            this.zipUrl = response.data.zipUrl;
            this.loadShow = false;
            this.progressNum = 100;
            this.nextStep2(1);
          })
          .catch((error) => {
            console.log(error.toString());
            this.$confirm('请检查网络连接是否正常!', {
              title: '提示',
              type: 'warning'
            });
            this.loadShow = false;
            return
          })

      // 获取后台进度
      let intervalId = setInterval(() => {
        console.log(this.progressNum);
        axios.post("/targetExtraction/getProgressNum", {zipRandomId: this.zipRandomId})
            .then((response) => {
              this.progressNum = response.data.progressNum;
              if (this.progressNum == 100) {
                clearInterval(intervalId);
              }
            })
            .catch((error) => {
              console.log(error.toString());
              this.$confirm('请检查网络连接是否正常!', {
                title: '提示',
                type: 'warning'
              });
              clearInterval(intervalId);
            })
      }, 1000);
    },
    downResultZip() {
      console.log("下载文件");
      if (this.uProShow == false) {
        this.$message({
          message: '请先上传压缩文件！',
          type: 'warning'
        });
        return;
      }
      if (this.progressNum != 100) {
        this.$message({
          message: '数据正在处理中！请耐心等待...',
          type: 'warning'
        });
        return;
      }
      this.downloadByName(getUrlName(this.zipUrl));
      this.nextStep2(2);
      //批处理进度重置
      setTimeout(() => {
        this.successInfo('下载完成！批处理进度已重置！');
        this.uBtnShow = true;
        this.uProShow = false;
        this.loadShow = false;
        this.progressNum = 0;
        this.stepNum2 = 0;
      }, 1000);
    },
    handleClick() {
    }
  },
  // mounted() {
  // }
}
</script>


<style>
.el-button {
  padding: 12px 20px !important;
}

.el-image-viewer__btn {
  opacity: 1 !important;
}
</style>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

div {
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

#TargetExtraction {
  display: flex;
  padding: 0px !important;
  margin: 0px !important;
  background-color: rgb(226, 225, 230) !important;
}

@media screen and (min-height: 580px) {
  #TargetExtraction {
    /*内容垂直居中*/
    align-items: center;
  }
}

@media screen and (min-width: 1165px) {
  #TargetExtraction {
    /*内容水平居中*/
    justify-content: center;
  }
}

#Content {
  background-color: rgb(246, 245, 250) !important;
  border-radius: 12px;
  display: flex;
  width: 1071px !important;
  height: 582px !important;
  padding: 0px !important;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

#aLeftSide {
  width: 260px;
  height: 575px;
  padding: 1px 5px;
  margin: 2px 10px;
  border-radius: 8px;
  background-color: #ffffff;
  /*margin-right: 80px;*/
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#aRightSide {
  display: flex;
  height: 100%;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0px;
  max-width: 1200px;
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#imageBox {
  margin-left: 20px;
  margin-top: 5px;
}

#imageCard {
  width: 750px !important;
  height: 350px !important;
  margin-top: 2px;
  border-radius: 4px;
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

.imageClass {
  width: 300px;
  height: 280px;
  background: #ffffff;
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.1);
}

.imgInfo {
  height: 30px;
  width: 300px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.imagePreview1 {
  width: 300px;
  height: 280px;
  float: left;
  margin-left: 20px;
  margin-top: 9px;
}

.imagePreview2 {
  width: 300px;
  height: 280px;
  float: right;
  margin-right: 20px;
  margin-top: 9px;
  /* background-color: green; */
}

.error {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

.elBtn {
  padding: 10px 16px !important;
}

.file {
  width: 200px;
  height: 130px;
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 1;
  -moz-opacity: 0;
  -ms-opacity: 0;
  -webkit-opacity: 0;
  opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
  filter: alpha(opacity=0);
  cursor: pointer;
}

.steps {
  font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
  "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  color: #21b3b9;
  text-align: center;
  margin: 15px auto;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.stepDiv {
  /*color: #303133 !important;*/
  margin: 0px 26px;
}

.radioLabel {
  padding-top: 12px;
  padding-left: 3px !important;
  padding-right: 10px !important;
}

#elCard {
  width: 750px !important;
  height: 213px !important;
  margin-top: 3px;
  margin-left: 20px;
  padding: 0px;
  border-radius: 8px;
}

.el-card /deep/ .el-card__header {
  padding: 10px !important;
}

.el-card /deep/ .el-card__body {
  padding: 10px !important;
}

.el-table /deep/ .el-table__cell {
  padding: 5px;
}

.el-table--border /deep/ th.el-table__cell {
  padding: 0px;
  margin: 0px;
}

.elTable {
  height: 81px;
  width: 750px;
  text-align: center;
}

.elTbColum {
  width: 100px !important;
  height: 60px !important;
  padding: 0px !important;
  margin: 0px !important;
}

.el-step.is-vertical /deep/ .el-step__title {
  padding-bottom: 0px;
}

/deep/ .el-dialog__footer {
  text-align: center !important;
}
</style>
