import json
import os
import re
import datetime
import openpyxl
import pandas as pd
import pymysql
import requests


# 从sql平台拉数据
def pull_jira_data(sql, instanceName, dbName):
    requests.packages.urllib3.disable_warnings()
    #调试时忽略http访问时没有证书时等乱七八糟的告警信息
    urlLogin1 = 'http://sql.900jit.com/login/'
    res = requests.get(url=urlLogin1)
    # print('res:', res)
    cookie = res.headers.get('Set-Cookie').split(";")[0]
    # print('cookie', cookie)
    csrf = cookie.split('=')[1]
    # print('csrf:', csrf)
    #上面这段代码是为了进入sql平台且未账号密码未登陆时，获取csrftoken值，后面用户认证中要用到
    #分别用;和=来做spilt是为因为后面请求header参数中cookie和X-CSRFToken参数要求不一样
    #例子：Cookie: csrftoken=VwQZXRk8jI16hjnnAsn7kGsH00A2fjli6zqnJySRUJTtgdIAjYiRItNznZpb0AxZ
    #X-CSRFToken: VwQZXRk8jI16hjnnAsn7kGsH00A2fjli6zqnJySRUJTtgdIAjYiRItNznZpb0AxZ
    urlLogin2 = 'http://sql.900jit.com/authenticate/'
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookie,
        "X-CSRFToken": csrf
    }
    #该header是为了用户认证需要用的，其中的cookie和X-CSRFToken上面提到了，Content-Type则要求为x-www-form-urlencoded
    #所以需要替换掉默认的json
    data = {
        "username": "18352958010",
        "password": "test1234"
    }
    #sql平台的账号密码，（需要修改成自己的）
    resl2 = requests.post(url=urlLogin2, data=data, headers=header, verify=False)
    # print('content', resl2.content)

    #发送用户认证请求
    cookief = resl2.headers.get("Set-Cookie")
    # print("cookief:", cookief)
    csrf2 = cookief.split(";")[0]
    # print("csrf2:", csrf2)
    csrf2 = csrf2.split("=")[1]
    # print("csrf2:", csrf2)

    sessionid = cookief.split(";")[4].split(",")[1]
    # print("sessionid:", sessionid)

    cookief = 'csrftoken=' + csrf2 + ';' + sessionid
    # print('cookief:', cookief)
    #从接口的相应头中获取对sessionid，并跟上面的csrftoken一起组成Cookie，下面sql查询接口要要用
    url = 'http://sql.900jit.com/query/'
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookief,
        "X-CSRFToken": csrf2,
        "X-Requested-With": "XMLHttpRequest",
        "Host": "sql.900jit.com",
        "Origin": "http://sql.900jit.com",
        "Referer": "http://sql.900jit.com/sqlquery/"
    }
    #包装接口访问要使用的header
    data = {"instance_name": instanceName,
            "db_name": dbName,
            "schema_name": "",
            "tb_name": "",
            "sql_content": sql,
            "limit_num": 100}

    #db_name为对应生产的数据库名，tb_name为对应的表名，sql_content为对应的sql语句，limit_num为数据的返回数据限制，一般最大为1000
    response = requests.post(url, data=data, headers=header, verify=False)
    # print(type(response.text))
    # print(response.text)
    newdev = json.loads(response.text).get('data').get('rows')
    # print('newdev', newdev)  # 打印返回的数据
    # newdev为sql返回的数据
    newlist = json.loads(response.text).get('data').get('column_list')
    #newlist为返回的列标头
    return newdev




# sqlTDev = "select * from visualization_sea_booking_subscribe limit 1;"
# sqlTDevResult = pull_jira_data(sqlTDev, '生产-pub-pub-mdm-读写', 'mdm')
# print('sqlTDevResult:', sqlTDevResult)
