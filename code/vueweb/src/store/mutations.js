import * as types from './mutation-types';
import {setLocalItem} from '../util/util';
import {SET_CLIENT_PHONE} from "./mutation-types";

const mutations = {
    // // 管理员
    // [types.SET_ADMIN_ID]: (state, adminId) => {
    //   state.adminId = adminId;
    //   setLocalItem('adminId', adminId);
    // },
    // [types.SET_ADMIN_NAME]: (state, adminName) => {
    //   state.adminName = adminName;
    //   setLocalItem('adminName', adminName);
    // },
    // [types.SET_ADMIN_TOKEN]: (state, adminToken) => {
    //   state.adminToken = adminToken;
    //   setLocalItem('adminToken', adminToken);
    // },
    // [types.ADMIN_LOGOUT]: (state) => {
    //   state.adminId='';
    //   state.adminName = '';
    //   state.adminToken = null;
    //   localStorage.removeItem('adminId');
    //   localStorage.removeItem('adminName');
    //   localStorage.removeItem('adminToken');
    // },

    //客户
    [types.SET_CLIENT_ID]: (state, clientId) => {
        state.clientId = clientId;
        setLocalItem('clientId', clientId);
    },
    [types.SET_CLIENT_NAME]: (state, clientName) => {
        state.clientName = clientName;
        setLocalItem('clientName', clientName);
    },
    [types.SET_CLIENT_PHONE]: (state, clientPhone) => {
        state.clientPhone = clientPhone;
        setLocalItem('clientPhone', clientPhone);
    },
    [types.SET_CLIENT_EMAIL]: (state, clientEmail) => {
        state.clientEmail = clientEmail;
        setLocalItem('clientEmail', clientEmail);
    },
    [types.CLIENT_LOGOUT]: (state) => {
        state.clientId = '';
        state.clientName = '';
        state.clientPhone = '';
        state.clientEmail = '';
        localStorage.removeItem('clientId');
        localStorage.removeItem('clientName');
        localStorage.removeItem('clientPhone');
        localStorage.removeItem('clientEmail');
    },
}
export default mutations;
