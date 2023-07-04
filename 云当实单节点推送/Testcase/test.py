import time

from datetime import datetime, date

#
# cur_dir = os.path.abspath(os.path.join(os.getcwd(), "..",))
# print("Current directory:", cur_dir)
# curDir = filePath.get_current_directory()
# path = curDir + '\sqlResultData'
# print(path)
GITM = '2023-07-03 14:27:59'
# # print(GITM.strftime("%Y-%m-%d %H:%M"))
# GITM = datetime.datetime.strptime(GITM, "%Y-%m-%d %H:%M:%S")
# GITM = GITM.strftime("%Y-%m-%d %H:%M")

GITM = datetime.strptime(GITM, '%Y-%m-%d %H:%M:%S')
GITM = GITM.strftime("%Y-%m-%d %H:%M")
print(GITM)