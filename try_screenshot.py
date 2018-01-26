# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 21:11:38 2018

@author: 牧羊少年
"""
import os
import time
import random
import math
from PIL import Image

def find_piece_board():
    
    scan_start_y = 0
    scan_x_border = 200
    piece_x_sum = 0
    piece_x_c = 0
    board_x = 0
    piece_y_max = 0
    piece_body_width = 34
    os.system('del 1.png')
    os.system('adb shell screencap -p /sdcard/1.png')
    os.system('adb pull /sdcard/1.png')
    im = Image.open('./1.png')
    w,h=im.size

    for i in range(int(h/3),int(h*2/3),50): #h 为截屏图片的高度
        last_pixel = im.getpixel((0,i))
        for j in range(1,w):                #w 为截屏图片的宽度
            pixel = im.getpixel((j,i))
            if abs(pixel[0]-last_pixel[0])+abs(pixel[1]-last_pixel[1])+abs(pixel[2]-last_pixel[2])>10:
                scan_start_y = i - 50
                break   
        if scan_start_y:      #这里的scan_start_y跌在之前赋初值0
            break
            
#从scan_start_y开始往下扫描，棋子应位于屏幕的上部分，这里暂定不超过2/3
    for i in range(scan_start_y, int(h*2/3)):
        for j in range(scan_x_border, w-scan_x_border): #here scan_x_border need define value
            pixel = im.getpixel((j,i))
            if(50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] <110):
                piece_x_sum += j  #piece sum so piece_x_sum need a define value 0
                piece_x_c += 1    #piece_x_c count alse need a define value 0
                piece_y_max = max(i,piece_y_max)  #find the max piece_y --- the bottle of piece
   
    if not all((piece_x_sum, piece_x_c)):
        return 0

    piece_x = int(piece_x_sum/piece_x_c)
    piece_y = piece_y_max

# 棋盘的判断
#限制扫描的横坐标，避免音符BUG
    if piece_x < w/2:
        board_x_start = piece_x
        board_x_end = w
    else:
        board_x_start = 0
        board_x_end = piece_x
        
    for i in range(int(h/3),int(h*2/3)):
        last_pixel = im.getpixel((0,i))
        if board_x:
            break
        board_x_sum = 0
        board_x_c = 0
        
        for j in range(int(board_x_start),int(board_x_end)):
            pixel = im.getpixel((j,i))
    #过滤棋子比下一个棋盘高的情况
            if abs(j - piece_x) < piece_body_width: #piece_body_width 34要根手机屏幕得不同来测并提前赋初值
                continue
    #当圆形的时候顶部是一条线
            if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2])>10:
                board_x_sum += j  #board_x_sum 需要赋初值 0
                board_x_c += 1 # board_x_c 需要提前赋初值 0
        if board_x_sum:
            board_x = int(board_x_sum / board_x_c)

    last_pixel = im.getpixel((board_x,i)) # 从这里起i是棋盘顶点 就被征用，

    for k in range(i+427,i,-1):   #   +274 要因手机屏幕大小而定
        pixel = im.getpixel((board_x,k))
        if abs(pixel[0]-last_pixel[0]) + abs(pixel[1] - pixel[1]) + abs(pixel[2] - pixel[2]) < 10:
            break
    board_y = int((i+k)/2)

#如果上一跳命中中间 ，则下一回合就会出现白点
    for I in range(i,i+200):
        pixel = im.getpixel((board_x,I))
        if abs(pixel[0] - 245) + abs(pixel[1] - 245) + abs(pixel[2] - 245) == 0:
            board_y = I+10 #这里的+10 也要根据手机屏幕得大小来设定
            break
    if not all((board_x,board_y)):
        return 0
    print('piece_x:{},piece_y:{},board_x:{},board_y:{}'.format(piece_x,piece_y,board_x,board_y))
    return(piece_x,piece_y,board_x,board_y)

def jump(distance): 
    press_factor = 1.0
    press_time = distance * press_factor #press_factor  需要给它赋初值 按压的长度
    press_time = max(press_time,200)
    press_time = int(press_time)
    cmd = 'adb shell input swipe {} {} {} {} {}'.format(500,500,700,700,press_time)
    print(cmd)
    os.system(cmd)

def mian():
    for count in range(1,10):
        piece_x,piece_y,board_x,board_y = find_piece_board()
        jump(math.sqrt((board_x - piece_x)**2 + (board_y - piece_y)**2))
        time.sleep(random.uniform(1,1.1))
    
mian()

    
