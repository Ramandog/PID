import os
import serial
import serial.tools.list_ports
import time
# import threading

class Pump():

    def __init__(self):
        pass

    def pump_test(self):
        '''
        检测串口
        '''
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            print("无串口设备,程序即将关闭。")
            time.sleep(1)
            os._exit(0)
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])
        return ''.join(list(comport)[0])

    def pump_conn(self, 
                  baudrate=1200,
                  parity='E',
                  timeout=0.1
                  ):
        '''
        串口开启
        baudrate:波特率;默认为1200
        parity:校验位;默认为'E'(偶校验)
        timeout:时延;默认为0.1
        '''
        com = self.pump_test()
        self.ser = serial.Serial(
                                com,
                                baudrate=baudrate,
                                parity=parity,
                                timeout=timeout)  
        #re = ser.read(4096)  
        #print(re)
        if self.ser.isOpen():     # 判断串口是否成功打开
            print("打开串口成功。")
            print(self.ser.name)     # 输出串口号
        else:
            print("打开串口失败。")
            time.sleep(1)
            os._exit(0)
        return self.ser
    
    def pump_closs(self): 
        '''
        关闭串口
        '''
        stop = 'E9 01 06 57 4A 00 00 00 01 1B'
        send_data = bytes.fromhex(stop)
        self.ser.write(send_data) 
        self.ser.close()

    def pump_stop(self): 
        '''
        停止泵
        '''
        stop = 'E9 01 06 57 4A 00 00 00 01 1B'
        send_data = bytes.fromhex(stop)
        self.ser.write(send_data) 
    
    def String_dec(self, 
                   string 
                   ):
        """ 
        str转为十进制
        """
        dec_data = 0
        capital  = string.upper() # 小写字符转大写字符.
        for i in capital:
            tmp = ord(i)          # 返回ASSCII值.
            if tmp <= ord('9') :
                dec_data = dec_data << 4
                dec_data += tmp - ord('0')
            elif ord('A') <= tmp <= ord('F'):
                dec_data = dec_data << 4
                dec_data += tmp - ord('A') + 10
        return dec_data

    def pump_sp(self,
                s,
                falWJ = 'E90106574A',
                qq = '01',
                diction='01'
                ):
        '''
        速度转指令
        s:速度;(1-999)
        falWJ = 'E90106574A'
        qq:全速/启停;(0:全速, 1:正常)/(0:停止, 1:启动)
        diction:方向；'01'(正向),'00'(反向)
        '''
        qq = qq
        diction = diction
        if s > 999:
            s = 999
            print("速度上限为999!")
        elif s < 1 and s!=0:
            s=1
            print("速度下限为1!")
        elif s==0:
            stop = 'E9 01 06 57 4A 00 00 00 01 1B'
            return bytes.fromhex(stop)
        speed = hex(s)
        if len(speed) == 3:
            speed1 = '00' 
            speed2 = '0' + speed[2:]
        elif len(speed) == 4:
            speed1 = '00' 
            speed2 = speed[2:]
        elif len(speed) == 5:
            speed1 = '0' + speed[2]
            speed2 = speed[3:]
        #fcs:校验位(同或校验)
        fcs = hex(0x01^0x06^0x57^0x4A\
                ^self.String_dec(speed1)^self.String_dec(speed2)\
                ^self.String_dec(qq)^self.String_dec(diction))
        
        if len(fcs) < 4:
            fcs = '0' + fcs[2:]
        else:
            fcs = fcs[2:]            
        instruction = falWJ+speed1+speed2+'01'+diction+fcs

        return bytes.fromhex(instruction.upper())
