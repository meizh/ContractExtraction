# -*- coding: utf-8 -*-

# pdf合同文档类，用于标识合同的不同部分
class ContractObj:
    def __init__(self, id = 0, title = '', first_party = '', \
                 fp_contract_number = '', second_party = '', \
                 sp_contract_number = '', sign_place = '', content = '', \
                 sign_first_party = '', sign_fp_rep = '', sign_fp_date = '', \
                 sign_second_party = '', sign_sp_rep = '', sign_sp_date = ''):
        self.id = id                                               # 合同标识
        self.title = title                                         # 合同名
        self.first_party = first_party                             # 甲方名称
        self.fp_contract_number = fp_contract_number               # 甲方合同号
        self.second_party = second_party                           # 乙方名称
        self.sp_contract_number = sp_contract_number               # 乙方合同号
        self.sign_place = sign_place                               # 签署地点
        self.content = content                                     # 合同内容
        self.sign_first_party = sign_first_party                   # 签名页甲方名称
        self.sign_fp_rep = sign_fp_rep                             # 签名页甲方代表人签名
        self.sign_fp_date = sign_fp_date                           # 签名页甲方签名时间
        self.sign_second_party = sign_second_party                 # 签名页乙方名称
        self.sign_sp_rep = sign_sp_rep                             # 签名页乙方代表人签字
        self.sign_sp_date = sign_sp_date                           # 签名页甲方签名时间

    # 将对象的所有字段置空
    def clearFields(self):
        self.title = ''
        self.first_party = ''
        self.fp_contract_number = ''
        self.second_party = ''
        self.sp_contract_number = ''
        self.sign_place = ''
        self.content = ''
        self.sign_first_party = ''
        self.sign_fp_rep = ''
        self.sign_fp_date = ''
        self.sign_second_party = ''
        self.sign_sp_rep = ''
        self.sign_sp_date = ''

    # 显示所识别出的合同的各部分的内容，主要用于测试识别是否正确
    def showFields(self):
        print 'self.title: ' + self.title
        print 'self.first_party: ' + self.first_party
        print 'self.fp_contract_number: ' + self.fp_contract_number
        print 'self.second_party: ' + self.second_party
        print 'self.sp_contract_number: ' + self.sp_contract_number
        print 'self.sign_place: ' + self.sign_place
        print 'self.content: \n' + self.content
        print 'self.sign_first_party: ' + self.sign_first_party
        print 'self.sign_fp_rep: ' + self.sign_fp_rep
        print 'self.sign_fp_date: ' + self.sign_fp_date
        print 'self.sign_second_party: ' + self.sign_second_party
        print 'self.sign_sp_rep: ' + self.sign_sp_rep
        print 'self.sign_sp_date: ' + self.sign_sp_date + '\n\n'