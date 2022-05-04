# encoding:utf-8
import re

from flask import current_app, request, jsonify
from authlib.jose import jwt, JoseError

import functools
from manage.models import Message, User

def generate_token(user, operation, **kwargs):
    """生成用于邮箱验证的JWT（json web token）"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = current_app.config['SECRET_KEY']
    # 待签名的数据负载
    data = {'uid': user.uid, 'operation': operation}
    data.update(**kwargs)

    return jwt.encode(header=header, payload=data, key=key)


def validate_token(token, operation):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    if not token:
        return False
    key = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(token, key)
        # print(data)
    except JoseError:
        return False
    ... # 其他字段确认
    if data['operation'] != operation:
        return False
    return data

# def verify_token(token):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except Exception:
#         return None

#     # user = Teacher.query.get(data['id'])
#     try:
#         user = User.query.filter(User.uid==data['uid']).first()
#         if not user:
#             return False
#     except Exception:
#         return False

#     return user


def login_required(view_func):
    @functools.wraps(view_func)
    def verify(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.cookies.get('token')
        except Exception:
            # 没接收的到token,给前端抛出错误
            return jsonify(code=201, msg='token required')
            # return render_template('')

        s = validate_token(token,'login')
        if not s:
            return jsonify(code=202, url='/', msg="login require")
        # print(s)
        uid = s['uid']
        if not uid:
            return jsonify(code=202, url='/', msg='no access')

        return view_func(*args, **kwargs)

    return verify


def inputs_valid_check(inputs):
    if inputs is None:
        return False
    id = inputs["account"]
    password = inputs['password']
    if not all([id, password]):
        return False
    _id_s = re.match("[A-Z][a-z]", id)
    if _id_s or len(id) != 8:
        return False
    _id_n = re.match("[0-9]{8}", id)
    if len(_id_n.group()) != 8:
        return False
    if len(password)<6 or len(password)>20:
        return False
    _p = re.match("[a-zA-Z0-9_'@]{6,20}", password)
    if _p.group() != password:
        return False
    return True
