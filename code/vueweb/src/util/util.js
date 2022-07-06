//获取屏幕宽高
export function getClientSize() {
    let h = document.documentElement.clientHeight || document.body.clientHeight;
    let w = document.documentElement.clientWidth || document.body.clientWidth;
    return {
        width: w,
        height: h
    }
}

//获取滚动条宽度
export function getScrollWidth() {
    let noScroll, scroll, oDiv = document.createElement("DIV");
    oDiv.style.cssText = "position:absolute; top:-1000px; width:100px; height:100px; overflow:hidden;";
    noScroll = document.body.appendChild(oDiv).clientWidth;
    oDiv.style.overflowY = "scroll";
    scroll = oDiv.clientWidth;
    document.body.removeChild(oDiv);
    return noScroll - scroll;
}

//回到顶部
export function backToTop() {
    let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    if (scrollTop > 0) {
        window.requestAnimationFrame(backToTop);
        window.scrollTo(0, scrollTop - (scrollTop / 5));
    }
}

//取本地储存数据
export function getLocalItem(key) {
    let value;
    try {
        value = localStorage.getItem(key);
    } catch (ex) {
        // 开发环境下提示error
        if (__DEV__) {
            console.error('localStorage.getItem报错, ', ex.message);
        }
    } finally {
        return value;
    }
}

//设置本地储存数据
export function setLocalItem(key, value) {
    try {
        // ios safari 无痕模式下，直接使用 localStorage.setItem 会报错
        localStorage.setItem(key, value);
    } catch (ex) {
        // 开发环境下提示 error
        if (__DEV__) {
            console.error('localStorage.setItem报错, ', ex.message);
        }
    }
}

//取会话储存数据
export function getSessionItem(key) {
    let value;
    try {
        value = sessionStorage.getItem(key);
    } catch (ex) {
        // 开发环境下提示error
        if (__DEV__) {
            console.error('sessionStorage.getItem报错, ', ex.message);
        }
    } finally {
        return value;
    }
}

//设置会话储存数据
export function setSessionItem(key, value) {
    try {
        // ios safari 无痕模式下，直接使用 sessionStorage.setItem 会报错
        sessionStorage.setItem(key, value);
    } catch (ex) {
        // 开发环境下提示 error
        if (__DEV__) {
            console.error('sessionStorage.setItem报错, ', ex.message);
        }
    }
}

//Unicode转中文汉字
export function decode(str) {
    str = str.replace(/(\\u)(\w{1,4})/gi, function ($0) {
        return (String.fromCharCode(parseInt((escape($0).replace(/(%5Cu)(\w{1,4})/g, "$2")), 16)));
    });
    str = str.replace(/(&#x)(\w{1,4});/gi, function ($0) {
        return String.fromCharCode(parseInt(escape($0).replace(/(%26%23x)(\w{1,4})(%3B)/g, "$2"), 16));
    });
    str = str.replace(/(&#)(\d{1,6});/gi, function ($0) {
        return String.fromCharCode(parseInt(escape($0).replace(/(%26%23)(\d{1,6})(%3B)/g, "$2")));
    });

    return str;
}

//转化为00:00时间格式
export function convertTime(seconds) {
    return [
        parseInt(seconds / 60 % 60),
        parseInt(seconds % 60)
    ].join(":").replace(/\b(\d)\b/g, "0$1");
}

export function shuffle(arr) {
    for (let i = arr.length - 1; i >= 0; i--) {
        let randomIndex = Math.floor(Math.random() * (i + 1));
        let itemAtIndex = arr[randomIndex];
        arr[randomIndex] = arr[i];
        arr[i] = itemAtIndex;
    }
    return arr;
}

//时间转换
export function convertDate(date) {
    let sign1 = "-";
    let sign2 = ":";
    let year = date.getFullYear() // 年
    let month = date.getMonth() + 1; // 月
    let day = date.getDate(); // 日
    let hour = date.getHours(); // 时
    let minutes = date.getMinutes(); // 分
    let seconds = date.getSeconds() //秒
    // 给一位数数据前面加 “0”
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (day >= 0 && day <= 9) {
        day = "0" + day;
    }
    if (hour >= 0 && hour <= 9) {
        hour = "0" + hour;
    }
    if (minutes >= 0 && minutes <= 9) {
        minutes = "0" + minutes;
    }
    if (seconds >= 0 && seconds <= 9) {
        seconds = "0" + seconds;
    }
    let newdate = year + sign1 + month + sign1 + day + " " +
        hour + sign2 + minutes + sign2 + seconds;
    return newdate;
}

// 获得目标文件的url
export function getFileURL(file) {
    let url = null;
    if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
    } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}

//获取文件后缀名
export function getFileSuffix(file) {
    try {
        let tmpArr = file.name.split('.');
        return tmpArr[tmpArr.length - 1];
    } catch (err) {
        return '';
    }
}

//获取文件大小 单位:MB
export function getFileSize(file) {
    return file.size / (1024 * 1024)
}

//获取url中的文件名
export function getUrlName(url) {
    try {
        let tmpArr = url.split('/');
        return tmpArr[tmpArr.length - 1];
    } catch (err) {
        return '';
    }
}

//验证邮箱的规则
export function checkEmail(value) {
    const regEmail = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    if (regEmail.test(value)) {
        //合法的邮箱
        return true;
    } else {
        return false;
    }
}

//验证手机号码的规则
export function checkMobile(value) {
    const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
    if (regMobile.test(value)) {
        //合法的手机号码
        return true;
    } else {
        return false;
    }
}

//生成一个随机的ID
export function GenNonDuplicateID() {
    return Math.random().toString(36).substr(3)
}


//设置cookie
export function setCookie(c_phone, c_pwd, exdays) {
    let exdate = new Date(); //获取当前时间
    exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); //保存的天数
    //字符串拼接cookie
    // console.log(window.document.cookie, c_phone)
    // console.log(window.document.cookie, c_phone, c_pwd)
    window.document.cookie =
        "userPhone" + "=" + c_phone + ";path=/;expires=" + exdate.toGMTString();
    window.document.cookie =
        "userPwd" + "=" + c_pwd + ";path=/;expires=" + exdate.toGMTString();
    //注意：";path=/;expires=" + exdate.toGMTString()"这个是给你设置的变量增加保存时间的，别忘了加
}

//获取cookie
export function getCookie() {
    let data = {phone: '', pwd: ''}
    if (document.cookie.length > 0) {
        let arr = document.cookie.split(";"); //这里显示的格式需要切割一下下
        for (let i = 0; i < arr.length; i++) {
            let arr2 = arr[i].split("="); //再次切割
            // console.log(arr2[0].trim(), arr2[1].trim());
            //判断查找相对应的值
            if (arr2[0].trim() == 'userPhone') {
                data.phone = arr2[1]; //获取用户电话到登录页面
            } else if (arr2[0].trim() == 'userPwd') {
                data.pwd = arr2[1];
            }
        }
    }
    return data
}

//清除cookie
export function clearCookie() {
    setCookie("", -1); //修改其他值都为空，天数为负1天
}
