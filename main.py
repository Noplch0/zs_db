import decimal
import json
import flask
from lib import db
from lib import get_data as gd
import os

app = flask.Flask(__name__)
userpath = "./data/users/"
datapath = "./data/inf/"


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
    print(username)
    print(pwd)
    print(email)
    if username and pwd:
        if os.path.exists("{userpath}{username}.json".format(username=username, userpath=userpath)):
            res = {'msg': '用户已存在'}
        else:
            userdict = {'username': username, 'password': pwd, 'email': email}
            with open("{userpath}{username}.json".format(username=username, userpath=userpath), 'w') as file:
                json.dump(userdict, file, cls=DecimalEncoder)
            res = {'msg': '注册成功'}
            res.update(userdict)
    else:
        res = {'msg': '必要字段未填'}
    return json.dumps(res, ensure_ascii=False)


# noinspection PyUnboundLocalVariable
@app.route('/login')
def login():
    username = flask.request.values.get('username')
    pwd = flask.request.values.get('passwd')
    if username and pwd and os.path.exists("{userpath}{username}.json".format(userpath=userpath, username=username)):
        with open("{userpath}{username}.json".format(username=username, userpath=userpath)) as file:
            userdict = json.load(file)
        if userdict.password == pwd:
            res = {'msg': '登录成功'}.update(userdict)
        else:
            res = {'msg': '密码错误'}
    elif not username or not pwd:
        res = {'msg': '必要字段未填'}
    elif not os.path.exists("{userpath}{username}.json".format(userpath=userpath, username=username)):
        res = {'msg': '用户不存在'}
    return json.dumps(res, ensure_ascii=False)


@app.route('/reset_passwd')
def reset_passwd():
    username = flask.request.values.get('username')
    origin_passwd = flask.request.values.get('origin_passwd')
    new_passwd = flask.request.values.get('new_passwd')
    if not os.path.exists("{userpath}{username}.json".format(userpath=userpath, username=username)):
        return {'msg': '用户不存在'}
    if username and origin_passwd and new_passwd:
        with open("{userpath}{username}.json".format(userpath=userpath, username=username), 'r') as file:
            userdict = json.load(file)
        if userdict['password'] == origin_passwd:
            userdict.update({'password': new_passwd})
            with open("{userpath}{username}.json".format(userpath=userpath, username=username), 'w') as file:
                json.dump(userdict, file, cls=DecimalEncoder)
            res = {'msg': '修改成功'}.update(userdict)
        else:
            res = {'msg': '修改失败'}
    else:
        res = {'msg': '必要字段未填'}
    return json.dumps(res, ensure_ascii=False)


@app.route('/get_data')
def get_data():
    code = flask.request.values.get('code')
    if not os.path.exists("{data}{code}.json".format(data=datapath, code=code)):
        return {'msg': '文件不存在'}
    else:
        with open("{data}{code}.json".format(data=datapath, code=code)) as file:
            data = json.load(file)
            return data


if __name__ == '__main__':
    app.run(port=5000, debug=True)
