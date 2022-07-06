<template>
  <div id="ChangeDetection">
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
                <p>|&emsp;--&emsp;Dir</p>
                <p>|&emsp;|&emsp;--&emsp;DirA</p>
                <p>|&emsp;|&emsp;--&emsp;DirB</p>
              </div>
            </template>
          </el-step>
          <el-step title="压缩包内容说明" style="width: 260px; margin-left: -5px">
            <template slot="description">
              <div>
                <p>1、Dir文夹件中有两个文件夹DirA和DirB。</p>
                <p>2、DirA和DirB分别存放变化前后的图像。</p>
                <p>3、DirA和DirB中的图像要一一对应。</p>
              </div>
            </template>
          </el-step>
        </el-steps>
        <span slot="footer" class="dialog-footer" style="text-align: center !important;">
        <el-button type="primary" @click="eDialogUploadZip">上传压缩包</el-button>
        <input ref="UZip" style="display: none"
               name="file" type="file" @change="uploadZip"
               accept="application/zip"/>
      </span>
      </el-dialog>
      <!-- 左边的操作指导栏 -->
      <div id="aLeftSide">
        <el-card
            body-style="padding: 5px"
            style="width: 249px; height: 500px; margin-top: 3px"
        >
          <div slot="header" class="clearfix" style="text-align: center">
            <span class="steps" style="letter-spacing: 7px">操作步骤</span>
          </div>
          <div style="height: 600px;margin-left:40px" class="stepDiv">
            <el-steps
                direction="vertical"
                :active="stepNum1"
                finish-status="success"
            >
              <el-step style="height: 90px" title="步骤 1">
                <template slot="description">
                  <!-- 上传文件 -->
                  上传变化前的图片A
                  <el-button
                      type="primary"
                      icon="el-icon-upload"
                      @click="true_uploadAStep"
                      class="elBtn"
                  >上传
                    <input ref="uploadAStep"
                           style="display: none"
                           name="file" type="file"
                           @change="updateImgA"
                           accept="image/png, image/jpg, image/jpeg"
                    />
                  </el-button>
                </template>
              </el-step>
              <el-step style="height: 90px" title="步骤 2">
                <template slot="description">
                  <!-- 上传文件 -->
                  上传变化后的图片B
                  <el-button
                      type="primary"
                      icon="el-icon-upload"
                      @click="true_uploadBStep"
                      class="elBtn"
                  >上传
                    <input ref="uploadBStep"
                           style="display: none"
                           name="file" type="file"
                           @change="updateImgB"
                           accept="image/png, image/jpg, image/jpeg"
                    />
                  </el-button>
                </template>
              </el-step>
              <el-step style="height: 115px" title="步骤 3">
                <template slot="description">
                  <!-- 发起请求 -->
                  <p>点击检测按钮,</p>
                  <p>发起变化检测请求</p>
                  <!-- 下载文件 -->
                  <el-button
                      type="primary"
                      icon="el-icon-data-analysis"
                      @click="changeDetection"
                      class="elBtn"
                  >检测
                  </el-button>
                </template>
              </el-step>
              <!-- 获得图像 -->
              <el-step style="height: 90px" title="步骤 4">
                <template slot="description">
                  <!-- 下载文件 -->
                  下载变化检测结果
                  <el-button
                      type="primary"
                      icon="el-icon-download"
                      @click="downloadResultImg"
                      class="elBtn"
                  >下载
                  </el-button>
                </template>
              </el-step>
              <el-step title="获取成功" style="height: 200px">
                <template slot="description"></template>
              </el-step>
            </el-steps>
          </div>
        </el-card>
        <el-card
            body-style="padding: 3px"
            style="width: 249px; height: 190px; margin-top: 3px"
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
              <el-step style="height: 65px;" title="压缩文件上传">
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
          <el-card id="imageCard">
            <div class="imagePreview1">
              <div
                  v-loading="loadingA"
                  element-loading-text="上传图片中"
                  element-loading-spinner="el-icon-loading"
              >
                <el-image
                    :src="imgAUrl"
                    class="imageClass"
                    :preview-src-list="srcListA"
                    style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      <el-button
                          v-show="true"
                          type="primary"
                          icon="el-icon-upload"
                          class="elBtn"
                          v-on:click="true_uploadA"
                      >
                        图片A
                        <input
                            ref="uploadA"
                            style="display: none"
                            name="file"
                            type="file"
                            @change="updateImgA"
                            accept="image/png, image/jpg, image/jpeg"
                        />
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <!-- 图片下方文字 -->
              <div class="imgInfo" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 6px">变化前遥感图片A</span>
              </div>
            </div>
            <div class="imagePreview2">
              <div
                  v-loading="loadingB"
                  element-loading-text="上传图片中"
                  element-loading-spinner="el-icon-loading"
              >
                <el-image
                    :src="imgBUrl"
                    class="imageClass"
                    :preview-src-list="srcListB"
                    style="border-radius: 3px 3px 0 0"
                >
                  <div slot="error">
                    <div slot="placeholder" class="error">
                      <el-button
                          v-show="true"
                          type="primary"
                          icon="el-icon-upload"
                          class="elBtn"
                          v-on:click="true_uploadB"
                      >
                        图片B
                        <input
                            ref="uploadB"
                            style="display: none"
                            name="file"
                            type="file"
                            @change="updateImgB"
                            accept="image/png, image/jpg, image/jpeg"
                        />
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <!-- 图片下方文字 -->
              <div class="imgInfo" style="border-radius: 0 0 5px 5px">
                <span style="color: white; letter-spacing: 6px">变化后遥感图片B</span>
              </div>
            </div>
            <div class="imagePreview3">
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
                          v-on:click="changeDetection"
                      >
                        检测
                      </el-button>
                    </div>
                  </div>
                </el-image>
              </div>
              <!-- 图片下方文字 -->
              <div class="imgInfo" style="border-radius: 0 0 5px 5px">
              <span style="color: white; letter-spacing: 4px"
              >变化检测结果</span
              >
              </div>
            </div>
          </el-card>
        </div>
        <!-- 卡片放置表格 -->
        <el-card id="elCard">
          <div slot="header" class="clearfix" style="padding: 10px 0px">
            <span>变化检测 - 详情</span>
          </div>
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="图像A" name="first">
              <!-- 表格存放特征值 -->
              <el-table :data="infoListImgA"
                        border
                        class="elTable"
                        v-loading="loadingInfoImgA"
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
            <el-tab-pane label="图像B" name="second">
              <!-- 表格存放特征值 -->
              <el-table :data="infoListImgB"
                        border
                        class="elTable"
                        v-loading="loadingInfoImgB"
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
            <el-tab-pane label="结果图像" name="third">
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
                <el-table-column label="处理时长" class="elTbColum">
                  <template slot-scope="scope">
                    <span>{{ scope.row[5] }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {getFileSuffix, getFileSize, getUrlName, GenNonDuplicateID} from "../../util/util";

export default {
  name: "ChangeDetection",
  data() {
    return {
      imgAUrl: '',
      imgBUrl: '',
      imgResultUrl: '',
      srcListA: [''],
      srcListB: [''],
      srcListResult: [''],
      loadingA: false,
      loadingB: false,
      loadingResult: false,
      table: false,
      stepNum1: 0,
      stepNum2: 0,

      activeName: "first",
      infoListImgA: [["——", "——", "——", "——", "——"]],
      infoListImgB: [["——", "——", "——", "——", "——"]],
      infoListResult: [["——", "——", "——", "——", "——", "——"]],
      loadingInfoImgA: false,
      loadingInfoImgB: false,
      loadingInfoResult: false,

      eDialogVisible: false,

      uBtnShow: true,
      uProShow: false,
      loadShow: false,

      resultZipUrl: '',
      zipUrl: '',
      zipRandomId: '',

      progressNum: 0,
    };
  },
  created: function () {
    document.title = "变化检测";
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
    true_uploadAStep() {
      this.$refs.uploadAStep.click();
    },
    true_uploadBStep() {
      this.$refs.uploadBStep.click();
    },
    true_uploadA() {
      this.$refs.uploadA.click();
    },
    true_uploadB() {
      this.$refs.uploadB.click();
    },
    true_uploadZip() {
      this.eDialogVisible = true;
    },
    // 上传文件
    updateImgA(e) {
      this.loadingA = true;
      let file = e.target.files[0];

      //判断文件类型是否符合要求
      if (['png', 'jpg', 'jpeg'].indexOf(getFileSuffix(file)) < 0) {
        this.$message({
          message: '文件类型需为png/jpg/jpeg',
          type: 'warning'
        });
        this.loadingA = false;
        return;
      }

      //判断文件内存大小是否符合要求
      if (getFileSize(file) > 10) {
        this.$message({
          message: '图片内存大小需小于10MB',
          type: 'warning'
        });
        this.loadingA = false;
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
      axios.post("/changeDetection/uploadImgA", param, config)
          .then((response) => {
            console.log(response);
            this.imgAUrl = response.data.imgAUrl;
            this.infoListImgA = response.data.infoListImgA;
            this.srcListA[0] = this.imgAUrl;
            this.loadingA = false;
            this.nextStep1(1);
            //保存临时会话数据
            // sessionStorage.setItem("cImgAUrl", this.imgAUrl);
          })
          .catch((error) => {
            console.log(error.toString());
            this.$confirm('请检查网络连接是否正常!', {
              title: '提示',
              type: 'warning'
            });
            this.loadingA = false;
          })
    },
    updateImgB(e) {
      this.loadingB = true;
      let file = e.target.files[0];

      //判断文件类型是否符合要求
      if (['png', 'jpg', 'jpeg'].indexOf(getFileSuffix(file)) < 0) {
        this.$message({
          message: '文件类型需为png/jpg/jpeg',
          type: 'warning'
        });
        this.loadingB = false;
        return;
      }

      //判断文件内存大小是否符合要求
      if (getFileSize(file) > 10) {
        this.$message({
          message: '图片内存大小需小于10MB',
          type: 'warning'
        });
        this.loadingB = false;
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
      axios.post("/changeDetection/uploadImgB", param, config)
          .then((response) => {
            console.log(response);
            this.imgBUrl = response.data.imgBUrl;
            this.infoListImgB = response.data.infoListImgB;
            this.srcListB[0] = this.imgBUrl;
            this.loadingB = false;
            this.nextStep1(2);
          })
          .catch((error) => {
            console.log(error.toString());
            this.$confirm('请检查网络连接是否正常!', {
              title: '提示',
              type: 'warning'
            });
            this.loadingB = false;
          })
    },
    //变化检测函数
    changeDetection() {
      if (this.imgAUrl == '') {
        this.$message({
          message: '请上传变化前图片A',
          type: 'warning'
        });
        return;
      }
      if (this.imgBUrl == '') {
        this.$message({
          message: '请上传变化后图片B',
          type: 'warning'
        });
        return;
      }
      this.loadingResult = true;
      console.log("开始变化检测");
      // 发起处理请求
      axios.post("/changeDetection/handle",
          {imgAName: getUrlName(this.imgAUrl), imgBName: getUrlName(this.imgBUrl)}, {timeout: 1000 * 60 * 3})
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
      a.href = '/changeDetection/download/' + name
      a.download = name
      a.click()
    },
    downloadResultImg() {
      if (this.imgResultUrl == '') {
        this.$message({
          message: '请先进行检测',
          type: 'warning'
        });
        return;
      }
      console.log("下载变化检测结果");
      this.downloadByName(getUrlName(this.resultZipUrl));
      this.nextStep1(5);
    },
    uploadZip(e) {
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
      param.append("file", file, this.zipRandomId + '_' + file.name); //通过append向form对象添加数据
      //添加请求头
      let config = {
        headers: {"Content-Type": "multipart/form-data"},
      };
      // 发起上传请求
      axios.post("/changeDetection/uploadZip", param, config)
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
        axios.post("/changeDetection/getProgressNum", {zipRandomId: this.zipRandomId})
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
      console.log("下载文件");
      this.downloadByName(getUrlName(this.zipUrl));
      this.nextStep2(5);
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
  mounted() {
    // this.imgAUrl = sessionStorage.getItem("cImgAUrl");
    // this.imgBUrl = sessionStorage.getItem("cImgBUrl");
    // this.imgResultUrl = sessionStorage.getItem("cImgResultUrl");
  }
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
  margin: 0px;
  padding: 0px;
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

#ChangeDetection {
  display: flex;
  padding: 0px !important;
  margin: 0px !important;
  background-color: rgb(226, 225, 230) !important;
}

@media screen and (min-height: 750px) {
  #ChangeDetection {
    /*内容垂直居中*/
    align-items: center;
  }
}

@media screen and (min-width: 1165px) {
  #ChangeDetection {
    /*内容水平居中*/
    justify-content: center;
  }
}

#Content {
  background-color: rgb(246, 245, 250) !important;
  border-radius: 12px;
  display: flex;
  width: 1071px !important;
  height: 732px !important;
  padding: 0px !important;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

#aLeftSide {
  width: 260px;
  height: 712px;
  padding: 5px;
  margin: 10px;
  border-radius: 8px;
  background-color: #ffffff;
  /*margin-right: 80px;*/
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#aRightSide {
  display: flex;
  height: 712px;
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
  height: 500px !important;
  /*margin: 0px;*/
  border-radius: 8px;
  /* background-color: RGB(239, 249, 251); */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

.imageClass {
  width: 275px;
  height: 200px;
  background: #ffffff;
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.1);
}

.imgInfo {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.imagePreview1 {
  width: 275px;
  height: 200px;
  margin-left: 35px;
  float: left;
}

.imagePreview2 {
  width: 275px;
  height: 200px;
  margin-top: 250px;
  margin-left: 35px;
  /* background-color: green; */
}

.imagePreview3 {
  width: 275px;
  height: 200px;
  margin-top: -300px;
  margin-right: 35px;
  float: right;
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
  margin: 20px 26px;
}


#elCard {
  width: 750px !important;
  height: 218px !important;
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
  height: 60px;
  padding: 0px !important;
  margin: 0px !important;
}

/deep/ .el-dialog__footer {
  text-align: center !important;
}
</style>
