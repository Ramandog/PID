import socket
import json
from struct import pack,unpack
from typing import Any
from pretreatment import Pre

class Get_pre(object):
    
    def __init__(self, model):
        self.model  = model
        pass
    
    def __call__(self):

        pre = Pre() #加载光谱预处理库
        data = self.get_sp() #获取光谱数据
        #test1 = pre.bs(data1[0,:].reshape(1,-1),sg = False)
        data_pre = pre.bs(data, sg = True) #数据预处理
        model1  = self.model(data_pre) #预处理后数据导入模型计算
        return model1
    
    @classmethod
    def get_sp(self, 
               host = '127.0.0.1', 
               port = 60000 
               ):
        '''
        获取光谱
        1.与光谱仪建立通讯
        2.获取光谱
        3.返回光谱
        '''
        server_ip = host #host
        servr_port = port #port

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp_client.bind(('127.0.0.1', 60000))
        tcp_client.settimeout(1) #延时时间
        tcp_client.connect((server_ip, servr_port)) #连接指令
        # load_table('spectrometer.json')
        # with open("spectrometer.json",'r') as f:
        #     lines=f.readline()
        #     db_table=json.loads(lines)
        # tx = json.dumps(db_table)
        spc_json = '{"method": "data_get","wavenumber": 1,"spectrum": 1,"wavelength": 1}'#接口命令
        tcp_client.sendall(bytearray(spc_json, encoding='ascii')) #发送指令
        spcout_json = tcp_client.recv(409600)#接收指令
        spcout = json.loads(spcout_json)["wavenumber_data"]#读取
        return spcout