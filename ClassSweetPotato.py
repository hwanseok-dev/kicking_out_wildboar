# -*- coding: utf-8 -*-


MAP_SIZE = 20

import numpy as np
import matplotlib.pyplot as plt
import random

#map_drone[:,:] = 

class SweetPotato:
    def __init__(self,_amount):
        
        #고구마가 그려질 밭. 지금은 모두 초록색으로 칠해진다.
        self.map_potato = np.zeros((MAP_SIZE, MAP_SIZE, 3), dtype =np.int)
        self.map_potato[:][:] = [0,255,0] # 초록으로 칠하기
        #생성할 고구마의 양
        self.amount = _amount
        
        #생성된 고구마의 좌표와 가치를 저장. 가치는 0(고구마없음),1,2,3의 값을 가 
        self.positions = np.zeros((1,3), dtype = np.int)
        for i in range(_amount):
            temp = np.zeros((1,3), dtype=np.int)#고구마 y 좌표
            y = random.randrange(0,MAP_SIZE)
            temp[0][0] = y
            x = random.randrange(0,MAP_SIZE) #고구마 x 좌표
            temp[0][1] = x
            value = random.randrange(0,3)    #고구마 가치(0~2)
            temp[0][2] = (4-value) * 50         
            self.positions = np.append(self.positions, temp,axis = 0)
        self.positions = np.delete(self.positions, 0, axis = 0)
        #print(self.positions)
    
    #고구마의 좌표 맵에 표현하        
    def draw(self):
        
        #맵에서 진한색으로 그려질 수록 높은 가치
        #고구마가 없는 밭의 픽셀값 : [0,255,0]
        #가치 1인 고구마의 픽셀값 : [150,0,150]
        #가치 2인 고구마의 픽셀값 : [100,0,100]
        #가치 3인 고구마의 픽셀값 : [50,0,50]
        for potato in self.positions:
            self.map_potato[potato[0], potato[1]]= [potato[2],0,potato[2]] #고구마의 가치에 따라서 자색으로 칠하기. 진한 색이 높은 가치를 나타냄
        #print(self.map_potato)
        
#Create SweetPotato object(_y,_x,_index)
'''
멧돼지 객체를 만들 때 _y 좌표를 먼저 입력하는 이유
              x축
      +-----------------
      |(0,0) (0,1) (0,2)
 y축  |(1,0) (1,1) (1,2)
'''

'''
#amount = random.randrange(1,3)
amount = MAP_SIZE * MAP_SIZE
sp = SweetPotato(amount)
sp.draw()
'''
