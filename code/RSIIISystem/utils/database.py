# 数据库连接配置
import pymysql
import logging

# 日志打印格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[%(funcName)s-->'
                           'line:%(lineno)d] - %(levelname)s: %(message)s')


# 连接数据库
def connectDatabase():
    # 数据库连接
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        database='paddleuser'
    )
    # 游标
    cur = conn.cursor()
    return cur, conn


# 关闭数据库
def closeDatabase(cur, conn):
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()


# ------------------------login
# 通过手机号查找用户
def findUserByPhone(phone):
    cur, conn = connectDatabase()
    sql = "select * from user where phone = '%s'" % (phone)
    cur.execute(sql)
    data = cur.fetchall()
    # 打印日志
    logging.info(data)
    closeDatabase(cur, conn)
    return data


# 通过id和密码查找用户
def findUserByIdAndPwd(uid, pwd):
    cur, conn = connectDatabase()
    sql = "select * from user where id = '%s' and password = '%s'" % (uid, pwd)
    cur.execute(sql)
    data = cur.fetchall()
    # 打印日志
    logging.info(data)
    closeDatabase(cur, conn)
    return data


# 通过电话和密码查找用户
def findUserByPhoneAndPwd(phone, pwd):
    cur, conn = connectDatabase()
    sql = "select * from user where phone = '%s' and password = '%s'" % (phone, pwd)
    cur.execute(sql)
    data = cur.fetchall()
    # 打印日志
    logging.info(data)
    closeDatabase(cur, conn)
    return data


# 通过邮箱和密码查找用户
def findUserByEmailAndPwd(email, pwd):
    cur, conn = connectDatabase()
    sql = "select * from user where email ='%s' and password ='%s'" % (email, pwd)
    cur.execute(sql)
    data = cur.fetchall()
    # 打印日志
    logging.info(data)
    closeDatabase(cur, conn)
    return data


# 添加用户
def addUser(username, password, email, phone):
    cur, conn = connectDatabase()
    sql = "insert into user(username,phone,email,password) values ('%s','%s','%s','%s')" % (
        username, password, email, phone)
    num = cur.execute(sql)
    conn.commit()  # 对数据库内容有改变，需要commit()
    closeDatabase(cur, conn)
    return num


# 修改密码
def updatePassword(phone, newPwd):
    data = findUserByPhone(phone)
    if len(data) == 0:
        print("用户不存在")
        return -1
    else:
        print("可以更改")
        cur, conn = connectDatabase()
        sql = "update user set password='%s' where phone='%s'" % (newPwd, phone)
        num = cur.execute(sql)
        conn.commit()  # 对数据库内容有改变，需要commit()
        closeDatabase(cur, conn)
        return num


# 修改用户信息
def updateUser(uid, username, phone, email, oldPwd, newPwd):
    data = findUserByIdAndPwd(uid, oldPwd)
    if len(data) == 0:
        print("密码错误")
        return -1
    else:
        print("可以更改")
        cur, conn = connectDatabase()
        sql = "update user set username='%s',phone='%s',email='%s',password='%s' where id='%s'" % (
            username, phone, email, newPwd, uid)
        num = cur.execute(sql)
        conn.commit()  # 对数据库内容有改变，需要commit()
        closeDatabase(cur, conn)
        return num
