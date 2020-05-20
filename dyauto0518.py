import cv2
import os
import time
import random
import numpy as np
import threading


##adb_device = "127.0.0.1:5555"
adb_device = "HJS5T19117003929"

#HUAWEI MATE20 Physical Phone:HJS5T19117003929
coordinates = {
     "portal_portal":(105,2045),#首页回到首页选项卡按钮
     "portal_me":(971,2045),# 首页进入号主个人页按钮
     "portal_livevideo":(98,150),#首页进入直播间按钮
     "myprofile_enterfanslist":(696,1106), #号主个人页面到粉丝列表入口按钮
     "fans_list_icon_distance":200, #两个粉丝头像顶点之间的距离
     "fans_list_icon_column_x":140,#粉丝列表页粉丝头像排列位置：x坐标。用于识别粉丝头像时。
     "fans_list_icon_y_range":(370,2080),#粉丝头像纵向显示范围
     "fans_profile_videolist_y":1700, #粉丝个人页，需要随机点击的视频的y坐标（上下位置）
     "fans_profile_videolist_3x":(187,510,890), #粉丝个人页，需要随机点击视频的横向三个视频的x坐标
     "videoplay_comment_field":(200,2049),#视频播放页：评论框
     "comment_page_edit_field":(200,975),#评论页：评论编辑框
     "comment_page_submit":(1002,975),#评论页：评论提交按钮
     "videoplay_favor_icon":(985,1105),#视频播放页：点赞心形
     "livevideo_rank_entry":(1000,150),#直播页：粉丝榜单入口
     "rank_redcross_column_x":180,#榜单页：加粉丝"红十字"图标"左右"位置
     "rank_redcross_column_y_range":(1000,2120),#榜单页：加粉丝"红十字"图标"上下"显示范围
     "red_cross_y_delta_up":14,       ##huawei mate20:上：14，下14；模拟器1440x900：上8，下9
     "red_cross_y_delta_down":14,         ##huawei mate20:上：14，下14；模拟器1440x900：上8，下9
 }
# simulator: 127.0.0.1:5555
##coordinates = {
##    "portal_portal":(92,1383),#首页回到首页选项卡按钮
##    "portal_me":(807,1384),# 首页进入号主个人页按钮
##    "portal_livevideo":(67,96),#首页进入直播间按钮
##    "myprofile_enterfanslist":(436,807), #号主个人页面到粉丝列表入口按钮
##    "fans_list_icon_distance":155, #两个粉丝头像顶点之间的距离
##    "fans_list_icon_column_x":92,#粉丝列表页粉丝头像排列位置：x坐标。用于识别粉丝头像时。
##    "fans_list_icon_y_range":(362,1414),#粉丝头像纵向显示范围
##    "fans_profile_videolist_y":1316, #粉丝个人页，需要随机点击的视频的y坐标（上下位置）
##    "fans_profile_videolist_3x":(168,448,682), #粉丝个人页，需要随机点击视频的横向三个视频的x坐标
##    "videoplay_comment_field":(172,1383),#视频播放页：评论框
##    "comment_page_edit_field":(108,1227),#评论页：评论编辑框
##    "comment_page_submit":(846,1223),#评论页：评论提交按钮
##    "videoplay_favor_icon":(837,755),#视频播放页：点赞心形
##    "livevideo_rank_entry":(793,57),#直播页：粉丝榜单入口
##    "rank_redcross_column_x":119,#榜单页：加粉丝"红十字"图标"左右"位置
##    "rank_redcross_column_y_range":(442,953),#榜单页：加粉丝"红十字"图标"上下"显示范围
##    "red_cross_y_delta_up":8,       ##huawei mate20:上：14，下14；模拟器1440x900：上8，下9
##    "red_cross_y_delta_down":9,         ##huawei mate20:上：14，下14；模拟器1440x900：上8，下9
##    "light_screen":(468,480), #点击屏幕，使屏幕由暗变亮
##
##}

flag_list = [

    "/Users/wyg/projects/tiktok/flags/livevideo_flag.jpg", #直播页-0
    "/Users/wyg/projects/tiktok/flags/videoplay_flag.jpg",  # 视频播放页-1
    "/Users/wyg/projects/tiktok/flags/fanslist_flag.jpg",  # 粉丝列表页-2
     "/Users/wyg/projects/tiktok/flags/fansprofile_flag.jpg", #粉丝个人页-3
     "/Users/wyg/projects/tiktok/flags/comment_flag.jpg" ,#评论页-4
     "/Users/wyg/projects/tiktok/flags/rank_flag.jpg" ,#榜单页-5
    "/Users/wyg/projects/tiktok/flags/personprofile_flag.jpg",  # 号主个人信息页-6
     "/Users/wyg/projects/tiktok/flags/zerowork_flag.jpg" ,#零作品页-7
    "/Users/wyg/projects/tiktok/flags/portal_flag.jpg",  # 抖音开场主页-8
    "/Users/wyg/projects/tiktok/flags/liveoff_flag.jpg",  # 直播结束页-9
    #"/Users/wyg/projects/tiktok/flags/message_flag.jpg",  # 个人消息页-10
   # "/Users/wyg/projects/tiktok/flags/camera_flag.jpg",  # 视频拍摄页-11
]

comment_list = [
    "Excellent~",
    "Amazing~",
    "Adorable~",
    "Awesome~",
    "Nice~",
    "Wonderful~",
    "you turns me on..",
    ]

match_factor = 0.55 ####****图像匹配系数，系数越小匹配越苛刻
comment_flag = 2
livevideo_flag =2
flag_lables = ["直播","视频播放","粉丝列表","粉丝个人","评论","榜单","号主个人","零作品","开场首页","直播结束","个人消息","拍视频","未知页面"]
##flag_threshold_scores =[320,800,800,1000,1800,1000,1800,1600,500,2000,2500,1300,] ##最关键的数据，经过反复更改靶图和调试得出
flag_threshold_scores =[320,800,800,1000,1800,1000,1800,1600,500,2000,] ##最关键的数据，经过反复更改靶图和调试得出
unknown_page_list = []

def getColorAverage(img,y,x):#计算像素颜色平均值
    b,g,r = img[y,x]
    aveValue = int((int(b) + int(g) + int(r))/3)
    return aveValue

def get_fans_icon():
    os.system("adb -s {} shell screencap -p /sdcard/screen_fans.png".format(adb_device))
    os.system("adb pull /sdcard/screen_fans.png screen_fans.png")
    img = cv2.imread("screen_fans.png")
    points = []
    x = coordinates["fans_list_icon_column_x"]
    y = coordinates["fans_list_icon_y_range"][0]
    while(y < coordinates["fans_list_icon_y_range"][1]):
        if getColorAverage(img,y,x) > 27: #关注页面背景像素BGR平均值
            points.append((x,y))
            y = y + coordinates["fans_list_icon_distance"]
        else:
            y = y + 1

    return(points)

def getCross(img,y,x): ##获取关注"+"图标。注意： img是已经读取后的图片数据
    center =  bool( 252<=getColorAverage(img,y,x) <= 255)
    up = bool( 120<=getColorAverage(img,y-coordinates["red_cross_y_delta_up"],x) <= 132)
    down = bool( 120<=getColorAverage(img,y+coordinates["red_cross_y_delta_down"],x) <= 132)
    return(center and up and down)

def auto_follow(): ##榜单页下识别"+"并关注
    os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))  # 翻过榜前10，回关率太低
    time.sleep(2)
    os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))  # 翻过榜前10，回关率太低
    blankpages = 0
    oldpoints = []
    while (blankpages <= 1):
        # 以下是粉丝翻页加关注
        time.sleep(2)  # 等待1秒用于屏幕滑动缓冲
        os.system("adb -s {} shell screencap -p /sdcard/screen3.png".format(adb_device))
        os.system("adb pull /sdcard/screen3.png rank.png")
        img = cv2.imread("rank.png")
        points = []
        x = coordinates["rank_redcross_column_x"]
        y_range = coordinates["rank_redcross_column_y_range"]
        for y in range(y_range[0], y_range[1]):
            if getCross(img, y, x) == True:
                print("get cross successfully")
                points.append((x, y))

        print(points)
        if len(points) != 0 and points != oldpoints:
            for point in points:
                os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,point[0], point[1]))
                time.sleep(0.3)
            os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))  # 粉丝页翻页，考虑滑动惯性
            time.sleep(1)  # 等待1秒用于屏幕滑动缓冲 
            oldpoints = points
        else:
            print("No cross found")
            time.sleep(0.3)
            blankpages = blankpages + 1
            os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))  # 粉丝页翻页，考虑滑动惯性
            time.sleep(1)  # 等待2秒用于屏幕滑动缓冲

    os.system("adb -s {} shell input keyevent 4".format(adb_device))  # 手机回退键
    time.sleep(2)


## 计算flag的des
def cal_des(flag_list):
    des_flag_list = []
    for flag in flag_list:
        trainingImage = cv2.imread(flag,0)
        sift = cv2.xfeatures2d.SIFT_create()
        kp,des = sift.detectAndCompute(trainingImage,None)
        des_flag_list.append(des)
    return des_flag_list
##图像匹配
def flann_match(qimage,des_flag):
    queryImage = cv2.imread(qimage,0)
    ##create SIFT and detect/compute
    sift = cv2.xfeatures2d.SIFT_create()
    kp,des = sift.detectAndCompute(queryImage,None)
    ## FLANN matcher parameters
    FLANN_INDEX_KDTREE =0
    indexParams = dict(algorithm = FLANN_INDEX_KDTREE,trees = 5) #algorithm = FLANN_INDEX_LSH;algorithm = FLANN_INDEX_KDTREE
    searchParams = dict(checks = 1) #or pass empty dictionary/checks = 50

    flann = cv2.FlannBasedMatcher(indexParams,searchParams)

    matches = flann.knnMatch(des,des_flag,k = 2)
    ##print("匹配点数为：{}".format(len(matches)))
    matchesMask = [[0,0] for i in range(len(matches))]
    good = []
    for i,(m,n) in enumerate(matches):
        if m.distance < match_factor*n.distance: ##这里调整最佳匹配点精度，越小越精
            matchesMask[i] = [1,0]
            good.append(m)
    return len(good)

class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None



##---------------------主程序--------------------------------

des_flag_list =  cal_des(flag_list)

while(True):
    os.system("adb -s {} shell screencap -p /sdcard/screen.png".format(adb_device))
    os.system("adb -s {} pull /sdcard/screen.png screen.png".format(adb_device))
    qimage = "screen.png"
    img = cv2.imread(qimage)
    start_time = time.time()
    real_scores = []
    page_index = 12
    page_index_list = []

    threads = []
    for i in range(len(des_flag_list)): ##多线程处理页面匹配值计算过程
        t = MyThread(flann_match,args=(qimage,des_flag_list[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        real_scores.append(t.get_result())

    for i in range(len(des_flag_list)):
        if real_scores[i]>=flag_threshold_scores[i]:##优先选拔匹配值超过阀值的元素
            page_index_list.append(i)
    if len(page_index_list) == 1: ##只有一个超阀值匹配的情况下算成功，否则如果有多个匹配则认为匹配失败
        page_index = page_index_list[0]
        print("超阀值获胜")
    elif len(page_index_list) ==0:
        arr_flag_threshold_scores = np.array(flag_threshold_scores)
        arr_real_scores = np.array(real_scores)
        diff = abs(arr_real_scores - arr_flag_threshold_scores)
        percents = np.round(np.true_divide(diff, arr_flag_threshold_scores), decimals=3) #计算各数据的偏差百分比
        min_percent = np.argmin(percents)
        #if min_percent <= 0.7: ##避免阀值不满足，误差都很大的无关页面出现的情况，误差大于0.6就没必要在里面选了，定为未知页面
        page_index = min_percent
        print("最小误差获胜")
    else:
        page_index = 12
    end_time = time.time()
    time_interval = end_time - start_time
    print("匹配用时：{}".format(time_interval))

    if page_index == 0:
        print("直播页")
        if livevideo_flag % 2 ==0:
            crd = coordinates["livevideo_rank_entry"]
            os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,crd[0],crd[1])) #点击直播页粉丝榜按钮
        else:
            livevideo_flag = livevideo_flag + 1
            os.system("adb -s {} shell input touchscreen swipe 550 842 550 500".format(adb_device)) #切换直播间

    elif page_index ==1:
        print("视频播放页")
        if comment_flag % 2 == 0:
            crd = coordinates["videoplay_comment_field"]
            os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,crd[0],crd[1]))  # 点击视频页评论编辑窗口
        else:
            crd = coordinates["videoplay_favor_icon"]
            comment_flag = comment_flag + 1
            b, g, r = img[crd[1], crd[0]]  ##点赞心形坐标
            avecolor = int((int(b) + int(g) + int(r)) / 3)
            if avecolor > 220:##如果心形未被点红，则点击，点击完退出
                os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,crd[0],crd[1]))  # 点赞坐标
                time.sleep(2)
            os.system("adb -s {} shell input keyevent 4".format(adb_device))
            time.sleep(1)
            os.system("adb -s {} shell input keyevent 4".format(adb_device))


    elif page_index ==2:
        print("粉丝列表页")
        for i in range(random.randint(1,7)): #下翻随机页
            os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))
        for i in range(random.randint(1, 4)):#上翻随机页
            os.system("adb -s {} shell input touchscreen swipe 500 700 500 1100".format(adb_device))
        time.sleep(2)##划屏缓冲
        icon_points = get_fans_icon()#获取粉丝列表页的所有粉丝头像坐标
        point = random.choice(icon_points) #随机选取一个头像坐标
        print(point)
        os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,point[0], point[1])) #点击粉丝头像

    elif page_index == 3:
        print("粉丝个人页")
        for i in range(random.randint(0,2)): #下翻随机页
            os.system("adb -s {} shell input touchscreen swipe 500 1100 500 700".format(adb_device))
            time.sleep(2)
            os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,random.choice([coordinates["fans_profile_videolist_3x"][0],coordinates["fans_profile_videolist_3x"][1],coordinates["fans_profile_videolist_3x"][2]]),coordinates["fans_profile_videolist_y"]))
            #这里用1888这个y坐标考虑了视频翻页到最底部后会有一个"没有更多视频"的黑色空白处


    elif page_index ==4:
        print("评论页")
        cord = coordinates["comment_page_edit_field"]
        comment_flag = comment_flag + 1
        os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1])) #评论页：评论编辑框
        time.sleep(2)
        comment = random.choice(comment_list)
        os.system("adb -s {} shell input text {}".format(adb_device,comment))##随机写评论
        time.sleep(2)
        cord = coordinates["comment_page_submit"]
        os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1])) #评论页：评论提交框
        time.sleep(2)

    elif page_index == 5:
        print("榜单页")
        auto_follow() ##自动加关注
        livevideo_flag = livevideo_flag + 1

    elif page_index ==6:
        print("号主个人信息页")
        cord = coordinates["myprofile_enterfanslist"]
        os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1]))  # 点击"粉丝"，进入粉丝页
    elif page_index == 7:
        print("0作品页")
        os.system("adb -s {} shell input keyevent 4".format(adb_device)) #手机回退键
    elif page_index == 8:
        print("开场首页")
        option = random.randint(1,2)
        if option == 1:
            cord = coordinates["portal_livevideo"]
            os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1])) #点击左上角"直播"按钮，进入直播间
        if option ==2:
            cord = coordinates["portal_me"]
            os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1]))  # 点击右下角"我"选项，进入号主个人页

    elif page_index ==9:
        print("直播结束页")
        os.system("adb -s {} shell input touchscreen swipe 550 1000 550 500".format(adb_device))
    elif page_index ==10:
        print("个人消息页")
        cord = coordinates["portal_portal"]
        os.system("adb -s {} shell input mouse tap {} {}".format(adb_device,cord[0],cord[1]))  # 点回主页
    elif page_index == 11:
        print("视频拍摄页")
        os.system("adb -s {} shell input keyevent 4".format(adb_device)) #手机回退键
    else:
        print("未知页面")
        unknown_page_list.append(1)
        if len(unknown_page_list) >=3:
            pass  ##此处添加退出app的脚本
            time.sleep(5)
            pass ##此处添加打开app的脚本
            unknown_page_list = []
        else:
            time.sleep(1)
            os.system("adb -s {} shell input keyevent 4".format(adb_device))  # 手机回退键
            time.sleep(4)
            os.system("adb -s {} shell input keyevent 4".format(adb_device))  # 手机回退键

    time.sleep(3) ##等待三秒进行下一张截图，避免由于截图过快程序连续截到相同页面

##----------------主程序结束--------------------------------------

# ##------------以下代码用于匹配情况显示和调试-----------------------
#     print("------start------------ \n")
#     print("Time cost:{}秒 \n".format(time_interval))
#     arr_flag_threshold_scores = np.array(flag_threshold_scores)
#     arr_real_scores = np.array(real_scores)
#     diff = abs(arr_real_scores - arr_flag_threshold_scores)
#     percents = np.round(np.true_divide(diff, arr_flag_threshold_scores), decimals=2)
#     print(flag_lables)
#     print("\n")
#     print("参考值：{}".format(flag_threshold_scores))
#     print("\n")
#     print("实际值：{}".format(real_scores))
#     print("\n")
#     print("误差：{}".format(percents))
#     print("-------------end-------------")
#
# ##-----------------------------------------------------
