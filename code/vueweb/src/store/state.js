import {getLocalItem} from '../util/util';

const state = {
    // //管理员后台管理
    // adminId:getLocalItem('adminId')?getLocalItem('adminId'):'',
    // adminName:getLocalItem('adminName')?getLocalItem('adminName'):'',
    // adminToken:getLocalItem('adminToken')?getLocalItem('adminToken'):null,

    //客户
    clientId: getLocalItem('clientId') ? getLocalItem('clientId') : '',
    clientName: getLocalItem('clientName') ? getLocalItem('clientName') : '',
    clientPhone: getLocalItem('clientPhone') ? getLocalItem('clientPhone') : '',
    clientEmail: getLocalItem('clientEmail') ? getLocalItem('clientEmail') : '',
}

export default state;
