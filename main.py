# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:59:11 2019

@author: NiklasJang
"""
#Basic lib
import matplotlib.pyplot as plt
import numpy as np
import time
import random

#Class lib
import ClassWildBoar as Boar
import ClassSweetPotato as Potato

#Socket lib
from pipesocket import PipeClient
from multiprocessing import Process, Pipe
from threading import Thread

MAP_SIZE = 20
np.random.seed(int(time.time()))

def simulation(HOW_MANY_BOARS = 1,HOW_MANY_DRONES = 10):
    boar_list = []
    boar_avoid_drone_flag = []
    boar_kicked_out_flag = []
    simulation_end = True
    for i in range(HOW_MANY_BOARS):
        if(i%2 == 0):
            start_x = random.randrange(0,MAP_SIZE) 
            start_y = 0
        else :
            start_y = random.randrange(0,MAP_SIZE) 
            start_x = 0
        boar_list.append(Boar.WildBoar(start_y,start_x,i))
        boar_avoid_drone_flag.append(False)
        boar_kicked_out_flag.append(False)
    
    print(boar_list)
    
    #고구마 생성해서 고구마 맵 만들기
    amount = MAP_SIZE * MAP_SIZE * 2  #생성할 고구마의 갯수
    potatos = Potato.SweetPotato(amount) #고구마 생성
    potatos.draw() #맵에 고구마 그리기
    
    '''
    #멧돼지 생성해서 멧돼지 맵 그리기
    boar = Boar.WildBoar(5,0,0) 
    boar2 = Boar.WildBoar(0,5,0)
    '''
    
    # @Param
    # ax : axes.Axes object or array of Axes objects.
    fig, ax = plt.subplots()

    #range안에 들어가는 숫자만큼 simulation이 동작합니다.
    for tq in range(50):
        ##최종 맵에 고구마 그리기
        map_result = np.copy(potatos.map_potato)
        
        ##최종 맵에 멧돼지 그리기
        for boar in boar_list:
            map_result = boar.draw(map_result)
            
        '''
        if(드론이 멧돼지를 발견하는 조건을 넣어주시면 됩니다.) :
           boar_avoid_drone_flag[i] = True
           
        아래 i == 50은 예시입니다.
        '''
        #드론이 멧돼지를 발견
        if(tq == 20) :
            for i in range(HOW_MANY_BOARS):
                boar_avoid_drone_flag[i] = True
        
        #모든 멧돼지들이 고구마를 먹어야하는지, 도망가야하는지 판단
        for i in range(HOW_MANY_BOARS):
            if( boar_avoid_drone_flag[i] == False):
                potatos.map_potato = boar_list[i].findPotatos(potatos.map_potato)    
            else :
                #드론 경보가 울리면 집으로 가기 위해서 움직입니다. 드론의 위치는 고려하지 않고 목표 지점을 보고 직진만 합니다.
                #아래처럼 그대로 두면,
                #왼쪽에서 태어난 멧돼지면 현재 위치(경보가 울릴 때 있었던 위치)에서 계속 왼쪽으로 이동해서 사라질 겁니다.
                #위쪽에서 태어난 맷돼지면 현재 위치(경보가 울릴 때 있었던 위치)에서 계속 위쪽으로 이동해서 사라질 겁니다.
                #예를 들어서 (0,1)으로 보내기 위해서는 
                #boar2.avoidDrone(0,1)을 적으면 됩니다.
                
                #드론 경보가 울리면
                boar_list[i].state = boar_list[i].STATE_WILL_TO_RUN_OUT
                #아직 다 도망가지 않았으면
                if(boar_kicked_out_flag[i] == False):
                    #완전히 맵에서 사라지게 하기 위해서 시작 위치보다 더 멀리 달아나게 합니다.
                    #avoidDrone : 다 도망갔으면 return True, otherwise False
                    boar_kicked_out_flag[i] = boar_list[i].avoidDrone(boar_list[i].start_y - 5, boar_list[i].start_x - 5)
                else :
                    boar_list[i].state = boar_list[i].STATE_KICKED_OUT

                
        #모두 쫓으면 프로그램 종료
        for i in range(HOW_MANY_BOARS):
            simulation_end = simulation_end and boar_kicked_out_flag[i]
        if(simulation_end == True):
            break
        ax.cla() # Clear the current axes
        ax.imshow(map_result) #맵 보여주기
        ax.set_title("frame {}".format(tq))
        #plt.pause(값) 값은 매 프레임마다 기다리는 '초'를 의미합니다.  지금은 매 1초마다 프레임이 바뀝니다.
        plt.pause(0.2)

def dsim_connection(self, conn):
    HOW_MANY_BOARS = 0
    HOW_MANY_DRONES = 0
    while True:
        command = conn.recv()
        
        if command['WildeBoar'] == '1':
            HOW_MANY_BOARS = 1
        elif command['WildeBoar'] == '2':
            HOW_MANY_BOARS = 2
        elif command['WildeBoar'] == '3':
            HOW_MANY_BOARS = 3
        elif command['WildeBoar'] == '4':
            HOW_MANY_BOARS = 4
        elif command['Drone'] == '10':
            HOW_MANY_DRONES = 10
        elif command['Drone'] == '20':
            HOW_MANY_DRONES = 20
        elif command['Drone'] == '30':
            HOW_MANY_DRONES = 30
        elif command['END'] == 'END':
            break
    simulation(HOW_MANY_BOARS,HOW_MANY_DRONES)
        


def main():    
    host = '127.0.0.1'
    port = 4011
    
    #Pipe() 가 반환하는 두 개의 연결 객체는 파이프의 두 끝을 나타냅니다.
    #각 연결 객체에는 (다른 것도 있지만) send() 및 recv() 메서드가 있습니다. 
    #두 프로세스 (또는 스레드)가 파이프의 같은 끝에서 동시에 읽거나 쓰려고 하면 파이프의 데이터가 손상될 수 있습니다. 
    #물론 파이프의 다른 끝을 동시에 사용하는 프로세스로 인해 손상될 위험은 없습니다.
    parent, child = Pipe()
    
    #PipeClient는 child 객체, IP, port를 전달받아서 pipe의 한쪽 끝 역할을 해줍니다.
    #clinet는 항상 능동적으로 자신과 서버 1:1로 연결하기 때문에 bind의 과정없이 connect만 해주면 됩니다.
    #bind는 소켓을 포트와 묶는 것으로, 서버는 다수의 client를 가질 수 있기 때문에 bind의 과정이 필요합니다.
    pipeClient = PipeClient(child, host, port)
    pipeClient.start()
    
    #Dsim으로부터 연결을 받으면 시뮬레이션을 시작한다.
    proc = Thread(target=dsim_connection, args=(parent, ))
    proc.start() 
    
    pipeClient.close()
    
if __name__ == '__main__' :
    #main()
    simulation(10,0)
    
    
    
'''
#np.random.seed(19680801)

# numpy.random.random(size=None)
# @Return
# Return random floats in the half-open interval [0.0, 1.0).
# @Param
# size : int or tuple of ints, optional. Output shape.
data = np.random.random((5, 5, 5))
'''