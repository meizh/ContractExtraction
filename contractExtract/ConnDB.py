# -*- coding: utf-8 -*-
import cx_Oracle
import sys
import os

# 进行数据库连接，提供数据插入等操作的类
class ConnDB:
    def __init__(self, userName, password, host, port, dbName):
        default_encoding = "utf-8"
        # 若系统默认的编码方式不为UTF-8，则设置为UTF-8，
        if sys.getdefaultencoding() != default_encoding:
            reload(sys)
            sys.setdefaultencoding(default_encoding)
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
        # 通过参数将类的变量初始化
        self.userName = userName
        self.password = password
        self.host = host
        self.port = port
        self.dbName = dbName
        self.conn = None
        self.cursor = None

    # 进行数据库连接，并获取数据库连接及游标
    def connectDB(self):
        print '进行数据库连接...'
        try:
            tns = cx_Oracle.makedsn(host = self.host, port = self.port, service_name = self.dbName)
            # 通过用户名、密码以及监听器连接Oracle数据库
            self.conn = cx_Oracle.connect(self.userName, self.password, tns)
            self.cursor = self.conn.cursor()
            print '数据库连接成功'
        except cx_Oracle.Error, e:
            print '数据库连接未成功：', format(e)

    # 显示数据库版本，主要用来测试是否连接上数据库
    def showVersion(self):
        print self.conn.version

    # 执行SQL语句
    def _executeSQL(self, sql):
        try:
            self.cursor.execute(sql)
        except cx_Oracle.Error, e:
            print 'Database Error:', format(e)

    # 获取数据库CONTRACT_CONTENT表当前的最大ID，确定插入数据时的起始ID，ID是自增的
    def getContractStartID(self):
        max_id_sql = 'select max(id) from CONTRACT_CONTENT'
        self.cursor.execute(max_id_sql)
        # 将所获取结果左右边的括号以及逗号去掉
        con_id_max = str(self.cursor.fetchone()).lstrip('(').rstrip(')').rstrip(',')
        con_id_start = 1 if con_id_max == 'None' else int(con_id_max)+ 1
        return con_id_start

    # 将文档内容的数据插入到数据库中
    def insertContractToDB(self, contractObj):
        try:
            sql_insert = 'insert into contract_content(id, title, first_party, fp_contract_number,  \
                                                        second_party, sp_contract_number, sign_place, content, \
                                                        sign_first_party, sign_fp_rep, sign_fp_date, \
                                                        sign_second_party, sign_sp_rep, sign_sp_date) \
                          values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)'
            # 因为content字段原始类型是varchar的，如果长度太大，在插入时会自动转换成LONG类型，因此插入到CLOB类型的数据库字段
            # 时会报“ORA-01461: 仅能绑定要插入 LONG 列的 LONG 值”的错误，需要在插入之前
            # 对varchar类型的字段进行转换，将其转换成CLOB类型，再插入才不会报错
            contentStr = self.cursor.var(cx_Oracle.CLOB)
            # 设置contentStr的值
            contentStr.setvalue(0, contractObj.content)
            # sql插入语句的参数
            params = (contractObj.id, contractObj.title, contractObj.first_party, contractObj.fp_contract_number, \
                      contractObj.second_party, contractObj.sp_contract_number, contractObj.sign_place, \
                      contentStr, \
                      contractObj.sign_first_party, contractObj.sign_fp_rep, contractObj.sign_fp_date, \
                      contractObj.sign_second_party, contractObj.sign_sp_rep, contractObj.sign_sp_date)
            # 执行数据的插入语句
            self.cursor.execute(sql_insert, params)
            self.conn.commit()
            # 返回插入成功信息
            print contractObj.title.strip('\n') + '：插入成功'
        except cx_Oracle.Error, e:
            print contractObj.title.strip('\n') + '：插入失败'
            print 'Error:', format(e)

    # 关闭数据库连接及游标
    def close(self):
        self.cursor.close()
        self.conn.close()