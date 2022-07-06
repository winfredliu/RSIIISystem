import 'babel-polyfill';
import Vue from 'vue';
import App from './App';
import router from './router/index';
import store from './store';
import './assets/css/common.less';
import './assets/font/iconfont.css';

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI);

import echarts from "echarts"
Vue.prototype.$echarts = echarts

import md5 from 'js-md5';
Vue.prototype.$md5 = md5;

Vue.config.productionTip = false;
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
});
