import axios from 'axios'
import store from '../store'
import * as types from '../store/mutation-types'
import router from '../router/index'

// axios 配置
// axios.defaults.timeout = 5000;
axios.defaults.baseURL = '';
// axios.defaults.baseURL = 'http://localhost:3000';
// axios.defaults.baseURL = 'http://localhost:5000';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        if (store.state.clientId) {
            config.headers.Authorization = `Bearer ${store.state.clientId}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    }
);

// http response 拦截器
// axios.interceptors.response.use(
//     response => {
// if(response.data.data.TokenStates==false){
//     store.commit(types.CLIENT_LOGOUT);
//     router.replace({
//         path: 'login',
//         query: {redirect: router.currentRoute.fullPath}
//     });
// }
// else{
//     return response;
// }
// },
// error => {
//     if (error.response) {
//         console.log(error)
//         switch (error.response.status) {
//             case 401:
//                 // 401 清除token信息并跳转到登录页面
//                 store.commit(types.CLIENT_LOGOUT);
//                 router.replace({
//                     path: 'login',
//                     query: {redirect: router.currentRoute.fullPath}
//                 })
//         }
//     }
// console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
//     return Promise.reject(error.response.data)
// });

export default axios;
