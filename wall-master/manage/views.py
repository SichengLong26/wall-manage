from flask import render_template, flash, url_for, request, json, jsonify, Response
from werkzeug.utils import redirect
from manage import keywords
from manage import app, db
from manage.keywords import DFAFilter
from manage.models import Message,User
from manage.web_utils import validate_token, generate_token, login_required


# 过滤敏感词
gfw = DFAFilter()
gfw.parse('./manage/keywords.txt')

# 展示后台页面
@app.route('/admin/manage', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('manage.html', messages=messages)

# 展示前台页面
@app.route('/wall', methods=['GET'])
def wall():
    return render_template('wallPage.html')

# 前台的输入的内容、名字存入数据库
@app.route('/add', methods=['POST'])
@login_required
def add_message():
    token = request.cookies.get('token')
    data_ = validate_token(token,'login')
    if not data_:
        return jsonify(code=201,msg="需要登录")
    user = User.query.filter(User.uid==data_['uid']).first()
    if not user:
        return jsonify(code=201,msg="需要登录")
    
    data = request.get_data().decode()
    data = json.loads(data)
    # print("submit",data)
    message = Message(
        username=user.username,
        content=data["content"],
        fontSize=data["fontSize"],
        centerRelX=data["centerRelX"],
        centerRelY=data["centerRelY"],
        width=data["width"],
        height=data["height"],
        borderRadius=data["borderRadius"])
    db.session.add(message)
    db.session.commit()
    return jsonify(code=200, msg="success")

# 后台手动删除功能
@app.route('/delete/<int:message_id>', methods=['GET','POST']) 
def delete_message(message_id):
    message = Message.query.get(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Your note is deleted.')
    return redirect(url_for('index')) 

# 将数据库的数据展示到前台
@app.route('/getMessage', methods=["GET"])
def getMessage():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    
    data = []
    for m in messages:
        # dict = {}
        # dict.update({
        #     "username":m.username,
        #     "content":gfw.filter(m.content),
        #     "fontSize":m.fontSize,
        #     "offsetX":m.offsetX,
        #     "offsetY":m.offsetY,
        #     "centerRelX":m.centerRelX,
        #     "centerRelY":m.centerRelY,
        #     "width":m.width, 
        #     "height":m.height,
        #     "borderRadius":m.borderRadius,
        # })
        message = m.to_dict()
        message['content'] = gfw.filter(m.content)
        data.append(message)
    print("测试：",data)
    return jsonify(code=200, data=data, msg="success")

# 注册用户信息存储
@app.route('/signUp',methods=['POST'])
def signUp():
    data = request.get_data().decode()
    data = json.loads(data)
    # print(data)
    phone = data["phone"]
    username = data["username"]
    password = data["password"]
    try:
        user = User(username=username,phone=phone,password=password)
        db.session.add(user)
        db.session.commit()
    except Exception:
        return jsonify(code=201, msg="已存在用户")
    return jsonify(code=200, msg="注册成功") 

@app.route('/signIn',methods=["POST"])
def signIn():
    data = request.get_data().decode()
    data = json.loads(data)
    user = User.query.filter(User.username==data['username'],User.password==data['password']).first()
    if not user:
        return jsonify(code=201, msg="账号或密码错误")
    token = generate_token(user,'login')
    resp = Response()
    resp.data = "{\"code\":200,\"msg\":\"success\"}"
    resp.set_cookie("token",token)
    return resp

@app.route('/getUserInfo',methods=["GET"])
@login_required
def getUserInfo():
    token = request.cookies.get('token')
    data = validate_token(token,'login')
    user = User.query.filter(User.uid==data['uid']).first()
    if not user:
        return jsonify(code=201,msg="查询失败,请重新登录")
    info = user.to_dict()
    del info['password']
    return jsonify(code=200,data=info,msg='success')



# 返回用户使用条例页面
@app.route('/illustration',methods=['GET'])
def illustration():
    return render_template('illustration.html')

# 搜索用户发表的留言
@app.route('/search',methods=['GET','POST'])
def search():
    return render_template('result.html')

@app.route('/search_results',methods=['GET','POST'])
def search_results():
    content = request.form.get('content')
    if content is None:
        content = " "
    results = Message.query.filter(Message.username == content).all()
    return render_template('result.html',results=results)