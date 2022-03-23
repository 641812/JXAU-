import json
import requests
import random
from datetime import datetime, timedelta
import time

#服务器信息
host = "https://xsgzgl.zxhnzq.com/"
#user = "api/ArticleInfo/GetTopList?istype=1&categoryid=0&num=6&scode=10410&sccode=1041001"
user = "api/PositionInfo/AddOrEditPosition"
api = "api/BatchSignin/Add"
ver = "2.0.56"

#学号
xh = ""
#学生登入身份认证口令
token = ""

# pushplus推送
pushtoken = ''  # 在pushplus网站中可以找到

def header():
    ID = str(12000000+random.randint(100000,999999))
    param = {
        "Host":"xsgzgl.zxhnzq.com",
        "Connection":"keep-alive",
        "Content-Length":"339",
        "Authorization": token,
        "version": ver,
        "content-type": "application/json",
        "env": "production",
        "terminal": "miniprogram",
        "positionID": ID,
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123a) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wx517b2d70f4cd9e2f/21/page-frame.html",
    }
    return param

#登入数据
def carddate():
    #time_stamp = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(time_stamp)
    #世界坐标随机
    tmp = random.uniform(28.75980, 28.75985) #随机种子
    lat = round(tmp, 6)
    tmp = random.uniform(115.83760, 115.83765)
    lng = round(tmp, 6)
    date={
    "usercode":xh,
    "xq":"20212","typeid":1,
    "remark":"首页启动",
    "biztime":time_stamp,
    "lat":lat,
    "lng":lng,
    "address":"江西省南昌市青山湖区志敏大道(江西农业大学)",
    "province":"江西省",
    "city":"南昌市",
    "district":"青山湖区",
    "street":"志敏大道",
    "scode":"10410",
    "sccode":"1041001"
    }
    return date

#登入
def enter():
    url=host+user
    #print(url)
    #r=requests.get(url,headers=header())
    #传送json数据获取上报id
    r = requests.post(url,json=carddate(),headers=header())
    print(carddate())
    r = json.loads(r.content)
    print(r)
    print("报文id:"+str(r["data"]))
    postid = r["data"]
    return postid

def clock_in(id):
    #打卡数据
    now_time = datetime.now()
    utc_time = now_time - timedelta(hours=8)  # UTC比北京时间提前了8个小时
    utc_time = utc_time.strftime("%Y-%m-%dT%H:%M:%S")
    regtime = utc_time + "." + str(random.randint(110, 299)) + "Z" # 构建时间格式
    #随机温度
    ret = random.uniform(36.3, 36.8)
    temperature = str(round(ret, 1))
    value={
        "batchid": 2002,
        "positionid": id,
        "verifystate": 0,
        "health_Student": {"xh": xh,
                           "registerdate": regtime,
                           "bodytemperature": temperature,
                           "bodystatus": "正常",
                           "bodyabnormalinfo": "无异常",
                           "xsremark": "",
                           "status": 0,
                           "quarantinestate": "无隔离",
                           "quarantineplace": "无",
                           "isverify": 0,
                           "verifytext": "",
                           "iscontractxinguan": "否",
                           "period": 0},
        "scode": "10410", "sccode": "1041001"}

    return value

def tempheader(id):
        param = {
            "Host": "xsgzgl.zxhnzq.com",
            "Connection": "keep-alive",
            "Content-Length": "390",
            "Authorization": token,
            "version": ver,
            "content-type": "application/json",
            "env": "production",
            "terminal": "miniprogram",
            "positionID": str(id),
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123a) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx517b2d70f4cd9e2f/21/page-frame.html",
        }
        return param

def push(content):
    title = '打卡信息'  # 改成你要的标题内容
    url = 'http://www.pushplus.plus/send?token=' + pushtoken + '&title=' + title + '&content=' + content
    requests.get(url)

def post(id):
    url = host+api
    # print(url)
    # r=requests.get(url,headers=header())
    # 传送json数据获取上报id
    value = clock_in(id)
    print("打卡数据" + str(value))
    r = requests.post(url, json=value, headers=tempheader(id))
    r = json.loads(r.content)
    print(r)
    if r["code"] == 200 :
        print("打卡成功")
        push("打卡成功")
    else:
        print("打卡错误:"+str(r["msg"]))
        push("打卡错误:"+str(r["msg"]))

def main():
    # 随机延时运行（分钟）
    checkin = random.uniform(5, 200)
    print("延时运行：" + str(round(checkin, 1)))
    time.sleep(checkin)
    #获得报文编号
    postid = enter()
    #发送报文
    post(postid)


if __name__ == "__main__":
    main()
