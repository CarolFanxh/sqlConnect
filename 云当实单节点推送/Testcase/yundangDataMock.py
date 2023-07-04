
import requests
from Config import login

bl_no = 'ZGSHA0382001043'
sqlTDev = f"select json_data from callback_in where json_data like '%{bl_no}%' and source = 'YUNDANG'"
# print(sqlTDev)
sqlTDevResult = login.pull_jira_data(sqlTDev, '生产-pub-pub-mdm-读写', 'mdm')
# print(sqlTDevResult)

url = 'http://116.63.45.120/dzg-logistics-rest/vol/callbackData/mockReCtnSourceData'

for i, row in enumerate(sqlTDevResult):
    for j, cell in enumerate(row):
        # 获取大括号里面的内容
        if isinstance(cell, str):
            # print(json.dumps(cell))转义
            data = {
                "jsonContent": cell,
                "platformCode": "YUNDANG",
                "nodeCode": "BDAR",
                "nodeType": ""
            }

            response = requests.post(url, json=data)
            assert response.status_code == 200
        else:
            content = cell.pop()


