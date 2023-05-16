import json
import flask
from lib import db

app = flask.Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
