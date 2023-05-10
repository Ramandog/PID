from pump_contr import Pump
import time

if __name__=='__main__':
    
    pump1 = Pump()
    ser1 = pump1.pump_conn()
    for i in range(1,11):
        time.sleep(2)
        ser1.write(pump1.pump_sp(i*100)) 

    time.sleep(5)

    pump1.pump_closs()
    if ser1.isOpen():             
        print("串口关闭失败。")
        print(ser1.name)  
    else:
        print("关闭串口成功。")