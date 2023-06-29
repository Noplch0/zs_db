import decimal
import json
import flask
from lib import db
from lib import get_data as gd

app = flask.Flask(__name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


@app.route('/reg')
def index():
    username = flask.request.values.get('username')
    pwd = flask.request.values.get('passwd')
    email = flask.request.values.get('email')
    linecount = db.command_db('SELECT COUNT(*) FROM register ;')
    print(linecount)
    if username and pwd:
        sql = 'select * from register where username = "%s";' % username
        if db.command_db(sql):
            res = {'msg': '用户已存在', 'msg_code': '0011'}
        else:
            password = db.get_md5(pwd)
            insert_sql = 'insert into register (username,password,ID,email) values ("%s","%s","%d","%s");' % (
                username, password, int(linecount[0][0]) + 1, email)
            db.command_db(insert_sql)
            res = {'msg': '注册成功', 'msg_code': '1010', 'reg_id': int(linecount[0][0]) + 1}
    else:
        res = {'msg': '必要字段未填', 'msg_code': '0012'}
    return json.dumps(res, ensure_ascii=False)


@app.route('/login')
def login():
    username = flask.request.values.get('username')
    pwd = flask.request.values.get('passwd')
    if username and pwd:
        password = db.get_md5(pwd)
        if db.is_existed(username, password):
            res = {'msg': '登录成功', 'msg_code': '1001'}
        elif db.is_exist_user(username):
            res = {'msg': '密码错误', 'msg_code': '0001'}
        elif not db.is_exist_user(username):
            res = {'msg': '用户不存在', 'msg_code': '0002'}
    else:
        res = {'msg': '必要字段未填', 'msg_code': '0003'}
    return json.dumps(res, ensure_ascii=False)


@app.route('/reset_passwd')
def reset_passwd():
    username = flask.request.values.get('username')
    origin_passwd = flask.request.values.get('origin_passwd')
    new_passwd = flask.request.values.get('new_passwd')
    if username and origin_passwd and new_passwd:
        o_passwd = db.get_md5(origin_passwd)
        n_passwd = db.get_md5(new_passwd)
        if db.is_existed(username, o_passwd):
            sql = 'update register set password="%s" where username = "%s"' % (n_passwd, username)
            if db.command_db(sql):
                res = {'msg': '修改成功', 'msg_code': '1020'}
        else:
            res = {'msg': '修改失败', 'msg_code': '0021'}
    return json.dumps(res, ensure_ascii=False)


@app.route('/get_data')
def get_data():
    table = flask.request.values.get('table')
    code = flask.request.values.get('code')
    if table == 'balancesheet':
        value = gd.get_balancesheet(code)
        db.insert_data(table, value)
    elif table == 'cashflow':
        value = gd.get_cashflow(code)
        db.insert_data(table, value)
    elif table == 'income_statement':
        value = gd.get_income_statement(code)
        db.insert_data(table, value)
    elif table == 'week_line':
        value = gd.get_weel_line(code)
        db.insert_data(table, value)
    result = db.query(table, code)
    print(value)
    print(result)
    if result:
        return json.dumps(result, ensure_ascii=False,cls=DecimalEncoder)
    else:
        res = {'msg': '查询失败', 'msg_code': '0031'}
        return json.dumps(res, ensure_ascii=False,cls=DecimalEncoder)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
