# -*- coding: utf-8 -*-
import ConfigParser

# 读取配置文件的类
class ConfigReader:
    def __init__(self, cfg_path='config.cfg'):
        self.cfg = ConfigParser.ConfigParser()
        # 读取配置文件的目录地址
        self.cfg.read(cfg_path)
        # 存放数据库配置的列表
        self._db = []
        # 存放文件目录的列表
        self._filePath = []

    def getDBConfig(self):
        # 获取DBConfig标签下的多条配置信息
        o = self.cfg.options('DBConfig')
        # 循环读取配置信息并存入列表中
        for oo in o:
            self._db.append(self.cfg.get('DBConfig',oo))
        return self._db

    def getContractPath(self):
        # 后去contractPathConfig标签下的多条配置信息
        o = self.cfg.options('ContractPathConfig')
        # 循环读取配置信息并存入列表中
        for oo in o:
            self._filePath.append(self.cfg.get('ContractPathConfig', oo))
        return self._filePath