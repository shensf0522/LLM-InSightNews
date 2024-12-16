from flask import Blueprint,request,jsonify
from utils.mysql_utils import mysql_utils
from db.preferences_sql import Preference_sql
from db.user_sql import User_sql

user_blueprint = Blueprint('user', __name__)

kind_lang_mapping_zh = {
    '经济': 'Economy',
    '房地产': 'Real estate',
    '教育':'Education',
    '科技':'Science and Technology',
    '娱乐':'Entertainment',
    '互联网':'Internet',
    '军事':'Military',
    '社会':'Social'
}

kind_lang_mapping_en = {value:key for key,value in kind_lang_mapping_zh.items()}

@user_blueprint.route('/api/user_regist', methods = ['POST'])
def register():
    '''
    对获取到的信息通过数据库查询，若该用户已经存在，则返回提示，否则进行用户注册
    :param:
    用户的注册信息：用户名，密码，pinah
    :return: 返回注册成功提示或者异常信息
    '''
    # 获取前端页面传递过来的数据
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    # 获取到勾选的偏好类别信息，类型为列表
    preferences_list = data['preferences']
    lang = data['lang']

    print(email, password, preferences_list, lang)

    # 检查数据是否为空
    if email == '' or password == '':
        return jsonify({"message":"注册失败，邮箱或密码为空"})
    new_mysql = mysql_utils()
    query_user_exist_txt = User_sql.query_user_exist_sql(email)
    res = new_mysql.do_execute(query_user_exist_txt, isSingle=True)
    if res['COUNT(email)'] != 0:
        return jsonify({"message": "用户已经存在，请登录"})
    else:
        registe_user_txt = User_sql.register_user_sql(username,email,password)
        register_id = new_mysql.do_execute(registe_user_txt)


        # 注册用户偏爱的类别信息
        for preferences in preferences_list:
            if lang == 'zh':
                preferences_eng = kind_lang_mapping_zh.get(preferences)
            else:
                preferences_eng = preferences
                preferences = kind_lang_mapping_en.get(preferences_eng)

            industries_add_text = Preference_sql.add_new_preference(preferences,register_id,preferences_eng)
            res = new_mysql.do_execute(industries_add_text)
    if res:
        return jsonify({"message": "True"})
    else:
        return jsonify({"message":"False"})

@user_blueprint.route('/api/login_check', methods=['POST'])
def login():
    '''
    用户登录验证
    :param
    username 用户名
    password 密码
    :return: 返回验证结果，True/False
    '''
    data = request.json
    email = data['email']
    password = data['password']
    print(email,password)
    if email == '' or password == '':
        return jsonify({"message": "登录失败，邮箱或密码为空"})

    # 从数据坤掉数据，进行验证
    new_mysql = mysql_utils()

    # 验证用户是否已经存在
    query_user_exist_txt = User_sql.query_user_exist_sql(email)
    res = new_mysql.do_execute(query_user_exist_txt,isSingle=True)
    if res['COUNT(email)'] == 0:
        return jsonify({"message":"用户不存在，请完成注册"})
    else:
        validate_user_login_sql = User_sql.validate_user_login_sql(email,password)
        res = new_mysql.do_execute(validate_user_login_sql,isSingle=True)
        # 根据用户的email，获取用户的id，查询用户的浏览偏好并且返回

        if res['COUNT(email)'] == 0:
            return jsonify({"message": "用户或密码错误，请重试!"})
        else:
            query_userId_txt = User_sql.query_userId_by_email(email)
            res = new_mysql.do_execute(query_userId_txt,isSingle=True)
            return jsonify({"userId": res.get('userId'), "message":"True"})