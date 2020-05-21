import cv2
import os
import time

##手动进入抖音个人主页中的"关注"列表，开启程序即可

def aveColor(x,y,img):
     b,g,r = img[y,x]
     average = int((int(b)+int(g)+int(r))/3)
     return average
cancel_num = 0

while(True):    
     x = 902
     points = [] 
     os.system("adb shell screencap -p /sdcard/screen.png")
     os.system("adb pull /sdcard/screen.png guanzhu.png")
     img = cv2.imread(r"guanzhu.png")

     for y in range (480,2100):
          if aveColor(x,y,img) > 200 and aveColor(x,y+9,img) > 200 and aveColor(x,y-9,img) > 200:
               points.append((x,y))
    ##print(points)
     if len(points) !=0:
          for point in points:
               os.system("adb shell input mouse tap {} {}".format(point[0],point[1]))
               print("成功取关: {}".format(point))
               cancel_num = cancel_num + 1
               time.sleep(0.2)
            
        
     else:
          print("无需取关")
     os.system("adb shell input touchscreen swipe 600 1500 600 700")
     print("已经取关的个数为：{}".format(cancel_num))
     time.sleep(1)
    



     
