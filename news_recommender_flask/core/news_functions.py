from flask import Blueprint,request,jsonify
from utils.mysql_utils import mysql_utils
from db.news_sql import News_sql
from db.history_sql import History_sql
from datetime import datetime
from utils.recommend_news_list import get_recommend_news_list
from utils.summary_news import get_news_summary

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/api/category_news_list', methods=['GET'])
def public_news_display():
    '''
    根据用户兴趣获取展示的新闻
    :return:
    '''
    userId = request.args.get('user_id')
    lang = request.args.get('lang')

    new_mysql = mysql_utils()
    query_txt = News_sql.query_category_news(userId,lang)

    res = new_mysql.do_execute(query_txt)
    # print(res)
    return jsonify({"display_news_list": res})

@news_blueprint.route('/api/news_detail', methods=['GET'])
def news_detail_display():
    '''
    通过新闻ID查询新闻详情内容,查询表格为new_resulte
    :param: newID
    :return: 返回新闻内容详情
    '''
    id = request.args.get('new_id')
    userId = request.args.get('user_id')
    print(id,userId)
    # 数据库查询
    new_mysql = mysql_utils()
    query_txt = News_sql.query_by_id(int(id))
    news_detail = new_mysql.do_execute(query_txt,isSingle=True)

    # 添加用户的浏览记录
    # 获取当前时间并转换为字符串，格式为“年-月-日”
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    current_date_str

    #添加用户的历史浏览记录

    histroy_add_txt = History_sql.add_history_sql(id,userId,current_date_str)
    new_mysql.do_execute(histroy_add_txt,isSingle=True)

    return jsonify({"news_detail":news_detail})

@news_blueprint.route('/api/recommend_news_list', methods=['GET'])
def news_recommendation_list():
    '''
    获取用户的历史记录，并且按照浏览的时间从新往旧排序
    :return: 推荐的新闻列表
    '''
    # 获取当前的时间，用于增加用户的历史浏览记录
    userId = request.args.get('user_id')
    lang = request.args.get('lang')
    recommend_news_list = get_recommend_news_list(userId,lang)
    if recommend_news_list:
        return jsonify({"news_recommend_list": recommend_news_list})
    else:
        return jsonify({"error": "No recommend content!"})


@news_blueprint.route('/api/news_summary', methods = ['GET'])
def news_summary():
    userId = request.args.get('user_id')
    lang = request.args.get('lang')
    newsId = request.args.get('news_id')

    if (newsId and userId and lang):
        # 获取新闻的摘要内容
        news_summary = get_news_summary(userId, lang, newsId)

    if news_summary:
        return jsonify({"news_summary": news_summary})
    else:
        return jsonify({"error": "No summary content!"})