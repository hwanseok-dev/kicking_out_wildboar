# -*- coding: utf-8 -*-


MAP_SIZE = 20

import numpy as np
import matplotlib.pyplot as plt


class WildBoar:
    def __init__(self,_y,_x,_index):
        self.map_boar = np.zeros((MAP_SIZE, MAP_SIZE,3), dtype =np.int)
        self.map_boar[:,:] = [0,255,0]
        
        #Define WildBoar's states according to STD
        self.STATE_KICKED_OUT = 0
        self.STATE_ACTIVE = 1
        self.STATE_WILL_TO_SWEET_POTATO = 2
        self.STATE_WILL_TO_RUN_OUT = 3
        self.STATE_MOVING = 4
        self.EATING = 5
        
        #Define Boae size
        self.SIZE_WIDTH = 2
        self.SIZE_HEIGHT = 3
        
        #Define WildeBoar's Orientation
        self.ORIENT_DOWN = 100
        self.ORIENT_UP = 101
        self.ORIENT_LEFT = 102
        self.ORIENT_RIGHT = 103
        
        #Initialize position ,state, index
        self.start_x = _x
        self.start_y = _y
        self.x = _x
        self.y = _y
        self.state = self.STATE_ACTIVE
        self.index = _index                   # 멧돼지 번호
        
        #멧돼지가 생겨난 방향에 따라서 보고 있는 방향을 상/하/좌/우 중에서 정해준다.
        #멧돼지가 보고 있는 방향은 멧돼지의 shape이 (2,3)이기 때문에 중요하고, 머리의 위치를 파악할 때 필요하
        if(self.y > self.x):
            self.orient = self.ORIENT_RIGHT
        else:
            self.orient = self.ORIENT_DOWN
    
    #앞으로 한 칸 전진
    def goStraight(self):
        if(self.orient == self.ORIENT_DOWN):
            self.y += 1
        elif(self.orient == self.ORIENT_UP):
            self.y -= 1
        elif(self.orient == self.ORIENT_LEFT):
            self.x -= 1
        elif(self.orient == self.ORIENT_RIGHT):
            self.x += 1
        else :
            print("goStraight Error")
    #좌회전
    def turnLeft(self):
        if(self.orient == self.ORIENT_DOWN):
            self.orient = self.ORIENT_RIGHT
        elif(self.orient == self.ORIENT_UP):
            self.orient = self.ORIENT_LEFT
        elif(self.orient == self.ORIENT_LEFT):
            self.orient = self.ORIENT_DOWN
        elif(self.orient == self.ORIENT_RIGHT):
            self.orient = self.ORIENT_UP
        else :
            print("turnLeft Error")
    #우회전
    def turnRight(self):
        if(self.orient == self.ORIENT_DOWN):
            self.orient = self.ORIENT_LEFT
        elif(self.orient == self.ORIENT_UP):
            self.orient = self.ORIENT_RIGHT
        elif(self.orient == self.ORIENT_LEFT):
            self.orient = self.ORIENT_UP
        elif(self.orient == self.ORIENT_RIGHT):
            self.orient = self.ORIENT_DOWN
        else :
            print("turnRight Error")
            
    #Param으로 주어진 '고구마가 그려진 맵'에 멧돼지의 위치를 나타내는 빨간색을 그려서 return한다.
    def draw(self, map_drone):
        #좌표와 방을 기준으로 (2*3)만큼 빨간색으로 칠한다.
        if(self.orient == self.ORIENT_DOWN):
            '''
            00  몸통
            00  몸통
            12  머리(2가 self.x,self.y 좌표)
            '''
            head_dx = [0,-1]
            head_dy = [0,0]
            body_dx = [0,0,-1,-1]
            body_dy = [-1,-2,-2,-1]
        elif(self.orient == self.ORIENT_RIGHT):
            '''
            002
            001
            '''
            head_dx = [0,0]
            head_dy = [0,1]
            body_dx = [-1,-2,-2,-1]
            body_dy = [0,0,1,1]
        elif(self.orient == self.ORIENT_UP):
            '''
            21
            00
            00
            '''
            head_dx = [0,1]
            head_dy = [0,0]
            body_dx = [0,0,1,1]
            body_dy = [1,2,2,1]
        elif(self.orient == self.ORIENT_LEFT):
            '''
            100
            200
            '''
            head_dx = [0,0]
            head_dy = [0,-1]
            body_dx = [1,2,2,1]
            body_dy = [0,0,-1,-1]
        
        for j in range(2):
            if(0<=self.y+head_dy[j] and self.y+head_dy[j]<MAP_SIZE and 0<=self.x+head_dx[j] and self.x+head_dx[j]<MAP_SIZE):
                map_drone[self.y+head_dy[j]][self.x+head_dx[j]] = [254,0,0]
        for j in range(4):
            if(0<=self.y+body_dy[j] and self.y+body_dy[j]<MAP_SIZE and 0<=self.x+body_dx[j] and self.x+body_dx[j]<MAP_SIZE):
                map_drone[self.y+body_dy[j]][self.x+body_dx[j]] = [255,0,0]
        #print(self.map_boar)
        return map_drone
    
    #빨간색이 칠해진 멧돼지의 위치에 있는 고구마의 가치를 줄인다. 피해입은 정도는 [고구마가치,피해입은 횟수,고구마가치]로 나타낸다.
    #예를 들어서 [50,1,50]이면 [100,0,100]에서 피해를 한 번 입은 경우
    #[50,2,50]이면 [150,0,150]에서 피해를 두 번 입은 경우를 의미한다.
    #맵에서 진한색으로 그려질 수록 높은 가치
    #고구마가 없는 밭의 픽셀값 : [0,255,0]
    #가치 1인 고구마의 픽셀값 : [150,0,150]
    #가치 2인 고구마의 픽셀값 : [100,0,100]
    #가치 3인 고구마의 픽셀값 : [50,0,50]
    def decreasePotatoValue(self,map_tofind ):
        if(self.orient == self.ORIENT_DOWN):
            '''
            00  몸통
            00  몸통
            12  머리(2가 self.x,self.y 좌표)
            '''
            head_dx = [0,-1]
            head_dy = [0,0]
            body_dx = [0,0,-1,-1]
            body_dy = [-1,-2,-2,-1]
        elif(self.orient == self.ORIENT_RIGHT):
            '''
            002
            001
            '''
            head_dx = [0,0]
            head_dy = [0,1]
            body_dx = [-1,-2,-2,-1]
            body_dy = [0,0,1,1]
        elif(self.orient == self.ORIENT_UP):
            '''
            21
            00
            00
            '''
            head_dx = [0,1]
            head_dy = [0,0]
            body_dx = [0,0,1,1]
            body_dy = [1,2,2,1]
        elif(self.orient == self.ORIENT_LEFT):
            '''
            100
            200
            '''
            head_dx = [0,0]
            head_dy = [0,-1]
            body_dx = [1,2,2,1]
            body_dy = [0,0,-1,-1]
        for j in range(2):
            if(0<=self.y+head_dy[j] and self.y+head_dy[j]<MAP_SIZE and 0<=self.x+head_dx[j] and self.x+head_dx[j]<MAP_SIZE):
                r = map_tofind[self.y+head_dy[j]][self.x+head_dx[j]][0]
                g = map_tofind[self.y+head_dy[j]][self.x+head_dx[j]][1]
                b = map_tofind[self.y+head_dy[j]][self.x+head_dx[j]][2]
                map_tofind[self.y+head_dy[j]][self.x+head_dx[j]] = [r+50,g+1,b+50]
                
        for j in range(4):
            if(0<=self.y+body_dy[j] and self.y+body_dy[j]<MAP_SIZE and 0<=self.x+body_dx[j] and self.x+body_dx[j]<MAP_SIZE):
                r = map_tofind[self.y+body_dy[j]][self.x+body_dx[j]][0]
                g = map_tofind[self.y+body_dy[j]][self.x+body_dx[j]][1]
                b = map_tofind[self.y+body_dy[j]][self.x+body_dx[j]][2]
                map_tofind[self.y+body_dy[j]][self.x+body_dx[j]] = [r+50,g+1,b+50]
        
        return map_tofind
   
    #주변에서 가장 가치가 높은 고구마를 찾아서 이동한다.
    def findPotatos(self, map_tofind):
        #현위치의 고구마의 가치를 깎음
        map_tofind = self.decreasePotatoValue(map_tofind)
        
        #주변에서 가장 가치가 높은 고구마의 위치를 찾음
        dx = [0,1,-1,2,-2]
        dy = [0,1,-1,2,-2]
        target_x = self.x
        target_y = self.y
        max_value = 255 # 고구마의 가치는 픽셀값이 작을 수록 높음
        grass_count = 0
        for i in dx:
            for j in dy:
                if(self.y+dy[j] < 0 or self.y+dy[j]>= MAP_SIZE or self.x+dx[i]<0 or self.x+dx[i]>=MAP_SIZE) :
                    continue
                if(np.array_equal(map_tofind[self.y+dy[j]][self.x+dx[i]],[0,255,0])):
                    grass_count += 1 # dummy
                elif(map_tofind[self.y+dy[j]][self.x+dx[i]][1] < 10):
                    if( max_value > map_tofind[self.y+dy[j]][self.x+dx[i]][0] ):
                        target_x =self.x+dx[i]
                        target_y = self.y+dy[j]
                        max_value = map_tofind[self.y+dy[j]][self.x+dx[i]][0]
        #print("현재 위치",self.y,self.x)
        #print("타깃 위치",target_y,target_x)
        #목표로 가기 위한 방향을 바라본다.
        self.checkOrientation(target_y,target_x)
        #목표로 한 번 움직인다.
        self.goStraight()
        return map_tofind
    
    #목표 위치로 가기 위해서 어느 방향을 봐야하는지 판단한다.
    def checkOrientation(self, target_y, target_x):
        if(target_x - self.x > 1): #오른쪽으로 가야하는 경우
            if(self.orient == self.ORIENT_UP):
                self.turnRight()
            elif(self.orient == self.ORIENT_DOWN):
                self.turnLeft()
            elif(self.orient == self.ORIENT_LEFT):
                self.turnLeft()
                self.turnLeft()
            
        elif(target_x - self.x < -1):
            if(self.orient == self.ORIENT_UP): #오른쪽으로 가야하는 경우
                self.turnLeft()
            elif(self.orient == self.ORIENT_DOWN):
                self.turnRight()
            elif(self.orient == self.ORIENT_RIGHT):
                self.turnLeft()
                self.turnLeft()
            
        elif(-1 <= target_x - self.x and target_x - self.x <= 1):
            if(target_y - self.y > 1): #오른쪽으로 가야하는 경우
                if(self.orient == self.ORIENT_UP):
                    self.turnLeft()
                    self.turnLeft()
                elif(self.orient == self.ORIENT_LEFT):
                    self.turnLeft()
                elif(self.orient == self.ORIENT_RIGHT):
                    self.turnRight()
                
            elif(target_y - self.y < -1):
                if(self.orient == self.ORIENT_DOWN):
                    self.turnLeft()
                    self.turnLeft()
                elif(self.orient == self.ORIENT_RIGHT):
                    self.turnLeft()
                elif(self.orient == self.ORIENT_LEFT):
                    self.turnRight()
               
        #print("현재 머리 방향은", self.orient)
    
    #멧돼지를 완전히 쫓았으면 return True otherwise False
    def avoidDrone(self,target_y,target_x):
        
        if(self.x <= target_x and self.y <= target_y): return True
        #목표로 가기 위한 방향을 바라본다.
        self.checkOrientation(target_y,target_x)
        #목표로 한 번 움직인다.
        self.goStraight()
        return False
        
#Create WildBoar object(_y,_x,_index)
'''
멧돼지 객체를 만들 때 _y 좌표를 먼저 입력하는 이유
              x축
      +-----------------
      |(0,0) (0,1) (0,2)
 y축  |(1,0) (1,1) (1,2)
'''

'''
boar = WildBoar(0,2,0)
boar.goStraight()
boar.goStraight()

boar.turnLeft()
boar.goStraight()
boar.goStraight()
boar.turnRight()

print(boar.draw())
'''

