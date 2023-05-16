import pymysql
import hashlib

# 连接数据库

# 初始化游标
db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='reg_log', autocommit=True)
cursor = db.cursor()


def command_db(command):
    cursor.execute(command)
    return cursor.fetchall()


def is_existed(username, passwd):
    sql = 'select * from register where username = "%s" and password = "%s";' % (username, passwd)
    result = command_db(sql)
    if result:
        return True
    else:
        return False


def is_exist_user(username):
    sql = 'select * from register where username = "%s";' % username
    result = command_db(sql)
    if result:
        return True
    else:
        return False


def get_md5(string):
    md = hashlib.md5()
    md.update(string.encode('utf-8'))
    return md.hexdigest()
