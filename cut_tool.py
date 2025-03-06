from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
import os
import cv2
import numpy as np
import sys
from pydub import AudioSegment
import subprocess
import webbrowser
import math

#global variable
path = os.getcwd()
working_path = path + "\\working_folder\\"

def check_margin(top_margin,bottom_margin,left_margin,right_margin):
    if not(top_margin.replace('-','').isdigit() and bottom_margin.replace('-','').isdigit() and left_margin.replace('-','').isdigit() and right_margin.replace('-','').isdigit()):
        messagebox.showerror(title="出错了！", message="边距参数有误（需整数）")
        return False
    if int(top_margin)>=200 or int(bottom_margin)>=200 or int(left_margin)>=200 or int(right_margin)>=200:
        messagebox.showerror(title="出错了！", message="边距像素数过大，请重新设置")
        return False
    return True

def check_crop(top_margin,bottom_margin,left_margin,right_margin,video_name):
    if int(top_margin)<0 or int(bottom_margin)<0 or int(left_margin)<0 or int(right_margin)<0:
        messagebox.showerror(title="出错了！", message="不能裁剪负数边距（剪暂停不影响）")
        return False
    if video_name=="aftercrop.mp4":
        messagebox.showerror(title="出错了！", message="裁剪文件名不能为aftercrop.mp4")
        return False      
    if os.path.exists(path+"/"+video_name):  
        messagebox.showerror(title="出错了！", message="上级目录已存在同文件名，请重命名")
        return False      
    return True

def check_start_end_seconds(start_second,end_second):
    if not(start_second.isdigit() and end_second.isdigit()):
        messagebox.showerror(title="出错了！", message="开始结束秒数有误（需正整数）")
        return False
    if int(start_second)>=int(end_second):            
        messagebox.showerror(title="出错了！", message="结束秒数必须大于开始秒数")
        return False
    return True

def check_file_and_return_path():      
    file_cnt = 0    
    working_folder_list = os.listdir(working_path)
    for lists in working_folder_list:
        file_cnt = file_cnt + 1
    if file_cnt==1:
        if working_folder_list[0].startswith("out"):
            messagebox.showerror(title="出错了！", message="文件名不得以out开头，请重命名") 
            return False
        return working_path + os.listdir(working_path)[0]            
    messagebox.showerror(title="出错了！", message="工作目录下文件数必须为1")
    return False
      
def check_measure_margin_second(measure_margin_second):
    if not(measure_margin_second.replace('.','',1).isdigit()):
        messagebox.showerror(title="出错了！", message="检测边距秒数有误（需大于0的数字，接受小数）")
        return False
    if not(float(measure_margin_second) > 0):
        messagebox.showerror(title="出错了！", message="检测边距秒数必须大于0")
        return False
    return True  
  
def set_margin(top_margin,bottom_margin,left_margin,right_margin):     
    e_top_margin.delete(0, END)
    e_bottom_margin.delete(0, END)
    e_left_margin.delete(0, END)  
    e_right_margin.delete(0, END)
    e_top_margin.insert(0, top_margin)
    e_bottom_margin.insert(0, bottom_margin)
    e_left_margin.insert(0, left_margin)
    e_right_margin.insert(0, right_margin)        
  
#TODO: come back later for this logic change then format
def measure_margin(measure_margin_second):  
    if check_measure_margin_second(measure_margin_second):        
        video_path=check_file_and_return_path()
        if video_path:   
            cap = cv2.VideoCapture(video_path)
            frame_cont=cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps=cap.get(cv2.CAP_PROP_FPS)
            lgt=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))       #length
            hgt=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    #height
            top_rgt_x=0
            top_rgt_y=0
            bot_lft_x=0
            bot_lft_y=0
            
            c = 0
            while c < int(fps)*float(measure_margin_second):
                ret, frame = cap.read()   
                c=c+1
            x=lgt-1
            flag=False
            while x >= 0:
                y=0
                while y <=hgt-1:
                    if(frame[y,x][2]>=90 and frame[y,x][0]<=20 and frame[y,x][1]<=20):
                        #print('here!')
                        top_rgt_x=x
                        top_rgt_y=y
                        rgt_m=lgt-1-x
                        y=y+1                        
                        #print('aaa frame[y,x] is ', y, x, frame[y,x])
                        while(not(frame[y,x][2]>=100 and frame[y,x][0]>= 100 and frame[y,x][1]>= 100)) and y<=hgt-2:
                            #print('yy frame[y,x] is ', y, x, frame[y,x])
                            y=y+1
                        #print('yyfinal frame[y,x] is ', y, x, frame[y,x])
                        bot_lft_y=y-1
                        y=top_rgt_y
                        #print('bot_lft_y is ', bot_lft_y)
                        #print('bbb frame[y,x] is ', y, x, frame[y,x])
                        while(not(frame[y,x][2]>=100 and frame[y,x][0]>= 100 and frame[y,x][1]>= 100)) and x>=1:
                            #print('xx frame[y,x] is ', y, x, frame[y,x])
                            x=x-1
                        bot_lft_x=x+1
                        #print('bot_lft_x is ', bot_lft_x)
                        #print('top_rgt_x is ', top_rgt_x)
                        flag=True
                        break                        
                    y=y+1
                if flag:
                    break
                x=x-1
            
            y=hgt-1
            bot_m = 1000 #default too big num
            while y >=0:
                x=0
                blue_cnt=0
                while x<=lgt-1:
                    if(frame[y,x][0]>=90 and frame[y,x][1]>=90 and frame[y,x][2]<=50):
                        blue_cnt=blue_cnt+1                        
                    x=x+1
                if blue_cnt/lgt < 0.25 and blue_cnt/lgt > 0.1:
                    bot_m=hgt-y-1
                    break
                y=y-1
            
            x=0
            lft_m = 1000 #default too big num
            while x<=lgt-1:
                y=0
                light_grey_cnt=0
                while y<=hgt-1:
                    #if x==0:
                    #    print('y/frame[y,x] is', y, frame[y,x])
                    if(frame[y,x][0]>=130 and frame[y,x][1]>=130 and frame[y,x][2]>=130):
                        light_grey_cnt=light_grey_cnt+1
                    y=y+1
                if light_grey_cnt/hgt < 0.25 and light_grey_cnt/hgt > 0.1:
                    #print('light_grey_cnt/x is ', light_grey_cnt,x)
                    lft_m=x
                    break
                x=x+1
                
            #print('top right x,y is ', top_rgt_x+1, top_rgt_y-2)
            #print('bot left x,y is', bot_lft_x-1, bot_lft_y+1)
            #print('lgt is, hgt is', lgt, hgt)
            
            if(top_rgt_x==bot_lft_x or top_rgt_y==bot_lft_y):
                messagebox.showerror(title="出错了！", message="计算有误，请重新输入正确的检测边距秒数（显示编队的帧）")
                return False
            else:
                #print('top_rgt_x is ', top_rgt_x)
                rgt_m=lgt-1-top_rgt_x
                top_m=math.floor(top_rgt_y-2-1/3*(bot_lft_y+1-top_rgt_y+2)) 
                #print(top_m,bot_m,lft_m,rgt_m)
                if(top_m>500 or bot_m>500 or lft_m>500 or rgt_m>500):
                    messagebox.showerror(title="出错了！", message="计算有误，请重新输入正确的检测边距秒数（显示编队的帧）")
                    return False                   
                set_margin(top_m,bot_m,lft_m,rgt_m)
                messagebox.showinfo(title="消息", message="边距已填充")
                return True
            cap.release()
        else:        
            return False
         
def cut_with_crop(start_second,end_second,measure_margin_second): 
    if check_start_end_seconds(start_second,end_second):
        if measure_margin(measure_margin_second):
            if crop(e_top_margin.get(),e_bottom_margin.get(),e_left_margin.get(),e_right_margin.get()):
                cut_without_crop(e_mode.get(),e_top_margin.get(),e_bottom_margin.get(),e_left_margin.get(),e_right_margin.get(),start_second,end_second)
 
def crop(top_margin,bottom_margin,left_margin,right_margin):
    video_path=check_file_and_return_path()
    if video_path:
        if check_margin(top_margin,bottom_margin,left_margin,right_margin):
            orig_name=os.listdir(working_path)[0]
            if check_crop(top_margin,bottom_margin,left_margin,right_margin,orig_name):
                cap = cv2.VideoCapture(video_path)
                lgt=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))     #length
                hgt=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    #height 
                cap.release()  
                out = working_path + 'aftercrop.mp4'
                W=str(lgt-int(left_margin)-int(right_margin))
                H=str(hgt-int(top_margin)-int(bottom_margin))
                X=left_margin
                Y=top_margin
                print('开始裁剪')
                subprocess.call('ffmpeg -loglevel ''quiet'' -i "'+video_path+'" -b:v 0 -vf crop='+W+':'+H+':'+X+':'+Y+' '+out,shell = True)
                os.rename(video_path,"./"+orig_name)
                print("已完成，请在working_folder下查看裁剪后的aftercrop.mp4文件，原文件已移动至上级目录")   
                set_margin(0,0,0,0)        
                return True
        
def show_desc():    
    b_show_desc.destroy()
    l3=Label(win, text="懒人模式将会自动剪掉暂停\n并且加速1倍速的部分为2倍速",font=20,height=3,width=30)
    l3_2=Label(win, text="适用于无需保留音效",font=20,width=30)
    l3_3=Label(win, text="此模式只会生成1个文件",font=20)
    l4=Label(win, text="正常模式将会自动分离暂停部分\n并且保留音效",font=20,height=3,width=30)
    l4_2=Label(win, text="适用于需要保留音效\n（注：正常模式不支持mkv格式）",font=20,width=30)
    l4_3=Label(win, text="此模式会生成较多文件",font=20)
    l3.grid(row=2)
    l3_2.grid(row=2,column=1)
    l3_3.grid(row=2,column=2)
    l4.grid(row=3)
    l4_2.grid(row=3,column=1)
    l4_3.grid(row=3,column=2)
 
def save_settings(mode_i,top_margin,bottom_margin,left_margin,right_margin):
    if check_margin(top_margin,bottom_margin,left_margin,right_margin):
        f=open(path+"/设置.txt","w+")
        f.write(str(mode_i)+"\n")
        f.write(top_margin+"\n")
        f.write(bottom_margin+"\n")
        f.write(left_margin+"\n")
        f.write(right_margin+"\n")
        f.close()
        messagebox.showinfo(title="消息", message="设置已保存")
        
def cut_without_crop(mode,top_margin,bottom_margin,left_margin,right_margin,start_second,end_second):
    if check_start_end_seconds(start_second,end_second):
        video_path=check_file_and_return_path()
        if video_path:
            cap = cv2.VideoCapture(video_path)
            frame_cont=cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps=cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            if check_margin(top_margin,bottom_margin,left_margin,right_margin):
                if(frame_cont/int(fps)<=int(end_second)):
                    messagebox.showerror(title="出错了！", message="结束秒数必须小于视频长度")  
                else:
                    if int(fps)!=fps:  #warning only not error
                        messagebox.showinfo(title="注意", message="视频帧数为非整数，可能会有剪辑问题，推荐使用其他软件重新导出为整数帧文件，点击确定或关闭窗口以继续")
                    if(mode=="懒人模式（保留有效暂停）" or mode=="懒人模式（暂停全剪）"):
                        lazy_version(video_path,mode,top_margin,bottom_margin,left_margin,right_margin,start_second,end_second)
                        print("已完成，请在working_folder下查看out.mp4文件")
                    else:  #normal mode otherwise
                        normal_version(video_path,mode,top_margin,bottom_margin,left_margin,right_margin,start_second,end_second)
                        print("已完成，请在working_folder下查看分离的mp4文件")

def jump_to_tutorial(event):
    webbrowser.open("https://www.bilibili.com/video/BV1qg411r7dV", new=0)


def lazy_version(video_path,mode,top_margin,bottom_margin,left_margin,right_margin,start_second,end_second):  
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    cap = cv2.VideoCapture(video_path)

    #settings
    frame_cont=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    lgt=cap.get(cv2.CAP_PROP_FRAME_WIDTH)       #length
    hgt=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    #height
    
    top_m=int(top_margin)    
    bot_m=int(bottom_margin)
    lft_m=int(left_margin)  
    rgt_m=int(right_margin)
    
    act_hgt=int(round(hgt-top_m-bot_m,0))
    
    act_lgt=int(round(lgt-lft_m-rgt_m,0))
    
    if act_lgt*1080<act_hgt*1920:
        mdf_hgt=int(round(act_lgt/1920*1080,0))
    else:
        mdf_hgt=act_hgt
    
    fps=int(cap.get(cv2.CAP_PROP_FPS))       #
    start_f=int(start_second)*fps#start frame (will keep frames before this)
    end_f=int(end_second)*fps  #end frame   (will keep frames after this)

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('./working_folder/out.mp4', fourcc, fps, size)

    p_m_y_co=0.074             #(right top) pause middle coefficient
    p_m_x_co=0.112
    p_l_x_co=0.125
    m_p_m_y_2_co=0.5           #this is the black point, other 3 are white point 
    m_p_m_x_2_co=0.5           
    m_p_l_y_co=0.007           #middle PAUSE
    m_p_l_x_co=0.19
    m_p_m_y_co=0.043
    m_p_r_y_co=0.023
    m_p_r_x_co=0.149
    acc_l_y_co=0.095           #accelerate
    acc_l_x_co=0.262
    acc_r_x_co=0.247
    
    vp_y_co=0.5       #valid pause
    vp_x_1_co=0.046
    vp_x_2_co=0.093
    vp_x_3_co=0.139
    vp_x_4_co=0.185
    
    vp_2_y_co=0.389   #second option to check valid pause
    vp_2_x_1_co=0.188 #wendi
    vp_2_x_2_co=0.197 #niaolong(mozu)
    vp_2_x_3_co=0.206 #m3
    vp_2_x_4_co=0.217 #panxie
    
    
    p_m_y=int(round(p_m_y_co*mdf_hgt+top_m,0))
    p_m_x=int(round(lgt-p_m_x_co*mdf_hgt-rgt_m,0))
    p_l_y=p_m_y
    p_l_x=int(round(lgt-p_l_x_co*mdf_hgt-rgt_m,0))

    m_p_m_y_2=int(round(m_p_m_y_2_co*act_hgt+top_m,0))
    m_p_m_x_2=int(round(m_p_m_x_2_co*(lgt-lft_m-rgt_m)+lft_m,0))

    m_p_l_y=int(round(m_p_m_y_2+m_p_l_y_co*mdf_hgt,0))   
    m_p_l_x=int(round(m_p_m_x_2-m_p_l_x_co*mdf_hgt,0))   
    m_p_m_y=int(round(m_p_m_y_2+m_p_m_y_co*mdf_hgt,0))
    m_p_m_x=m_p_m_x_2
    m_p_r_y=int(round(m_p_m_y_2-m_p_r_y_co*mdf_hgt,0))  
    m_p_r_x=int(round(m_p_m_x_2+m_p_r_x_co*mdf_hgt,0))  

    acc_l_y=int(round(acc_l_y_co*mdf_hgt+top_m,0))
    acc_l_x=int(round(lgt-acc_l_x_co*mdf_hgt-rgt_m,0))
    acc_r_y=acc_l_y
    acc_r_x=int(round(lgt-acc_r_x_co*mdf_hgt-rgt_m,0))
    
    vp_y=int(round(vp_y_co*act_hgt+top_m,0))
    vp_x_1=int(round(vp_x_1_co*mdf_hgt+lft_m,0))
    vp_x_2=int(round(vp_x_2_co*mdf_hgt+lft_m,0))
    vp_x_3=int(round(vp_x_3_co*mdf_hgt+lft_m,0))
    vp_x_4=int(round(vp_x_4_co*mdf_hgt+lft_m,0))
    
    vp_2_y=int(round(vp_y_co*act_hgt+top_m - (vp_y_co-vp_2_y_co)*mdf_hgt,0))
    vp_2_x_1=int(round(vp_2_x_1_co*mdf_hgt+lft_m,0))
    vp_2_x_2=int(round(vp_2_x_2_co*mdf_hgt+lft_m,0))
    vp_2_x_3=int(round(vp_2_x_3_co*mdf_hgt+lft_m,0))
    vp_2_x_4=int(round(vp_2_x_4_co*mdf_hgt+lft_m,0))
    
    #print(p_m_y, p_m_x, m_p_m_y_2, m_p_m_x_2, m_p_l_y, m_p_l_x, acc_l_y, acc_l_x, acc_r_y, acc_r_x)

    c=0
    skip=0
    pause_y_n=np.arange(0,frame_cont)
    vp_y_n=np.arange(0,frame_cont)
    
    keep_frame_y_n=np.ones(int(frame_cont))  #0 means keep, 1 means no keep
    if mode=="懒人模式（保留有效暂停）":
        while(c<frame_cont):     
            # get a frame
            ret, frame = cap.read()   
            if c<=start_f or c>=end_f:
                keep_frame_y_n[c]=0
            else:
                if not(abs(float(sum(frame[p_l_y,p_l_x])/len(frame[p_l_y,p_l_x]))-float(sum(frame[p_m_y,p_m_x])/len(frame[p_m_y,p_m_x]))) < 10 or \
                    (all(frame[m_p_l_y,m_p_l_x] > np.array([240,240,240]))\
                    and all(frame[m_p_m_y,m_p_m_x] > np.array([240,240,240]))\
                    and all(frame[m_p_r_y,m_p_r_x] > np.array([240,240,240]))) or \
                    (all(frame[m_p_m_y,m_p_m_x] > np.array([128,128,128])) \
                    and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_l_y,m_p_l_x][0])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_l_y,m_p_l_x][1])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_l_y,m_p_l_x][2])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                    and all(frame[m_p_m_y_2,m_p_m_x_2] < np.array([128,128,128])) > 30)):
                    pause_y_n[c]=1
                    vp_y_n[c]=1
                         #above means not a pause frame
                    if all(frame[acc_r_y,acc_r_x] > np.array([200,200,200])) and \
                        any(frame[acc_l_y,acc_l_x] < np.array([200,200,200])):
                        skip=skip+1
                        if(skip==1):
                            skip=-1
                        else:
                            keep_frame_y_n[c]=0
                    else:                    
                        keep_frame_y_n[c]=0
                else:
                    pause_y_n[c]=0
                    #print(c, ' is ', frame[vp_y,vp_x_1], frame[vp_y,vp_x_2], frame[vp_y,vp_x_3], frame[vp_y,vp_x_4])
                    if(((55<=frame[vp_y,vp_x_1][0]<=130 and 55<=frame[vp_y,vp_x_1][1]<=130 and 55<=frame[vp_y,vp_x_1][2]<=130) and (55<=frame[vp_y,vp_x_2][0]<=130 and 55<=frame[vp_y,vp_x_2][1]<=130 and 55<=frame[vp_y,vp_x_2][2]<=130) and (55<=frame[vp_y,vp_x_3][0]<=130 and 55<=frame[vp_y,vp_x_3][1]<=130 and 55<=frame[vp_y,vp_x_3][2]<=130) and (55<=frame[vp_y,vp_x_4][0]<=130 and 55<=frame[vp_y,vp_x_4][1]<=130 and 55<=frame[vp_y,vp_x_4][2]<=130)) or ((55<=frame[vp_y-1,vp_x_1][0]<=130 and 55<=frame[vp_y-1,vp_x_1][1]<=130 and 55<=frame[vp_y-1,vp_x_1][2]<=130) and (55<=frame[vp_y-1,vp_x_2][0]<=130 and 55<=frame[vp_y-1,vp_x_2][1]<=130 and 55<=frame[vp_y-1,vp_x_2][2]<=130) and (55<=frame[vp_y-1,vp_x_3][0]<=130 and 55<=frame[vp_y-1,vp_x_3][1]<=130 and 55<=frame[vp_y-1,vp_x_3][2]<=130) and (55<=frame[vp_y-1,vp_x_4][0]<=130 and 55<=frame[vp_y-1,vp_x_4][1]<=130 and 55<=frame[vp_y-1,vp_x_4][2]<=130)) or ((55<=frame[vp_y+1,vp_x_1][0]<=130 and 55<=frame[vp_y+1,vp_x_1][1]<=130 and 55<=frame[vp_y+1,vp_x_1][2]<=130) and (55<=frame[vp_y+1,vp_x_2][0]<=130 and 55<=frame[vp_y+1,vp_x_2][1]<=130 and 55<=frame[vp_y+1,vp_x_2][2]<=130) and (55<=frame[vp_y+1,vp_x_3][0]<=130 and 55<=frame[vp_y+1,vp_x_3][1]<=130 and 55<=frame[vp_y+1,vp_x_3][2]<=130) and (55<=frame[vp_y+1,vp_x_4][0]<=130 and 55<=frame[vp_y+1,vp_x_4][1]<=130 and 55<=frame[vp_y+1,vp_x_4][2]<=130))) \
                    and all(frame[vp_y-5,vp_x_1] < np.array([30,30,30])) \
                    or (all(frame[vp_2_y,vp_2_x_1] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_2] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_3] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_4] > np.array([240,240,240]))):
                    #or (all(frame[vp_3_y,vp_3_x_1] > np.array([240,240,240])) and 65<=frame[vp_3_y,vp_3_x_2][0]<=75 and 230<=frame[vp_3_y,vp_3_x_2][1]<=240 and 198<=frame[vp_3_y,vp_3_x_2][2]<=208):
                        vp_y_n[c]=0
                        keep_frame_y_n[c]=0
                    else:
                        vp_y_n[c]=1     
            if(c==start_f):
                print("开始分析暂停位置")
            elif(c==int(start_f + (end_f-start_f)/10)):
                print("10%")
            elif(c==int(start_f + (end_f-start_f)/10*2)):
                print("20%")
            elif(c==int(start_f + (end_f-start_f)/10*3)):
                print("30%")
            elif(c==int(start_f + (end_f-start_f)/10*4)):
                print("40%")
            elif(c==int(start_f + (end_f-start_f)/10*5)):
                print("50%")
            elif(c==int(start_f + (end_f-start_f)/10*6)):
                print("60%")
            elif(c==int(start_f + (end_f-start_f)/10*7)):
                print("70%")
            elif(c==int(start_f + (end_f-start_f)/10*8)):
                print("80%")
            elif(c==int(start_f + (end_f-start_f)/10*9)):
                print("90%")
            elif(c==end_f):
                print("100%")                   
            c=c+1
        c=1       
        while(c<frame_cont):
            if vp_y_n[c]==0 and vp_y_n[c-1]==1 and pause_y_n[c-1]==0:
                a=c-1
                while(pause_y_n[a]==0 and a>=0):
                    vp_y_n[a]=0
                    keep_frame_y_n[a]=0
                    a=a-1
                a=c+1
                while(pause_y_n[a]==0 and a<frame_cont):
                    vp_y_n[a]=0
                    keep_frame_y_n[a]=0
                    a=a+1
            c=c+1
        cap = cv2.VideoCapture(video_path)
        c=0
        while(c<frame_cont):     
            # get a frame
            ret, frame = cap.read()   
            if keep_frame_y_n[c]==0:
                out.write(frame)   
            if(c==start_f):
                print("已复制开始秒数之前的片段，开始剪掉暂停及加速")
            elif(c==int(start_f + (end_f-start_f)/10)):
                print("10%")
            elif(c==int(start_f + (end_f-start_f)/10*2)):
                print("20%")
            elif(c==int(start_f + (end_f-start_f)/10*3)):
                print("30%")
            elif(c==int(start_f + (end_f-start_f)/10*4)):
                print("40%")
            elif(c==int(start_f + (end_f-start_f)/10*5)):
                print("50%")
            elif(c==int(start_f + (end_f-start_f)/10*6)):
                print("60%")
            elif(c==int(start_f + (end_f-start_f)/10*7)):
                print("70%")
            elif(c==int(start_f + (end_f-start_f)/10*8)):
                print("80%")
            elif(c==int(start_f + (end_f-start_f)/10*9)):
                print("90%")
            elif(c==end_f):
                print("100%，正在复制结束秒数之后的片段请稍后")
            c=c+1
    elif mode=="懒人模式（暂停全剪）":        
        while(c<frame_cont):     
            # get a frame
            ret, frame = cap.read()   
            if c<=start_f or c>=end_f:
                out.write(frame)   
            else:
                if not(abs(float(sum(frame[p_l_y,p_l_x])/len(frame[p_l_y,p_l_x]))-float(sum(frame[p_m_y,p_m_x])/len(frame[p_m_y,p_m_x]))) < 10 or \
                    (all(frame[m_p_l_y,m_p_l_x] > np.array([240,240,240]))\
                    and all(frame[m_p_m_y,m_p_m_x] > np.array([240,240,240]))\
                    and all(frame[m_p_r_y,m_p_r_x] > np.array([240,240,240]))) or \
                    (all(frame[m_p_m_y,m_p_m_x] > np.array([128,128,128])) \
                    and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_l_y,m_p_l_x][0])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_l_y,m_p_l_x][1])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_l_y,m_p_l_x][2])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                    and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                    and abs(int(frame[m_p_l_y,m_p_l_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                    and all(frame[m_p_m_y_2,m_p_m_x_2] < np.array([128,128,128])) > 30)):
                    if all(frame[acc_r_y,acc_r_x] > np.array([200,200,200])) and \
                        any(frame[acc_l_y,acc_l_x] < np.array([200,200,200])):
                        skip=skip+1
                        if(skip==1):
                            skip=-1
                        else:
                            out.write(frame)
                    else:                    
                        out.write(frame)
            if(c==start_f):
                print("已复制开始秒数之前的片段，开始剪掉暂停及加速")
            elif(c==int(start_f + (end_f-start_f)/10)):
                print("10%")
            elif(c==int(start_f + (end_f-start_f)/10*2)):
                print("20%")
            elif(c==int(start_f + (end_f-start_f)/10*3)):
                print("30%")
            elif(c==int(start_f + (end_f-start_f)/10*4)):
                print("40%")
            elif(c==int(start_f + (end_f-start_f)/10*5)):
                print("50%")
            elif(c==int(start_f + (end_f-start_f)/10*6)):
                print("60%")
            elif(c==int(start_f + (end_f-start_f)/10*7)):
                print("70%")
            elif(c==int(start_f + (end_f-start_f)/10*8)):
                print("80%")
            elif(c==int(start_f + (end_f-start_f)/10*9)):
                print("90%")
            elif(c==end_f):
                print("100%，正在复制结束秒数之后的片段请稍后")
            c=c+1
    cap.release()
    cv2.destroyAllWindows()

def normal_version(video_path,mode,top_margin,bottom_margin,left_margin,right_margin,start_second,end_second): 

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    cap = cv2.VideoCapture(video_path)
    
    #settings
    frame_cont=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    lgt=cap.get(cv2.CAP_PROP_FRAME_WIDTH)       #length
    hgt=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    #height
    
    top_m=int(top_margin)    
    bot_m=int(bottom_margin)
    lft_m=int(left_margin)  
    rgt_m=int(right_margin)
    
    act_hgt=int(round(hgt-top_m-bot_m,0))
    
    act_lgt=int(round(lgt-lft_m-rgt_m,0))
    
    if act_lgt*1080<act_hgt*1920:
        mdf_hgt=int(round(act_lgt/1920*1080,0))
    else:
        mdf_hgt=act_hgt
        
    fps=int(cap.get(cv2.CAP_PROP_FPS))       #
    start_f=int(start_second)*fps#start frame (will keep frames before this)
    end_f=int(end_second)*fps  #end frame   (will keep frames after this)

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    p_m_y_co=0.074             #(right top) pause middle coefficient
    p_m_x_co=0.112
    p_l_x_co=0.125
    m_p_m_y_2_co=0.5           #this is the black point, other 3 are white point 
    m_p_m_x_2_co=0.5           
    m_p_l_y_co=0.007           #middle PAUSE
    m_p_l_x_co=0.19
    m_p_m_y_co=0.043
    m_p_r_y_co=0.023
    m_p_r_x_co=0.149
    
    vp_y_co=0.5       #valid pause
    vp_x_1_co=0.046
    vp_x_2_co=0.093
    vp_x_3_co=0.139
    vp_x_4_co=0.185
    
    vp_2_y_co=0.389   #second option to check valid pause
    vp_2_x_1_co=0.188 #wendi
    vp_2_x_2_co=0.197 #niaolong(mozu)
    vp_2_x_3_co=0.206 #m3
    vp_2_x_4_co=0.217 #panxie
    
    #vp_3_y_co=0.669   #third option to check valid pause (just before click skill)
    #vp_3_x_1_co=0.121 #from middle point (white)
    #vp_3_x_2_co=0.140 #(green)

    p_m_y=int(round(p_m_y_co*mdf_hgt+top_m,0))
    p_m_x=int(round(lgt-p_m_x_co*mdf_hgt-rgt_m,0))
    p_l_y=p_m_y
    p_l_x=int(round(lgt-p_l_x_co*mdf_hgt-rgt_m,0))

    m_p_m_y_2=int(round(m_p_m_y_2_co*act_hgt+top_m,0))
    m_p_m_x_2=int(round(m_p_m_x_2_co*(lgt-lft_m-rgt_m)+lft_m,0))

    m_p_l_y=int(round(m_p_m_y_2+m_p_l_y_co*mdf_hgt,0))   
    m_p_l_x=int(round(m_p_m_x_2-m_p_l_x_co*mdf_hgt,0))   
    m_p_m_y=int(round(m_p_m_y_2+m_p_m_y_co*mdf_hgt,0))
    m_p_m_x=m_p_m_x_2
    m_p_r_y=int(round(m_p_m_y_2-m_p_r_y_co*mdf_hgt,0))  
    m_p_r_x=int(round(m_p_m_x_2+m_p_r_x_co*mdf_hgt,0))

    vp_y=int(round(vp_y_co*act_hgt+top_m,0))
    vp_x_1=int(round(vp_x_1_co*mdf_hgt+lft_m,0))
    vp_x_2=int(round(vp_x_2_co*mdf_hgt+lft_m,0))
    vp_x_3=int(round(vp_x_3_co*mdf_hgt+lft_m,0))
    vp_x_4=int(round(vp_x_4_co*mdf_hgt+lft_m,0))
    
    vp_2_y=int(round(vp_y_co*act_hgt+top_m - (vp_y_co-vp_2_y_co)*mdf_hgt,0))
    vp_2_x_1=int(round(vp_2_x_1_co*mdf_hgt+lft_m,0))
    vp_2_x_2=int(round(vp_2_x_2_co*mdf_hgt+lft_m,0))
    vp_2_x_3=int(round(vp_2_x_3_co*mdf_hgt+lft_m,0))
    vp_2_x_4=int(round(vp_2_x_4_co*mdf_hgt+lft_m,0))
    
    #vp_3_y=int(round(vp_3_y_co*mdf_hgt+top_m,0))
    #vp_3_x_1=int(round(vp_3_x_1_co*mdf_hgt+lft_m+0.5*(lgt-lft_m-rgt_m),0))
    #vp_3_x_2=int(round(vp_3_x_2_co*mdf_hgt+lft_m+0.5*(lgt-lft_m-rgt_m),0))
    
    #print(vp_y, vp_x_1,vp_x_2,vp_x_3,vp_x_4)
    #print(act_hgt, mdf_hgt)
    #print(p_m_y, p_m_x, m_p_l_y, m_p_l_x, vp_y, vp_x_1, vp_x_4, vp_2_y, vp_2_x_1, vp_2_x_4)
#68 1522 546 638 540 42 169 439 172 198 611 923 940  -- print
    c=0
    pause_y_n=np.arange(0,frame_cont)
    vp_y_n=np.arange(0,frame_cont)
    while(c<frame_cont):
        # get a frame
        ret, frame = cap.read()
        #print(frame[vp_2_y,vp_2_x_3])
        if c<=start_f or c>=end_f:
            pause_y_n[c]=1
            vp_y_n[c]=1
        else:
            if not(abs(float(sum(frame[p_l_y,p_l_x])/len(frame[p_l_y,p_l_x]))-float(sum(frame[p_m_y,p_m_x])/len(frame[p_m_y,p_m_x]))) < 10 or \
                (all(frame[m_p_l_y,m_p_l_x] > np.array([240,240,240]))\
                and all(frame[m_p_m_y,m_p_m_x] > np.array([240,240,240]))\
                and all(frame[m_p_r_y,m_p_r_x] > np.array([240,240,240]))) or \
                (all(frame[m_p_m_y,m_p_m_x] > np.array([128,128,128])) \
                and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_l_y,m_p_l_x][0])) < 30 \
                and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_l_y,m_p_l_x][1])) < 30 \
                and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_l_y,m_p_l_x][2])) < 30 \
                and abs(int(frame[m_p_m_y,m_p_m_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                and abs(int(frame[m_p_m_y,m_p_m_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                and abs(int(frame[m_p_m_y,m_p_m_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                and abs(int(frame[m_p_l_y,m_p_l_x][0])-int(frame[m_p_r_y,m_p_r_x][0])) < 30 \
                and abs(int(frame[m_p_l_y,m_p_l_x][1])-int(frame[m_p_r_y,m_p_r_x][1])) < 30 \
                and abs(int(frame[m_p_l_y,m_p_l_x][2])-int(frame[m_p_r_y,m_p_r_x][2])) < 30 \
                and all(frame[m_p_m_y_2,m_p_m_x_2] < np.array([128,128,128])) > 30)):
                    pause_y_n[c]=1
                    vp_y_n[c]=1
                         #above means not a pause frame
            else:
                pause_y_n[c]=0
                if(((55<=frame[vp_y,vp_x_1][0]<=130 and 55<=frame[vp_y,vp_x_1][1]<=130 and 55<=frame[vp_y,vp_x_1][2]<=130) and (55<=frame[vp_y,vp_x_2][0]<=130 and 55<=frame[vp_y,vp_x_2][1]<=130 and 55<=frame[vp_y,vp_x_2][2]<=130) and (55<=frame[vp_y,vp_x_3][0]<=130 and 55<=frame[vp_y,vp_x_3][1]<=130 and 55<=frame[vp_y,vp_x_3][2]<=130) and (55<=frame[vp_y,vp_x_4][0]<=130 and 55<=frame[vp_y,vp_x_4][1]<=130 and 55<=frame[vp_y,vp_x_4][2]<=130)) or ((55<=frame[vp_y-1,vp_x_1][0]<=130 and 55<=frame[vp_y-1,vp_x_1][1]<=130 and 55<=frame[vp_y-1,vp_x_1][2]<=130) and (55<=frame[vp_y-1,vp_x_2][0]<=130 and 55<=frame[vp_y-1,vp_x_2][1]<=130 and 55<=frame[vp_y-1,vp_x_2][2]<=130) and (55<=frame[vp_y-1,vp_x_3][0]<=130 and 55<=frame[vp_y-1,vp_x_3][1]<=130 and 55<=frame[vp_y-1,vp_x_3][2]<=130) and (55<=frame[vp_y-1,vp_x_4][0]<=130 and 55<=frame[vp_y-1,vp_x_4][1]<=130 and 55<=frame[vp_y-1,vp_x_4][2]<=130)) or ((55<=frame[vp_y+1,vp_x_1][0]<=130 and 55<=frame[vp_y+1,vp_x_1][1]<=130 and 55<=frame[vp_y+1,vp_x_1][2]<=130) and (55<=frame[vp_y+1,vp_x_2][0]<=130 and 55<=frame[vp_y+1,vp_x_2][1]<=130 and 55<=frame[vp_y+1,vp_x_2][2]<=130) and (55<=frame[vp_y+1,vp_x_3][0]<=130 and 55<=frame[vp_y+1,vp_x_3][1]<=130 and 55<=frame[vp_y+1,vp_x_3][2]<=130) and (55<=frame[vp_y+1,vp_x_4][0]<=130 and 55<=frame[vp_y+1,vp_x_4][1]<=130 and 55<=frame[vp_y+1,vp_x_4][2]<=130))) \
                and all(frame[vp_y-5,vp_x_1] < np.array([30,30,30])) \
                or (all(frame[vp_2_y,vp_2_x_1] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_2] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_3] > np.array([240,240,240])) or all(frame[vp_2_y,vp_2_x_4] > np.array([240,240,240]))):
                #or (all(frame[vp_3_y,vp_3_x_1] > np.array([240,240,240])) and 65<=frame[vp_3_y,vp_3_x_2][0]<=75 and 230<=frame[vp_3_y,vp_3_x_2][1]<=240 and 198<=frame[vp_3_y,vp_3_x_2][2]<=208):
                    vp_y_n[c]=0
                else:
                    vp_y_n[c]=1
                #print(c, ' is ', frame[vp_y,vp_x_1], frame[vp_y,vp_x_2], frame[vp_y,vp_x_3], frame[vp_y,vp_x_4], frame[vp_y-5,vp_x_1], ', vp_y_n is ', vp_y_n[c])
                #print('  ', c, ' is ', frame[vp_y-1,vp_x_1], frame[vp_y-1,vp_x_2], frame[vp_y-1,vp_x_3], frame[vp_y-1,vp_x_4])
                #print('  ', c, ' is ', frame[vp_y+1,vp_x_1], frame[vp_y+1,vp_x_2], frame[vp_y+1,vp_x_3], frame[vp_y+1,vp_x_4])
        
        if(c==start_f):
            print("开始分析暂停位置")
        elif(c==int(start_f + (end_f-start_f)/10)):
            print("10%")
        elif(c==int(start_f + (end_f-start_f)/10*2)):
            print("20%")
        elif(c==int(start_f + (end_f-start_f)/10*3)):
            print("30%")
        elif(c==int(start_f + (end_f-start_f)/10*4)):
            print("40%")
        elif(c==int(start_f + (end_f-start_f)/10*5)):
            print("50%")
        elif(c==int(start_f + (end_f-start_f)/10*6)):
            print("60%")
        elif(c==int(start_f + (end_f-start_f)/10*7)):
            print("70%")
        elif(c==int(start_f + (end_f-start_f)/10*8)):
            print("80%")
        elif(c==int(start_f + (end_f-start_f)/10*9)):
            print("90%")
        elif(c==end_f):
            print("100%")
        c=c+1        
    
    
    #with open('./abc.txt','a+') as f:
        #print('pause_y_n start',file=f)
        #for x in pause_y_n:
            #print(x,file=f)
        #print('pause_y_n end',file=f)
    #with open('./abc.txt','a+') as f:
        #print('vp_y_n start',file=f)
        #for x in vp_y_n:
            #print(x,file=f)
        #print('vp_y_n end',file=f)
 #    while(c<frame_cont):
#        if vp_y_n[c]==0 and vp_y_n[c-1]==1 and pause_y_n[c-1]==0:
#            a=c-2
#            vp_y_n[c-1]=0
#            while(a>=0):
#                if pause_y_n[a]==1:
#                    vp_y_n[a+1]=0
#                    vp_y_n[a]=1
#                    break
#                else:
#                    vp_y_n[a]=0
#                a=a-1
#        c=c+1       
    c=1       
    while(c<frame_cont):
        if vp_y_n[c]==0 and vp_y_n[c-1]==1 and pause_y_n[c-1]==0:
            a=c-1
            while(pause_y_n[a]==0 and a>=0):
                vp_y_n[a]=0
                a=a-1
            a=c+1
            while(pause_y_n[a]==0 and a<frame_cont):
                vp_y_n[a]=0
                a=a+1
        c=c+1
        
    #c=1       
    #while(c<frame_cont):
        #if vp_y_n[c-1]==0 and pause_y_n[c]==1:
            #print("c is ",c)
            #a=c-1
            #while(pause_y_n[a]==0 and a>=0):
                #print("vp_y_n[",a,"] has changed to 1")
                #vp_y_n[a]=1
                #a=a-1
        #c=c+1
    
    #with open('./abc.txt','a+') as f:
    #    print('-----------------------',file=f)
    #    print('vp_y_n start',file=f)
    #    for x in vp_y_n:
    #        print(x,file=f)
    #    print('vp_y_n end',file=f)
    
    
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    cap = cv2.VideoCapture(video_path)
    sound_ind = 1
    try:
        sound = AudioSegment.from_file(video_path, format=os.path.splitext(video_path)[-1].split(".")[1])    
    except:
        sound_ind = 0
    #print("sound_ind is ", sound_ind)
    index=0    
    vp=''
    if vp_y_n[0]==0:
        vp='有效暂停'
    elif pause_y_n[0]==0:
        vp='无效暂停'
    else:
        vp=''
    out = cv2.VideoWriter('./working_folder/out_'+str(index)+vp+'.mp4', fourcc, fps, size)
    start_time=0
    stop_time=0
    inc=1/fps*1000
    check=0
    c=0

            #stop_time=inc
            #stop_time=stop_time+inc

            #word=sound[start_time:stop_time+fps]
            #word.export('./working_folder/out_'+str(index)+'.mp3')
            #start_time=stop_time

    while(c<frame_cont-1):
        # get a frame
        ret, frame = cap.read()
        if c==0:
            out.write(frame)
            stop_time=inc
        elif pause_y_n[c]==pause_y_n[c-1]:
            check=0
            out.write(frame)
            stop_time=stop_time+inc
        elif pause_y_n[c]!=pause_y_n[c-1] and pause_y_n[c+1]!=pause_y_n[c]:
            if check==1:
                out.write(frame)
                stop_time=stop_time+inc
            else:
                out.release()
                if vp_y_n[int(round(start_time/inc,0))]==0:
                    vp='有效暂停'
                elif pause_y_n[int(round(start_time/inc,0))]==0:
                    vp='无效暂停'
                else:
                    vp=''
                if(sound_ind):
                    word=sound[start_time:stop_time+fps]
                    word.export('./working_folder/out_'+str(index)+vp+'.mp3')
                    #print("first part start_time to stop_time is ", start_time, " ", stop_time)
                start_time=stop_time
                index=index+1
                if vp_y_n[c]==0:
                    vp='有效暂停'
                elif pause_y_n[c]==0:
                    vp='无效暂停'
                else:
                    vp=''
                out = cv2.VideoWriter('./working_folder/out_'+str(index)+vp+'.mp4', fourcc, fps, size)
                out.write(frame)
                stop_time=stop_time+inc
                out.release()
                if(sound_ind):
                    word=sound[start_time:stop_time+fps]            
                    word.export('./working_folder/out_'+str(index)+vp+'.mp3')
                    #print("second part start_time to stop_time is ", start_time, " ", stop_time)
                start_time=stop_time
                index=index+1
                if vp_y_n[c+1]==0:
                    vp='有效暂停'
                elif pause_y_n[c+1]==0:
                    vp='无效暂停'
                else:
                    vp=''
                out = cv2.VideoWriter('./working_folder/out_'+str(index)+vp+'.mp4', fourcc, fps, size)
                check=1
        else:
            if check==1:
                out.write(frame)
                stop_time=stop_time+inc
            else:
                check=0
                out.release()
                if vp_y_n[int(round(start_time/inc,0))]==0:
                    vp='有效暂停'
                elif pause_y_n[int(round(start_time/inc,0))]==0:
                    vp='无效暂停'
                else:
                    vp=''
                if(sound_ind):
                    word=sound[start_time:stop_time+fps]            
                    word.export('./working_folder/out_'+str(index)+vp+'.mp3')
                    #print("third part start_time to stop_time is ", start_time, " ", stop_time)
                start_time=stop_time
                index=index+1
                if vp_y_n[c]==0:
                    vp='有效暂停'
                elif pause_y_n[c]==0:
                    vp='无效暂停'
                else:
                    vp=''
                out = cv2.VideoWriter('./working_folder/out_'+str(index)+vp+'.mp4', fourcc, fps, size)
                out.write(frame)
                stop_time=stop_time+inc
        if(c==start_f):
            print("已复制开始秒数之前的片段，继续生成分离片段")
        elif(c==int(start_f + (end_f-start_f)/10)):
            print("10%")
        elif(c==int(start_f + (end_f-start_f)/10*2)):
            print("20%")
        elif(c==int(start_f + (end_f-start_f)/10*3)):
            print("30%")
        elif(c==int(start_f + (end_f-start_f)/10*4)):
            print("40%")
        elif(c==int(start_f + (end_f-start_f)/10*5)):
            print("50%")
        elif(c==int(start_f + (end_f-start_f)/10*6)):
            print("60%")
        elif(c==int(start_f + (end_f-start_f)/10*7)):
            print("70%")
        elif(c==int(start_f + (end_f-start_f)/10*8)):
            print("80%")
        elif(c==int(start_f + (end_f-start_f)/10*9)):
            print("90%")
        elif(c==end_f):
            print("100%，正在复制结束秒数之后的片段请稍后")
        c=c+1

    out.release()
    if vp_y_n[int(round(start_time/inc,0))]==0:
        vp='有效暂停'
    elif pause_y_n[int(round(start_time/inc,0))]==0:
        vp='无效暂停'
    else:
        vp=''
    
    if(sound_ind):
        word=sound[start_time:stop_time+fps]
        word.export('./working_folder/out_'+str(index)+vp+'.mp3')                 
        #print("last part start_time to stop_time is ", start_time, " ", stop_time)
        
    cap.release()
    cv2.destroyAllWindows()
    
  

    file_dir="./working_folder/"
    list=os.listdir(file_dir)
    list.sort(key=lambda fn: os.path.getmtime(file_dir+fn) if not os.path.isdir(file_dir+fn) else 0)

    count=int(list[-1].split("_")[1].split(".")[0])
    #print("片段数量为",count)
    i=0
    while(i<=count):
        j=pow(10,len(str(count)))+i
        if(sound_ind):
            subprocess.call('ffmpeg -loglevel ''quiet'' -i '+file_dir+"out_"+str(i)+".mp4"+' -i '+file_dir+"out_"+str(i)+".mp3"+' -c:v copy -c:a aac '+file_dir+str(j)+".mp4",shell = True)
            subprocess.call('ffmpeg -loglevel ''quiet'' -i '+file_dir+"out_"+str(i)+"有效暂停.mp4"+' -i '+file_dir+"out_"+str(i)+"有效暂停.mp3"+' -c:v copy -c:a aac '+file_dir+str(j)+"有效暂停.mp4",shell = True)
            if(mode=="正常模式（保留无效暂停视频）"):
                subprocess.call('ffmpeg -loglevel ''quiet'' -i '+file_dir+"out_"+str(i)+"无效暂停.mp4"+' -i '+file_dir+"out_"+str(i)+"无效暂停.mp3"+' -c:v copy -c:a aac '+file_dir+str(j)+"无效暂停.mp4",shell = True)
            else:    
                try:
                    os.rename(file_dir+"out_"+str(i)+"无效暂停.mp3",file_dir+str(j)+"无效暂停.mp3")
                except:
                    dummy=0                
            if(i==0):
                print("开始合并音频视频片段")
            elif(i==int(count/10)):
                print("10%")
            elif(i==int(count/10*2)):
                print("20%")
            elif(i==int(count/10*3)):
                print("30%")
            elif(i==int(count/10*4)):
                print("40%")
            elif(i==int(count/10*5)):
                print("50%")
            elif(i==int(count/10*6)):
                print("60%")
            elif(i==int(count/10*7)):
                print("70%")
            elif(i==int(count/10*8)):
                print("80%")
            elif(i==int(count/10*9)):
                print("90%")
            elif(i==count):
                print("100%，正在清理片段请稍后")
            i=i+1
        else:
            try:
                os.rename(file_dir+"out_"+str(i)+".mp4",file_dir+str(j)+".mp4")
            except:
                dummy=0
            try:
                os.rename(file_dir+"out_"+str(i)+"有效暂停.mp4",file_dir+str(j)+"有效暂停.mp4")
            except:
                dummy=0   
            if(mode=="正常模式（保留无效暂停视频）"):
                try:
                    os.rename(file_dir+"out_"+str(i)+"无效暂停.mp4",file_dir+str(j)+"无效暂停.mp4")
                except:
                    dummy=0              
            if(i==0):
                print("视频未检测出音频，仅重命名")
            elif(i==int(count/10)):
                print("10%")
            elif(i==int(count/10*2)):
                print("20%")
            elif(i==int(count/10*3)):
                print("30%")
            elif(i==int(count/10*4)):
                print("40%")
            elif(i==int(count/10*5)):
                print("50%")
            elif(i==int(count/10*6)):
                print("60%")
            elif(i==int(count/10*7)):
                print("70%")
            elif(i==int(count/10*8)):
                print("80%")
            elif(i==int(count/10*9)):
                print("90%")
            elif(i==count):
                print("100%，重命名完成")
            i=i+1
    if(sound_ind):       
        for root , dirs, files in os.walk(working_path):
            for name in files:
                if name.startswith("out"):
                    os.remove(os.path.join(root, name))   

# main here

# 创建窗口
win = Tk()
# 设置窗口标题
win.title('明日方舟自动分离/剪掉暂停')

# 设置窗口宽度和高度
win.geometry(str(1100+len(path.encode('utf-8'))*5)+'x850')  
    
l_text_working_path=Label(win, text="当前工作目录",font=20,height=3)
l_working_path=Label(win, text=working_path, bg="lightgrey",font=20,height=3)

l_mode=Label(win, text="选择模式",font=20,height=3)
e_mode=ttk.Combobox(win,font=20,height=4,width=28)
e_mode['value']=("正常模式（仅保留无效暂停音效）","正常模式（保留无效暂停视频）","懒人模式（保留有效暂停）","懒人模式（暂停全剪）")
win.option_add('*TCombobox*Listbox.font',20)
e_mode.current(0) #give default
b_show_desc=Button(win, text="显示说明", command=show_desc,font=20)

l_top_margin=Label(win, text="上边距（像素数）",font=20,height=2)
e_top_margin=Entry(win, bg="white",font=20)
        
l_bottom_margin=Label(win, text="下边距",font=20,height=2)
e_bottom_margin=Entry(win, bg="white",font=20) 

l_left_margin=Label(win, text="左边距",font=20,height=2)
e_left_margin=Entry(win, bg="white",font=20)

l_right_margin=Label(win, text="右边距",font=20,height=2)
e_right_margin=Entry(win, bg="white",font=20)

b_save_settings=Button(win, text="保存设置", command=lambda: save_settings(e_mode.current(),e_top_margin.get(),e_bottom_margin.get(),e_left_margin.get(),e_right_margin.get()), font=20)

l_measure_margin_second=Label(win, text="检测边距秒数",font=20,height=2)
e_measure_margin_second=Entry(win, bg="white",font=20)

b_measure_margin=Button(win, text="检测边距", command=lambda: measure_margin(e_measure_margin_second.get()),font=20)
b_crop=Button(win, text="按边距裁剪（边距将被重置为0）", command=lambda: crop(e_top_margin.get(),e_bottom_margin.get(),e_left_margin.get(),e_right_margin.get()),font=20)

l_start_second=Label(win, text="开始秒数",font=20,height=2)
e_start_second=Entry(win, bg="white",font=20)

l_end_second=Label(win, text="结束秒数",font=20,height=2)
e_end_second=Entry(win, bg="white",font=20)

b_cut_without_crop=Button(win, text="点击开始自动分离/剪掉暂停（不包含边距裁剪）", command=lambda: cut_without_crop(e_mode.get(),e_top_margin.get(),e_bottom_margin.get(),e_left_margin.get(),e_right_margin.get(),e_start_second.get(),e_end_second.get()),font=20)
b_cut_with_crop=Button(win, text="点击开始自动分离/剪掉暂停（包含边距裁剪）", command=lambda: cut_with_crop(e_start_second.get(),e_end_second.get(),e_measure_margin_second.get()),font=20)

l_tutorial=Label(win, text="详细操作教程：",font=20,height=2)

ft = tkFont.Font(family = 'Fixdsys',size = 11,weight = tkFont.NORMAL, underline=1)  
l_tutorial_url=Label(win, text="www.bilibili.com/video/BV1qg411r7dV",font=ft,fg="blue",height=2)
l_tutorial_url.bind("<ButtonPress-1>", jump_to_tutorial)  

l_text_working_path.grid(row=0)
l_working_path.grid(row=0,column=1)
l_mode.grid(row=1)
e_mode.grid(row=1,column=1)
b_show_desc.grid(row=1,column=2)

l_top_margin.grid(row=4)
e_top_margin.grid(row=4,column=1)
l_bottom_margin.grid(row=5)
e_bottom_margin.grid(row=5,column=1)
l_left_margin.grid(row=6)
e_left_margin.grid(row=6,column=1)
l_right_margin.grid(row=7)
e_right_margin.grid(row=7,column=1)

b_save_settings.grid(row=8)

l_measure_margin_second.grid(row=9)
e_measure_margin_second.grid(row=9,column=1)
b_measure_margin.grid(row=10)
b_crop.grid(row=10,column=1)

l_start_second.grid(row=11)
e_start_second.grid(row=11,column=1)
l_end_second.grid(row=12)
e_end_second.grid(row=12,column=1)

b_cut_without_crop.grid(row=13,column=0)
b_cut_with_crop.grid(row=13,column=1)
l_tutorial_url.grid(row=14,column=0)
l_tutorial_url.grid(row=14,column=1)       

if os.path.exists(path+"/设置.txt"):
    f = open(path+"/设置.txt")
    e_mode.current(int(f.readline()))
    set_margin(int(f.readline()),int(f.readline()),int(f.readline()),int(f.readline()))
    f.close()  
    
# 主循环
win.mainloop()