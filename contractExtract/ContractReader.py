# -*- coding:utf-8 -*-
import jieba
import matplotlib.pyplot as plt
from jieba import analyse
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
from ContractObj import *
import fnmatch
import os
import re

# 将pdf文件转成txt，并读取txt合同内容的类
class ContractReader:
    # pdfPath : pdf文件的目录
    # textPath：txt文件的目录
    def __init__(self, pdfPath, textPath, wordFreqPath):
        self.pdfPath = pdfPath
        self.textPath = textPath
        self.wordFreqPath = wordFreqPath

    # 将pdf文档转成txt文件，
    def pdf2Text(self):
        # 循环读取pdfPath目录下的pdf文件，
        for filename in os.listdir(self.pdfPath):
            # 若目录中的文件不是pdf文件，则跳过
            if not fnmatch.fnmatch(filename, '*.pdf'):
                continue
            # 若是pdf文档，则将目录和文件名称合并,设置需要打开的文件的完整地址及名称
            pdfFile = os.path.abspath(os.path.join(self.pdfPath, filename))
            # 如果txt存放的目录不存在，则新建该目录
            if os.path.exists(self.textPath) is False:
                os.makedirs(self.textPath)
            # 设置pdf转换成的txt文档的名称及完整目录
            textFile = os.path.abspath(os.path.join(self.textPath, filename[:-3] + 'txt'))
            try:
                # 以读的方式打开pdf文件，写的方式打开txt文件
                fp_pdf = open(pdfFile, "rb")
                fp_text = open(textFile, "w")
                # 读取pdf文件，并返回pdf的页面集合、页面解释器和聚合器
                doc, interpreter, device = self._openPDF(fp_pdf)
                # 使用文档对象得到页面集合
                for page in PDFPage.create_pages(doc):
                    # 使用页面解释器来读取
                    interpreter.process_page(page)
                    # 使用聚合器来获取内容
                    layout = device.get_result()
                    for out in layout:
                        if hasattr(out, "get_text"):
                            # 将读取的内容以utf-8的格式写入txt文件
                            fp_text.write(out.get_text().encode('utf-8'))
                print filename + '： 转换成功 ！'
            except IOError, e:
                print 'File Open Error:', format(e)

    def _openPDF(self, fp):
        # 创建一个与文档相关联的解释器
        parser = PDFParser(fp)
        # PDF文档对象
        doc = PDFDocument(parser)
        # 链接解释器和文档对象
        parser.set_document(doc)
        # 创建PDF资源管理器
        resource = PDFResourceManager()
        # 参数分析器
        laparam = LAParams()
        # 创建一个聚合器
        device = PDFPageAggregator(resource, laparams=laparam)
        # 创建PDF页面解释器
        interpreter = PDFPageInterpreter(resource, device)
        list_pdf = [doc, interpreter, device]
        return list_pdf

    def text2DB(self, connDB):
        # 用于返回所读取内容的 contractObj对象
        contractObj = ContractObj()
        # 检查页数的通配字符串
        patternStr = r'第  \d*  页  共  \d* 页'
        # 设置模式字符串
        detPattern = re.compile(patternStr)
        i = connDB.getContractStartID()
        # 循环读取txt目录的文件
        for filename in os.listdir(self.textPath):
            # 若目录中的文件不是pdf文件，则跳过
            if not fnmatch.fnmatch(filename, '*.txt'):
                continue
            # 将目录和文件名称合并,设置需要打开的文件
            textFile = os.path.abspath(os.path.join(self.textPath, filename))
            fp_text = open(textFile, "r")
            j = 1  # 页数
            k = 1  # 行数
            lines = fp_text.readlines()
            # 设置当前是第i个txt文件
            contractObj.id = i
            for line in lines:
                # 去掉字符串前后的换行符和空格符
                conStr = line.strip('\n').strip(' ')
                # 判断去掉换行符和回车符的字符串是否为空
                if len(conStr) > 1:
                    # 如果该行与检查页数的字符串匹配，则页数加1，行数重新置为1
                    if detPattern.match(line) is not None:
                        j += 1
                        k = 1
                    #  如果该行与检查页数的字符串不匹配，则通过当前的页数、行数及内容来识别
                    else:
                        # print '第' + str(i) + '个文件' + ' 第' + str(j) + '页:' + ' 第' + str(k) + '行:' + conStr
                        self._contentRecognition(j, k, conStr, contractObj)
                        k += 1
            # contractObj.showFields()
            # 将识别的txt文档内容插入数据库
            connDB.insertContractToDB(contractObj)
            i += 1
            # 关闭txt文档
            fp_text.close()
            # 将对象的全部字段置空
            contractObj.clearFields()

    def _contentRecognition(self, j, k, conStr, contractObj):
        if j == 1:
            if k == 1:
                contractObj.title = conStr
            elif k == 2:
                contractObj.first_party = conStr
            elif k == 3:
                contractObj.fp_contract_number = conStr
            elif k == 4:
                contractObj.second_party = conStr
            elif k == 5:
                contractObj.sp_contract_number = conStr
            elif k == 6:
                contractObj.sign_place = conStr
            elif k >= 7:
                contractObj.content += conStr + '\n'
        elif j == 15:
            if k == 3:
                contractObj.sign_first_party = conStr
            elif k == 4 or k == 5:
                contractObj.sign_fp_rep += conStr
            elif k == 6:
                contractObj.sign_fp_date = conStr
            elif k == 7:
                contractObj.sign_second_party = conStr
            elif k == 8 or k == 9:
                contractObj.sign_sp_rep += conStr
            elif k == 10:
                contractObj.sign_sp_date = conStr
        else:
            contractObj.content += conStr+ '\n'
        return contractObj

    # 对文档进行分词，并返回分词结果以及文档内容
    def textCut(self, textFile):
        # 打开txt文档，并读取内容
        fp_text = open(textFile, "rb")
        lines = fp_text.readlines()
        words = ''
        text = ''
        jieba.add_word('應用軟體')
        # jieba.load_userdict('C:/Users/Russell/Desktop/Contract/scel/amuse.txt')
        # 逐行读取内容，并进行分词
        for line in lines:
            text += line
            line = line.strip('\n').strip(' ')
            words += ' '.join(jieba.cut(line, cut_all = True))
        words_text = [words, text]
        fp_text.close()
        return words_text

    # 绘制词云的函数
    def wordCloudPlot(self, words):
        background_Image = plt.imread(r'E:\pictures\timg.jpg')
        # 设置描绘词云时的相关参数
        wc = WordCloud(background_color = 'white',  # 设置背景颜色
                       mask = background_Image,      # 设置背景图片
                       max_words = 100,              # 设置最大显示的单词数
                       stopwords = STOPWORDS,        # 设置停用词
                       font_path = 'C:/Users/Windows/fonts/msyh.ttf',  # 设置字体格式，如不设置显示不了中文
                       max_font_size = 100,           # 设置字体最大值
                       random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
                       )
        # 从分词结果来描绘词云
        wc.generate_from_frequencies(words)
        image_colors = ImageColorGenerator(background_Image)
        wc.recolor(color_func=image_colors)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    # 输出词频
    def wordFrequence(self, text, wordFreqPath, filename):
        # 依据文件目录打开文件
        if not os.path.exists(wordFreqPath):
            os.mkdir(wordFreqPath)
        filePath = os.path.abspath(os.path.join(wordFreqPath, filename))
        fp = open(filePath, "w")
        list_key = []
        list_value = []
        # 输出top100的词频
        for key in analyse.extract_tags(text, 1000, withWeight = True):
            fp.write(key[0].encode('utf-8') + ': ' + str(int(key[1] * 10000)).encode('utf-8') + '\n')
            list_key.append(key[0])
            list_value.append(key[1])
        wordFreq = dict(zip(list_key, list_value))

        # 以下代码可以识别中文的关键词，但是无法识别英文，将wordFreq用于描绘词云时，英文文档会报错
        # result = jieba.analyse.textrank(text, topK = 1000, withWeight=True)
        # wordFreq = dict()
        # for i in result:
        #     wordFreq[i[0]] = i[1]
        return wordFreq