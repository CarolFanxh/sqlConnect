# python 请求之前执行
# python 请求之前执行
import requests
import json
import datetime#TimeDeal需要
import openpyxl
import pandas as pd
import pymysql
import os
import re
import time

# time.sleep(20)

def authenticate():
    urlLogin1 = "http://sql.900jit.com/login/"
    res = requests.get(url=urlLogin1)
    cookie = res.headers.get("Set-Cookie").split(";")[0]
    csrf = cookie.split("=")[1]
    urlLogin2 = "http://sql.900jit.com/authenticate/"

    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookie,
        "X-CSRFToken": csrf
    }
    data = {
        "username": "18352958010",
        "password": "test1234"
    }
    resl2 = requests.post(url=urlLogin2, data=data, headers=header, verify=False)
    cookief = resl2.headers.get("Set-Cookie")
    csrf2 = cookief.split(";")[0].split("=")[1]
    sessionid = cookief.split(";")[4].split(",")[1]
    cookief = "csrftoken=" + csrf2 + ";" + sessionid
    return cookief, csrf2

def pull_jira_data(sql, instanceName, dbName):
    requests.packages.urllib3.disable_warnings()
    cookief, csrf2 = authenticate()
    url = "http://sql.900jit.com/query/"


    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookief,
        "X-CSRFToken": csrf2,
        "X-Requested-With": "XMLHttpRequest",
        "Host": "sql.900jit.com",
        "Origin": "http://sql.900jit.com",
        "Referer": "http://sql.900jit.com/sqlquery/"
    }
    data = {"instance_name": instanceName,
            "db_name": dbName,
            "schema_name": "",
            "tb_name": "",
            "sql_content": sql,
            "limit_num": 100}
    response = requests.post(url, data=data, headers=header, verify=False)
    newdev = json.loads(response.text).get("data").get("rows")
    return newdev



def TimeDeal(intime):
    # 计算时间戳
    seconds = intime / 1000
    # 创建 datetime 对象
    dt_obj = datetime.datetime.fromtimestamp(seconds)
    # 将 datetime 对象转换为指定格式的时间字符串
    out_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    return out_time


current_date = datetime.datetime.now().date()
new_create_time = str(current_date) + " 07:40:53"
casenumber = "285756680744384"
sqlTDev = f"SELECT * FROM LV_PUSH_NODE_LOG WHERE casenumber = '{casenumber}' AND type = 'DINGDING' AND CREATE_TIME > to_date('{new_create_time}','yyyy-MM-dd HH24:mi:ss')  ORDER BY create_time DESC;"
print(sqlTDev)

sqlTDevResult = pull_jira_data(sqlTDev, "生产-GM2-ORACLE-读写权限", "MODELHOME")
# print(sqlTDevResult)

ctn_desc = {}
EMAIL = {}
DING = {}

data = {}
for one in sqlTDevResult:
    statusCode = one[2]
    assert one[3] == 'success', '钉钉推送失败'
    print(statusCode)
    statusJson = json.loads(one[4])
    if statusCode not in data:
        data[statusCode] = {}
        # print(11111,data[statusCode])
        for key, value in statusJson.items():
            data[statusCode][key] = value
    else:
        continue


print(data)

# ARun.set("data", data)


