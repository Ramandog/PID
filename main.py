import os
import datetime
from pump_contr import Pump
from apscheduler.schedulers.blocking import BlockingScheduler
from spc import Get_pre
from job import Job


if __name__=='__main__':

    target = 30
    target_low = 28 #目标浓度下限
    target_high = 32 #目标浓度上限

    pump1 = Pump() #泵方法库
    ser1 = pump1.pump_conn()#泵连接
    scheduler1 = BlockingScheduler()#线程池
    load_model1 = [] ####加载模型
    get_pre1 = Get_pre(load_model1) #Current concentration;当前浓度
    start_time1 = datetime.datetime.now()     

    #job方法库
    job1 = Job(
            start_time1,
            get_pre1,
            ser1,
            pump1,
            scheduler1)  

    if get_pre1 < target_low:
        #启动pid
        print("当前浓度: %s; 未低于目标浓度: %s!"%(get_pre1, target),'\n',"开始自动补料！")
        scheduler1 .add_job(
                            job1.my_job1,
                            'interval',
                            seconds=5,
                            id = '001'
                            )
        scheduler1.start()
    else:
        print("当前浓度: %s; 未低于目标浓度: %s!"%(get_pre1, target))
    # scheduler.remove_all_jobs()
    # scheduler.shutdown(wait=False)