<template>
  <div id="EditInfo">
    <div style="height:479px;background-color:#f2f2f2;border-radius: 15px;padding: 35px">
      <header style="text-align: center">
        <span>信息修改</span>
      </header>
      <div class="content">
        <div class="inputBox">
          <span>姓名：</span>
          <TextInput placeholder="请输入姓名" v-model="username" :initText="username" id="username"/>
        </div>
        <div class="inputBox">
          <span>电话：</span>
          <TextInput placeholder="请输入phone" v-model="phone" :initText="phone" id="phone"/>
        </div>
        <div class="inputBox">
          <span>邮箱：</span>
          <TextInput placeholder="请输入邮箱" v-model="email" :initText="email" id="=email"/>
        </div>
        <div class="inputBox">
          <span>原密码：</span>
          <TextInput placeholder="请输入原密码" v-model="oldPwd" type="password" id="oldPwd"/>
        </div>
        <div class="inputBox">
          <span>新密码：</span>
          <TextInput placeholder="请输入新密码" v-model="newPwd" type="password" id="newPwd"/>
        </div>
        <div class="inputBox">
          <span>确认新密码：</span>
          <TextInput placeholder="请再输入一次新密码" v-model="confirmPwd" type="password" id="confirmPwd"/>
        </div>
        <button @click="confirmChange">确认修改</button>
      </div>
    </div>
  </div>
</template>

<script>
import TextInput from '../../components/TextInput';
import {mapState, mapMutations} from 'vuex';
import {update} from "../../api/client";
import {checkEmail, checkMobile} from "../../util/util";

export default {
  name: 'EditInfo',
  components: {
    TextInput
  },
  computed: {
    ...mapState([
      'clientId',
      'clientName',
      'clientPhone',
      'clientEmail'
    ]),
  },
  data() {
    return {
      username: '',
      phone: '',
      email: '',
      oldPwd: '',
      newPwd: '',
      confirmPwd: ''
    }
  },
  created: function () {
    document.title = "信息修改";
  },
  methods: {
    ...mapMutations({
      clientLogout: 'CLIENT_LOGOUT',
    }),
    //错误提示
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
    judgeName() {
      if (this.username.trim() == '') {
        return this.warnInfo('姓名不能为空！');
      }
      return true;
    },
    judgePhone() {
      if (this.phone.trim() == '') {
        return this.warnInfo('电话不能为空！');
      }
      if (checkMobile(this.phone.trim()) == false) {
        return this.warnInfo('电话不符合要求！');
      }
      return true;
    },
    judgeEmail() {
      if (this.email.trim() == '') {
        return this.warnInfo('邮箱不能为空！');
      }
      if (checkEmail(this.email.trim()) == false) {
        return this.warnInfo('邮箱不符合要求！');
      }
      return true;
    },
    judgeOldPwd() {
      if (this.oldPwd.trim() == '') {
        return this.warnInfo('原密码不能为空！');
      }
      return true;
    },
    judgeNewPwd() {
      if (this.newPwd.trim() == '') {
        return this.warnInfo('新密码不能为空！');
      }
      return true;
    },
    judgeNewPwdConfirm() {
      if (this.confirmPwd.trim() == '') {
        return this.warnInfo('新密码确认不能为空！');
      }
      if (this.newPwd.trim() != this.confirmPwd.trim()) {
        return this.warnInfo('新密码和新密码确认值不匹配！');
      }
      return true;
    },
    confirmChange() {
      if (this.judgeName() == false) {
        document.getElementById("username").focus();
        return;
      }
      if (this.judgePhone() == false) {
        document.getElementById("phone").focus();
        return;
      }
      if (this.judgeEmail() == false) {
        document.getElementById("email").focus();
        return;
      }
      if (this.judgeOldPwd() == false) {
        document.getElementById("oldPwd").focus();
        return;
      }
      if (this.judgeNewPwd() == false) {
        document.getElementById("newPwd").focus();
        return;
      }
      if (this.judgeNewPwdConfirm() == false) {
        document.getElementById("confirmPwd").focus();
        return;
      }
      const uid = this.clientId;
      const username = this.username.trim();
      const phone = this.phone.trim();
      const email = this.email.trim();
      const oldPwd = this.$md5(this.oldPwd.trim());
      const newPwd = this.$md5(this.newPwd.trim());
      const res = update({
        uid,
        username,
        phone,
        email,
        oldPwd,
        newPwd
      });
      res.then((res) => {
        this.oldPwd = '';
        this.newPwd = '';
        this.confirmPwd = '';
        console.log(res);
        this.successInfo(res);
        this.clientLogout();
        this.$router.push('/login');
      }).catch((e) => {
        this.$message({
          message: e.toString(),
          type: 'error'
        });
      })
    }
  },

  mounted() {
    this.username = this.clientName;
    this.phone = this.clientPhone;
    this.email = this.clientEmail;
  }
}
</script>

<style scoped lang="less">
@import "../../assets/css/var.less";

input:focus { //获取焦点
  outline: 1px solid #51c9ff; //边框不用border，用outline
  background: rgba(3, 16, 28, 0); //背景色
}

#EditInfo {
  display: flex;
  header {
    width: 100%;
    height: 40px;
    line-height: 40px;
  }
  .content {
    margin-top: 20px;
    width: 290px;
    text-align: center;

    .inputBox {
      text-align: left;
      margin-bottom: 20px;

      span {
        color: @fontDefaultColor;
        font-size: 13px;
        display: inline-block;
        width: 90px;
      }

      input {
      }
    }

    button {
      background-color: #337da4;
      color: white;
      border: none;
      width: 80px;
      height: 30px;
      border-radius: 5px;
      cursor: pointer;
    }
  }
}
@media screen and (min-width: 500px){
  #EditInfo{
    justify-content: center; //内容水平居中
  }
}
@media screen and (min-height: 520px){
  #EditInfo{
    align-items: center; //内容垂直居中
  }
}
</style>
