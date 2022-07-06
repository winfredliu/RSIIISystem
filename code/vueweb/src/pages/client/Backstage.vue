<template>
  <div class="Backstage" :style="{width:width+'px',height:height+'px'}">
    <div class="bsLeft" style="float: left">
      <div class="logo">{{ clientName }}</div>
      <ul :style="{height:(height-70)+'px'}">
        <li @click="navTo('/backstage/changeDetection')" :class="{selected:curPath==='/backstage/changeDetection'}">
          变化检测
        </li>
        <li @click="navTo('/backstage/groundObjectsClassification')"
            :class="{selected:curPath==='/backstage/groundObjectsClassification'}">地物分类
        </li>
        <li @click="navTo('/backstage/objectDetection')" :class="{selected:curPath==='/backstage/objectDetection'}">
          目标检测
        </li>
        <li @click="navTo('/backstage/targetExtraction')" :class="{selected:curPath==='/backstage/targetExtraction'}">
          目标提取
        </li>
        <li @click="navTo('/backstage/editInfo')" :class="{selected:curPath==='/backstage/editInfo'}">信息修改</li>
      </ul>
    </div>
    <div class="bsRight">
      <div class="header">
        <div class="title">遥感图像智能解译系统</div>
        <div class="userInfo" @mouseover="showUserTips" @mouseout="closeUserTips">
          欢迎您,
          <span @mouseover="showUserTips" @mouseout="closeUserTips">{{ clientName }}</span>
          <ul class="userTips" @mouseover="showUserTips" @mouseout="closeUserTips" v-show="userTipsShow">
            <li @click="navTo('/backstage/editInfo')">信息修改</li>
            <li @click="logout">退出</li>
          </ul>
        </div>
      </div>
      <transition name="router-fade" mode="out-in">
        <keep-alive>
          <router-view
              :style="{height:(height-70)+'px',overflowY:'scroll',width:'100%',padding:'20px',backgroundColor:'#f6f5fa'}">
          </router-view>
        </keep-alive>
      </transition>
    </div>
  </div>
</template>

<script>
import {mapState, mapMutations} from 'vuex';
import {clearCookie, getClientSize, getCookie} from '../../util/util';

export default {
  name: 'Backstage',
  data() {
    return {
      userTipsShow: false,
      curPath: this.$route.path
    }
  },
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
  methods: {
    ...mapMutations({
      clientLogout: 'CLIENT_LOGOUT'
    }),
    showUserTips() {
      this.userTipsShow = true;
    },
    closeUserTips() {
      this.userTipsShow = false;
    },
    navTo(route) {
      if (this.curPath === route) {
        return;
      }
      this.$router.push(route)
    },
    logout() {
      this.clientLogout();
      this.$router.push('/login');
      clearCookie();
    }
  },
  watch: {
    '$route'(to, from) {
      this.curPath = to.path;
    }
  },
  mounted() {
    // //关闭页面前清楚数据
    // let _this = this;
    // window.onbeforeunload = function (e) {
    //   _this.clientLogout();
    // }
  }
}
</script>

<style scoped lang="less">
@import "../../assets/css/var.less";

.Backstage {
  overflow: hidden;

  .bsLeft {
    width: 15%;
    height: 100%;
    display: inline-block;
    overflow: hidden;
    user-select: none;

    .logo {
      width: 100%;
      height: 70px;
      background-color: @mainColor;
      color: white;
      font-size: 25px;
      overflow: hidden;
      text-align: center;
      line-height: 70px;
    }

    ul {
      width: 100%;
      background-color: #313541;

      li {
        width: 100%;
        color: @fontDefaultColor;
        height: 45px;
        line-height: 45px;
        cursor: pointer;
        padding: 0 20px;
      }

      .selected {
        background-color: #272a34;
        color: white;
      }
    }
  }

  .bsRight {
    width: 85%;
    height: 100%;
    display: inline-block;
    overflow: hidden;

    .header {
      width: 100%;
      height: 70px;
      border-bottom: 1px solid @borderColor;
      position: relative;
      user-select: none;

      .title {
        line-height: 70px;
        font-size: 23px;
        position: absolute;
        left: 10px;
        vertical-align: middle;
        color: @fontDefaultColor;
      }

      .userInfo {
        line-height: 70px;
        position: absolute;
        right: 10px;
        font-size: 14px;
        z-index: 1;

        i {
        }

        span {
          cursor: pointer;
        }

        .userTips {
          position: absolute;
          top: 45px;
          right: 0;
          width: 66px;
          cursor: pointer;
          border: 1px solid @borderColor;
          background-color: white;

          li {
            width: 100%;
            height: 30px;
            text-align: center;
            line-height: 30px;
            border-bottom: 1px solid @borderColor;
          }
        }
      }
    }
  }
}
</style>
