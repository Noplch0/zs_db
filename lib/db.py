import pymysql
import hashlib


def command_db(command):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='regsys', autocommit=True)
    cursor = db.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    db.close()
    return result


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


def insert_data(table, value):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='finacedata', autocommit=True)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 列的字段
    keys = ', '.join(value.keys())
    # 行字段
    values = ', '.join(str(v) for v in value.values())
    d_sql = 'delete from %s where code = %s' % (table, value['code'])
    cursor.execute(d_sql)
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result


def query(table, code):
    db = pymysql.connect(host='81.70.245.162', user='root', password='lkijnfgh', database='finacedata', autocommit=True,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = r"select * from %s where code = '%s'" % (table, code)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result
