<template>
  <div class="Login" :style="{width:width+'px',height:height+'px'}">
    <div class="content">
      <h3>PaddlePaddle</h3>
      <P>遥感图像智能解译系统</P>
      <div class="tag">
        <span @click="setIndex(0)" :class="{selected:curIndex===0}">登录</span>
        <span @click="setIndex(1)" :class="{selected:curIndex===1}">注册</span>
      </div>
      <div class="formBox" v-show="curIndex===0">
        <input ref="lPhone" type="text" placeholder="电话" @blur="judgeLPhone"/>
        <input ref="lPassword" type="password" placeholder="密码" @blur="judgeLPwd"/>
        <div style="display: flex;text-align: center;justify-content: center;">
          <el-checkbox style="margin-right: 9rem;" v-model="checked">记住我</el-checkbox>
          <el-link @click="dialogFormVisible = true">忘记密码</el-link>
        </div>
        <button @click="login">登录</button>
      </div>
      <div class="formBox" v-show="curIndex===1">
        <input ref="rUsername" type="text" placeholder="姓名" @blur="judgeRName"/>
        <input ref="rPhone" type="text" placeholder="联系电话" @blur="judgeRPhone"/>
        <input ref="rEmail" type="text" placeholder="邮箱" @blur="judgeREmail"/>
        <input ref="rPassword" type="password" placeholder="密码" @blur="judgeRPwd"/>
        <input ref="rPasswordConfirm" type="password" placeholder="密码确认" @blur="judgeRPwdConfirm"/>
        <button @click="register">注册</button>
      </div>
    </div>
    <el-dialog title="密码重置" :visible.sync="dialogFormVisible" width="500px">
      <el-form :model="form">
        <el-form-item label="电话:" :label-width="formLabelWidth">
          <el-input type="text" v-model="form.phone" ref="fPhone" @blur="judgeUPhone"></el-input>
        </el-form-item>
        <el-form-item label="新密码:" :label-width="formLabelWidth">
          <el-input type="password" v-model="form.pwd" ref="fPwd" @blur="judgeUPwd"></el-input>
        </el-form-item>
        <el-form-item label="确认密码:" :label-width="formLabelWidth">
          <el-input type="password" v-model="form.pwdConfirm" ref="fPwdConfirm" @blur="judgeUPwdConfirm"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="updatePwd">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {mapMutations, mapState} from 'vuex'
import {checkEmail, checkMobile, getClientSize, setCookie, getCookie, clearCookie} from '../../util/util';
import {login, register, updatePwd} from '../../api/client';

export default {
  name: 'Login',
  computed: {
    ...mapState([
      'clientId',
      'clientName',
      'clientPhone',
      'clientEmail'
    ]),
    width() {
      return getClientSize().width;
    },
    height() {
      return getClientSize().height;
    },
  },
  data() {
    return {
      curIndex: 0,
      checked: false,

      dialogFormVisible: false,
      form: {
        phone: '',
        pwd: '',
        pwdConfirm: ''
      },
      formLabelWidth: '75px'
    }
  },
  methods: {
    ...mapMutations({
      setClientId: 'SET_CLIENT_ID',
      setClientName: 'SET_CLIENT_NAME',
      setClientPhone: 'SET_CLIENT_PHONE',
      setClientEmail: 'SET_CLIENT_EMAIL',
      clientLogout: 'CLIENT_LOGOUT'
    }),
    setIndex(index) {
      if (index === this.curIndex) {
        return;
      }
      this.curIndex = index;
    },
    //输入判断
    warnInfo(message) {
      this.$message({
        message: message,
        type: 'warning'
      });
      return false;
    },
    successInfo(message) {
      this.$message({
        message: message,
        type: 'success'
      });
      return true;
    },
    judgeLPhone() {
      if (this.$refs.lPhone.value.trim() == '') {
        return this.warnInfo('电话不能为空！');
      }
      if (checkMobile(this.$refs.lPhone.value.trim()) == false) {
        return this.warnInfo('电话不符合要求！');
      }
      return true;
    },
    judgeLPwd() {
      if (this.$refs.lPassword.value.trim() == '') {
        return this.warnInfo('密码不能为空！');
      }
      return true;
    },
    judgeRName() {
      if (this.$refs.rUsername.value.trim() == '') {
        return this.warnInfo('姓名不能为空！');
      }
      return true;
    },
    judgeRPhone() {
      if (this.$refs.rPhone.value.trim() == '') {
        return this.warnInfo('电话不能为空！');
      }
      if (checkMobile(this.$refs.rPhone.value.trim()) == false) {
        return this.warnInfo('电话不符合要求！');
      }
      return true;
    },
    judgeREmail() {
      if (this.$refs.rEmail.value.trim() == '') {
        return this.warnInfo('邮箱不能为空！');
      }
      if (checkEmail(this.$refs.rEmail.value.trim()) == false) {
        return this.warnInfo('邮箱不符合要求！');
      }
      return true;
    },
    judgeRPwd() {
      if (this.$refs.rPassword.value.trim() == '') {
        return this.warnInfo('密码不能为空！');
      }
      return true;
    },
    judgeRPwdConfirm() {
      if (this.$refs.rPassword.value.trim() == '') {
        return this.warnInfo('密码确认不能为空！');
      }
      if (this.$refs.rPassword.value.trim() != this.$refs.rPasswordConfirm.value.trim()) {
        return this.warnInfo('密码和密码确认值不匹配！');
      }
      return true;
    },
    judgeUPhone() {
      if (this.form.phone.trim() == '') {
        return this.warnInfo('电话不能为空！');
      }
      if (checkMobile(this.form.phone.trim()) == false) {
        return this.warnInfo('电话不符合要求！');
      }
      return true;
    },
    judgeUPwd() {
      if (this.form.pwd.trim() == '') {
        return this.warnInfo('密码不能为空！');
      }
      return true;
    },
    judgeUPwdConfirm() {
      if (this.form.pwdConfirm.trim() == '') {
        return this.warnInfo('密码确认不能为空！');
      }
      if (this.form.pwd.trim() != this.form.pwdConfirm.trim()) {
        return this.warnInfo('密码和密码确认值不匹配！');
      }
      return true;
    },

    login() {
      if (this.judgeLPhone() == false) {
        this.$refs.lPhone.focus();
        return;
      }
      if (this.judgeLPwd() == false) {
        this.$refs.lPassword.focus();
        return;
      }
      const res = login({
        phone: this.$refs.lPhone.value.trim(),
        password: this.$md5(this.$refs.lPassword.value.trim())
      });
      res.then((data) => {
        this.setClientId(data.id);
        this.setClientName(data.username);
        this.setClientPhone(data.phone);
        this.setClientEmail(data.email);
        if (this.checked) {
          setCookie(this.$refs.lPhone.value.trim(), this.$refs.lPassword.value.trim(), 3)
        } else {
          setCookie('', '', -1)
        }
        this.$router.push('/backstage');
      }).catch((e) => {
        this.$message({
          message: e.toString(),
          type: 'error'
        });
      })
    },
    register() {
      if (this.judgeRName() == false) {
        this.$refs.rUsername.focus();
        return;
      }
      if (this.judgeRPhone() == false) {
        this.$refs.rPhone.focus();
        return;
      }
      if (this.judgeREmail() == false) {
        this.$refs.rEmail.focus();
        return;
      }
      if (this.judgeRPwd() == false) {
        this.$refs.rPassword.focus();
        return;
      }
      if (this.judgeRPwdConfirm() == false) {
        this.$refs.rPasswordConfirm.focus();
        return;
      }
      const res = register({
        username: this.$refs.rUsername.value.trim(),
        phone: this.$refs.rPhone.value.trim(),
        email: this.$refs.rEmail.value.trim(),
        password: this.$md5(this.$refs.rPassword.value.trim()),
      });
      res.then((data) => {
        console.log(data);
        this.successInfo(data);
        this.curIndex = 0;
        this.$refs.lPhone.value = this.$refs.rPhone.value;
        this.$refs.rUsername.value = '';
        this.$refs.rPhone.value = '';
        this.$refs.rEmail.value = '';
        this.$refs.rPassword.value = '';
        this.$refs.rPasswordConfirm.value = '';
      }).catch((e) => {
        this.$message({
          message: e.toString(),
          type: 'error'
        });
      })
    },
    updatePwd() {
      if (this.judgeUPhone() == false) {
        this.$refs.fPhone.focus();
        return;
      }
      if (this.judgeUPwd() == false) {
        this.$refs.fPwd.focus();
        return;
      }
      if (this.judgeUPwdConfirm() == false) {
        this.$refs.fPwdConfirm.focus();
        return;
      }
      const res = updatePwd({
        phone: this.form.phone.trim(),
        password: this.$md5(this.form.pwd.trim()),
      });
      res.then((data) => {
        console.log(data);
        this.successInfo(data);
        this.curIndex = 0;
        this.$refs.lPhone.value = this.form.phone;
        this.dialogFormVisible = false;
      }).catch((e) => {
        this.$message({
          message: e.toString(),
          type: 'error'
        });
      })
    },
  },
  mounted() {
    let data = getCookie()
    if (data.phone != '' && data.pwd != '') {
      this.$router.push('/backstage');
    } else {
      this.clientLogout();
    }
  }
}
</script>

<style scoped lang="less">
@import "../../assets/css/var.less";

input:focus { //获取焦点
  outline: 1px solid #51c9ff; //边框不用border，用outline
  background: rgba(3, 16, 28, 0); //背景色
}

.Login {
  background-color: @bgColor;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  .content {
    width: 350px;
    position: absolute;
    //top: 50%;
    //left: 50%;
    //margin-top: -260px;
    //margin-left: -150px;
    text-align: center;
    overflow: hidden;

    h3 {
      color: @secondColor;
      font-size: 50px;
    }

    p {
      margin-top: 20px;
      color: @fontDefaultColor;
      margin-bottom: 20px;
    }

    .tag {
      margin-top: 20px;
      color: @fontDefaultColor;
      margin-bottom: 20px;

      span {
        display: inline-block;
        width: 50px;
        text-align: center;
        margin: 0 10px;
        padding: 10px 0;
        cursor: pointer;
      }

      .selected {
        border-bottom: 2px solid @secondColor;
        color: @secondColor
      }
    }

    input {
      border-radius: 7px;
      box-shadow: none;
      background: #fff;
      padding: 14px;
      width: 85%;
      border: 1px solid @borderColor;
      margin-bottom: 10px;
    }

    button {
      width: 90%;
      background: @secondColor;
      box-shadow: none;
      border: 0;
      border-radius: 3px;
      line-height: 41px;
      color: #fff;
      cursor: pointer;
      margin-top: 20px;
    }
  }
}
</style>
