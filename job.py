import datetime
import time
from simple_pid import PID

class Job():
    def __init__(self, start_time, get_pre, ser, pump, scheduler):
        self.Target = 30 #目标浓度
        self.s_alph = 200
        self.T_feed = 3 #1.补料周期：补料时长
        self.T_wait = 3 #2.等待周期：等待补料响应
        self.T_pred = 2 #3.预测周期：预测周期要大于采样周期+模型计算周期
        self.low = 28 #目标浓度下限
        self.high = 32 #目标浓度上限
        self.start_time = start_time #反馈控制开始时间
        self.pred = get_pre #get_pre()
        self.pid = PID(0.5, 0, 0.1, setpoint = self.Target)
        self.ser = ser #ser1 实例
        self.pump = pump #pump1 实例
        self.scheduler = scheduler #scheduler1 实例
        pass

    def my_job1(self):

        self.volume = self.pred #获取当前浓度
        current_time = datetime.datetime.now()
        #dt = (current_time - last_time)
        # time.sleep(self.T_feed) #
        print('开始补料：',current_time.strftime('%Y-%m-%d %H:%M:%S'))
        #变量volume在整个系统中作为输出，变量volume与理想值之差作为反馈回路中的输入，通过反馈回路调节变量power的变化。
        power = self.pid(self.volume)
        #print(power)
        speed =  self.s_alph*power #计算泵速度
        print("当前浓度：", self.volume, " ; ",'speed', speed) #输出速度
        i_open = self.pump.pump_sp(speed)
        self.ser.write(i_open) #开泵
        time.sleep(self.T_feed) #补料时长
        i_closs = self.pump.pump_sp(speed)
        self.ser.write(i_closs) #关泵
        time.sleep(self.T_feed) #等待反应稳定
        self.volume = self.pred #等待反应稳定
        print('补料结束: ',(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'))
        print("当前浓度：", self.volume)
        #用于输出结果可视化
        # x += [current_time - start_time]
        # y += [myplc.get_value('pH')[0]]
        # setpoint += [3]
        #用于变量volume赋初值
        if (current_time-self.start_time).total_seconds() > 0: #start_time关闭时更新

            self.pid.setpoint = self.Target

        #last_time = current_time
        #timeend = timestart+datetime.timedelta(seconds=10)
        if self.volume > self.low:
            #np.save
            self.scheduler.pause_job('001')
            self.scheduler.remove_job('001')