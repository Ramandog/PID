import numpy as np
import copy
from BaselineRemoval import BaselineRemoval
from scipy.signal import savgol_filter

class EMA():
    '''
    period:滤波器开头基数
    arr:输入矩阵
    '''

    def __init__(self
                , period=21 
                 ):
        self.period=period 

    def _ema1(self, arr):
        N = len(arr)
        a = 2/(N+1)
        data = np.zeros(len(arr))
        for i in range(len(data)):
            data[i] = arr[i] if i==0 else a*arr[i]+(1-a)*data[i-1]  #从首开始循环
        return data[-1]

    def _ema2(self, arr):
        data = copy.deepcopy(arr)
        for i in range(self.period-1,len(arr)):
            data[i] = self._ema1(arr[i+1-self.period:i+1])

        return data
    
    def ema(self, arr):
        X = copy.deepcopy(arr)
        n= arr.shape[1]
        for i in range(n):
                X[:, i] = self._ema2(X[:,i])

        return X
    

class Pre():
            
    def __init__(self, 
                 period=21,
                 sf_w = 7,
                 sf_i = 5,
                 ):
        self.period=period
        self.sf_w = sf_w
        self.sf_i = sf_i  

    def _std(self, 
             a, 
             windosize = 3, 
             n =1.5
             ):

            #for i in range(time):
            output = []
            for i in range(len(a)):

                        if i < windosize:
                                    output = np.append(output, a[i])

                        elif i > len(a)-windosize-1:
                                    output = np.append(output, a[i])

                        else:
                                    pl = a[i-windosize:i+windosize+1] 
                                    median = np.median(pl, axis=0)
                                    mean = np.mean(pl, axis=0)
                                    std = np.std(pl)
                                    max_range = median + n*std 
                                    min_range = median - n*std

                                    if a[i] > max_range:
                                                max_range = median + n*std *0.01
                                                output = np.append(output, max_range)

                                    elif a[i] < min_range:
                                                min_range = median - n*std*0.01
                                                output = np.append(output, min_range)

                                    else:
                                                output = np.append(output, a[i])

                                    #a = output
            return(output)

    def bs(self, 
           X, 
           start = 40,
           end = 600, 
           deriv = 0,
           alphr = 28,
           sg = False,
           sg_w = 5,
           sg_i = 3,
           d = 0
           ):
            '''
            deriv变量为求导阶数
            ''' 
            test = copy.deepcopy(X[:, start:end])

            for i in range(test.shape[0]):

                test_std = self._std(test[i, :], 3, 1.5)
                test_fit = savgol_filter(test_std, self.sf_w, self.sf_i, deriv)
                base = BaselineRemoval(test_fit)
                test[i] = base.ZhangFit(alphr)
                if(sg):
                    test[i] = savgol_filter(test[i], sg_w, sg_i, d)  
            return test
    
    def normal(self, 
               X,
               start = 120,
               end = 160,
               sg = False,
               sg_w = 5,
               sg_i = 3,
               d = 0 
               ):
            '''
            deriv变量为求导阶数
            ''' 
            test = copy.deepcopy(X)

            for i in range(test.shape[0]):
            #test_std = STD(test[i, :], 3, 1.5)
            #test_fit = savgol_filter(test[i, :], 1, 1, deriv)
                if(sg):
                    test[i] = savgol_filter((test[i]/np.max(test[i,start:end]))*100,sg_w, sg_i, d)
                else:
                    test[i] = test[i]/np.max(test[i,start:end])*100
            return test
    
from datetime import *

class Tloss():

    def __init__(self):
        pass

    def date(self, t):

        dt = list(str(int(t)))
        for i in range(1, 6):
            dt.insert((1+i*3), ',')
        dt = ''.join(dt) 
        date = datetime.strptime(dt, "%Y,%m,%d,%H,%M,%S")

        return date

    def to_digit1(self, x):

        Out = np.zeros((x.shape[0]))
        start = self.date(x[0])
        for i in range(len(x)):
            Out[i] = (self.date(x[i])- start).total_seconds()
        return Out
        
    def to_digit2(self, x):
        
        Out = np.zeros((x.shape[0]))
        for i in range(1, len(x)):
            Out[i] = (self.date(x[i])- self.date(x[i-1])).total_seconds()
        return Out