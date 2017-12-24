# -*- coding:utf-8 -*-

# 用于测试一些语法和功能的，无实际作用
from ContractReader import *
import re
import jieba.analyse
import nltk
# pdfPath = r'C:\Users\Russell\Desktop\Contract'
# txtPath = r'C:\Users\Russell\Desktop\Contract\text'
#
# contractObj = ContractReader(txtPath)
# contractObj.extract()
# filename = r'jobs.txt'
# textPath = r'C:\Users\Russell\Desktop\Contract\text'
# # 获取文件名称及完整目录
# textFile = os.path.abspath(os.path.join(textPath, filename))
# fp_text = open(textFile, "r")
# text = fp_text.read()
# list_key = []
# list_value = []
# # text = 'When Paul Jobs was mustered out of the Coast Guard after World War II, he made a wager with his crewmates.'
# for key in analyse.extract_tags(text, 10, withWeight=True):
#     list_key.append(key[0])
#     list_value.append(key[1])
# wordFreq = dict(zip(list_key, list_value))
# for key, value in wordFreq.items():
#     print key + value
# strs='1、大专以上学历，年龄在18-28岁之间；2、计算机相关专业、自动化、测控、生仪、机电、数学、物理等等理工科专业优先；' \
#      '3、热爱软件开发事业、有较强的逻辑思维能力，对IT行业抱有浓厚的兴趣并有志于在IT行业长远发展，创造个人价值（非销售、非保险岗位）；4、有无相关经验均可，欢迎优秀的应届大学毕业生' \
#      '5、渴望能有一项扎实的技术、获得一份有长远发展、稳定、有晋升空间的工作；、学习能力强，工作热情高，富有责任感，工作认真、细致、敬业，责任心强；'
# text1=jieba.cut(strs)
# fd=nltk.FreqDist(text1)
# keys=fd.keys()
# item=fd.iteritems()
# print ' '.join(keys)
# dicts=dict(item)
# sort_dict=sorted(dicts.iteritems(),key=lambda d:d[1],reverse=True)
# for k, v in sort_dict:
#     print k.encode('utf-8') + ': ' + str(v)

pop_str = [',','，', '“', '”','、', '。', '[', ']', ':', '：', ';', '；',  ' ', '）', '（', '(', ')', '/', '\\']

wordFreq = {',': 2, '“': 4, '+': 3, '）': 1, '-': 5}
for s in pop_str:
    if wordFreq.has_key(s):
        del wordFreq[s]
for k, v in wordFreq.items():
    print k.encode('utf-8') + ':' + str(v)


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