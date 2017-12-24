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
    pdfPath, textPath, cutResultPath, wordWeightPath, wordFreqPath = config.getContractPath()

    # 创建读取合同的对象
    conReader = ContractReader(pdfPath, textPath, cutResultPath, wordWeightPath, wordFreqPath)
    # 将pdf转成txt
    # conReader.pdf2Text()
    # 将txt文档的内容识别，并插入数据库
    # conReader.text2DB(connDB)
    # 关闭数据库连接
    # connDB.close()

    # 循环读取pdf转换成的txt文件，进行分词及绘词云
    for filename in os.listdir(textPath):
        # 将分词结果写入文件，并返回分词的结果和原始文档内容
        words, text = conReader.textCut(filename, textPath, cutResultPath)
        # 输出单词权重到文件，并返回单词权重的结果
        wordWei = conReader.wordWeight(text, filename, wordWeightPath)
        # 输出词频到文件，并返回词频排序后的结果
        wordFreq = conReader.wordFrequence(text, filename, wordFreqPath)
        # 直接通过分词结果描绘词云会出现单词重复，通过词频来描绘词云不会
        # 既可通过词频来绘词云，也可通过单词的权重来描绘词云
        conReader.wordCloudPlot(wordFreq)