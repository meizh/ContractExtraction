# -*- coding:utf-8 -*-
from ConnDB import *
from ConfigReader import *
from ContractReader import *

# 主程序文件
if __name__ == '__main__':
    # 创建配置类对象
    config = ConfigReader()
    # 获取连接数据库配置参数
    # userName, password, host, port, dbName = config.getDBConfig()
    # 创建数据库实例对象
    # connDB = ConnDB(userName, password, host, port, dbName)
    # 连接数据库meizh
    # connDB.connectDB()
    # 打印数据库版本，测试是否连接成功
    # connDB.showVersion()

    # 获取doc文件存放目录
    pdfPath, textPath, wordFreqPath = config.getContractPath()

    # 创建读取合同的对象
    conReader = ContractReader(pdfPath, textPath, wordFreqPath)
    # 将pdf转成txt
    # conReader.pdf2Text()
    # 将txt文档的内容识别，并插入数据库
    # conReader.text2DB(connDB)
    # 关闭数据库连接
    # connDB.close()

    # 循环读取pdf转换成的txt文件，进行分词及绘词云
    for filename in os.listdir(textPath):
        # 获取文件名称及完整目录
        textFile = os.path.abspath(os.path.join(textPath, filename))
        # 分词并输出分词结果以及原始文本的内容
        words, text = conReader.textCut(textFile)
        # 输出词频到文件，并返回词频的对象
        wordFreq = conReader.wordFrequence(text, wordFreqPath, filename)
        # 直接通过分词结果描绘词云会出现单词重复，通过词频来描绘词云不会
        conReader.wordCloudPlot(wordFreq)