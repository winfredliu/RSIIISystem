import axios from '../config/axios-client';

//用户登录
export function login(data) {
    const res = axios.post('/api/client/login', data);
    return new Promise((resolve, reject) => {
        res.then((result) => {
            if (result.status === 200) {
                return result.data;
            } else {
                reject(result.status)
            }
        }).then((json) => {
            if (json.code === 0) {
                resolve(json.data);
            } else {
                reject(json.message);
            }
        }).catch((e) => {
            reject(e.toString())
        })
    })
}

//用户注册
export function register(data) {
    const res = axios.post('/api/client/register', data);
    return new Promise((resolve, reject) => {
        res.then((result) => {
            if (result.status === 200) {
                return result.data;
            } else {
                reject(result.status)
            }
        }).then((json) => {
            if (json.code === 0) {
                resolve(json.message);
            } else {
                reject(json.message);
            }
        }).catch((e) => {
            reject(e.toString())
        })
    })
}
//用户密码重置
export function updatePwd(data) {
    const res = axios.post('/api/client/updatePwd', data);
    return new Promise((resolve, reject) => {
        res.then((result) => {
            if (result.status === 200) {
                return result.data;
            } else {
                reject(result.status)
            }
        }).then((json) => {
            if (json.code === 0) {
                resolve(json.message);
            } else {
                reject(json.message);
            }
        }).catch((e) => {
            reject(e.toString())
        })
    })
}


//修改用户信息
export function update(data) {
    const res = axios.post('/api/client/update', data);
    return new Promise((resolve, reject) => {
        res.then((result) => {
            if (result.status === 200) {
                return result.data;
            } else {
                reject(result.status)
            }
        }).then((json) => {
            if (json.code === 0) {
                resolve(json.message);
            } else {
                reject(json.message);
            }
        }).catch((e) => {
            reject(e.toString())
        })
    })
}
