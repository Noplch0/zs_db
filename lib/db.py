import pymysql
import hashlib

# 连接数据库

# 初始化游标

def init_cursor():

    return cursor

def command_db(command):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='regsys', autocommit=True)
    cursor = db.cursor()
    cursor.execute(command)
    db.close()
    return cursor.fetchall()


def is_existed(username, passwd):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='regsys', autocommit=True)
    cursor = db.cursor()
    sql = 'select * from register where username = "%s" and password = "%s";' % (username, passwd)
    result = command_db(sql)
    if result:
        db.close()
        return True
    else:
        db.close()
        return False


def is_exist_user(username):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='regsys', autocommit=True)
    cursor = db.cursor()
    sql = 'select * from register where username = "%s";' % username
    result = command_db(sql)
    if result:
        db.close()
        return True
    else:
        db.close()
        return False


def get_md5(string):
    md = hashlib.md5()
    md.update(string.encode('utf-8'))
    return md.hexdigest()


def insert_data(table, value):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='finacedata', autocommit=True)
    cursor = db.cursor()
    table = table
    # 列的字段
    keys = ', '.join(value.keys())
    # 行字段
    values = ', '.join(str(v) for v in value.values())
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    cursor.execute(sql)
