# -*- coding:utf-8 -*-

# 用于测试一些语法和功能的，无实际作用
from ContractReader import *
import re
import jieba.analyse
# pdfPath = r'C:\Users\Russell\Desktop\Contract'
# txtPath = r'C:\Users\Russell\Desktop\Contract\text'
#
# contractObj = ContractReader(txtPath)
# contractObj.extract()
filename = r'jobs.txt'
textPath = r'C:\Users\Russell\Desktop\Contract\text'
# 获取文件名称及完整目录
textFile = os.path.abspath(os.path.join(textPath, filename))
fp_text = open(textFile, "r")
text = fp_text.read()
list_key = []
list_value = []
# text = 'When Paul Jobs was mustered out of the Coast Guard after World War II, he made a wager with his crewmates.'
for key in analyse.extract_tags(text, 10, withWeight=True):
    list_key.append(key[0])
    list_value.append(key[1])
wordFreq = dict(zip(list_key, list_value))
for key, value in wordFreq.items():
    print key + value
# detPattern = re.compile(r'第  \d*  页  共  \d* 页')
# res = detPattern.match('第  1  页  共  13 页')
# if res is not None:
#     print True

# try:
#     f = open(r'C:\Users\Russell\Desktop\Contract\123.txt', 'w')
#     f.write("页面访问成功\n")
#     f.close()
# except Exception, e:
#     print 'Error:', format(e)