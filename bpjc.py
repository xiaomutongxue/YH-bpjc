#yaohuo 44747 小沐同学 仅限妖火内分享 此脚本仅用于学习 下载后请立即删除 后果与作者无关

import base64,requests,json,time,os,datetime

#登录方式有两种
#1.在python内填写
#只能填写一种登录方式信息，不然可能出错，即填写“JC_Authorization与JC_token ” 或 账号密码登录mail与password
#2.在青龙运行
#只能填写一种登录方式信息，不然可能出错
#即填写“JC_Authorization与JC_token ” 或 账号密码登录JC_Account（格式为 “账号|密码”）如 JC_Account=clover@qq.com|woailaoC

#你的微信PUSH_PLUS_TOKEN,
PUSH_PLUS_TOKEN = ''
#JC_Authorization登录
JC_Authorization = ""
JC_token = ""
#账号密码登录
mail=""
password = ""


def main(account_Authorization,info,token):
    new_info={
        'user':'',
        'time_dingyue2':'',
        'time_dingyue':'',
        'liuliang':''
    }
    dy_time =info["time_dingyue2"]
    dy_liuliang=info["liuliang"]
    time = datetime.datetime.now().timestamp()
    statue = "false"
    if (dy_time-time<=86400):
        statue  = reNew(account_Authorization)
        new_info = get_info(account_Authorization,token)
        dy_liuliang =new_info["liuliang"]

    if(dy_liuliang<10):
        statue  =  reNew(account_Authorization)
        new_info = get_info(account_Authorization,token)
    if(statue== True):
        notify(new_info )
    else:
        notify(info)


def notify(new_info):
    message = "******白嫖机场小助手*******\n"
    message += "当前用户："+new_info["user"]
    message += "\n当前剩余流量："+str(new_info["liuliang"])+"G"
    message += "\n当前订阅到期时间："+new_info["time_dingyue"]
    message += "\n**************************"
    message +="\n1.脚本会在订阅到期前10天重新订阅"
    message +="\n2.脚本会在流量剩余10g以下重新订阅"

    if "PUSH_PLUS_TOKEN" in os.environ:
        PUSH_PLUS_TOKEN1 = os.environ["PUSH_PLUS_TOKEN"]
    else:
        PUSH_PLUS_TOKEN1 = PUSH_PLUS_TOKEN
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_TOKEN1,
        "title": "白嫖机场小助手",
        "content": message,
        "topic": '',
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    if PUSH_PLUS_TOKEN1 == "":
       print("未填写PUSH_PLUS_TOKEN，不推送！")
    else:
        response = requests.post(url=url, data=body, headers=headers).json()
        print(response)
        if response["code"] == 200:
            print("PUSHPLUS 推送成功！")
        else:

            url_old = "http://pushplus.hxtrip.com/send"
            response = requests.post(url=url_old, data=body, headers=headers).json()

            if response["code"] == 200:
                print("PUSHPLUS(hxtrip) 推送成功！")

            else:
                print("PUSHPLUS 推送失败！")

def reNew(account_Authorization):
    data = {
        'period':'month_price',
        'plan_id':'1',
        'coupon_code':'bp88'
    }
    headers = {
        'authorization': account_Authorization,
        'Host': 'xn--mesv7f5toqlp.com',
        'Origin': 'https://xn--mesv7f5toqlp.com/',
        'Referer': 'https://xn--mesv7f5toqlp.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    url_save = "https://xn--mesv7f5toqlp.com/api/v1/user/order/save"
    save_re = requests.post(url_save, headers=headers, json=data)
    get_data = save_re.json()["data"]

    data2 = {
        'trade_no':get_data,
        'method':2
    }
    url_checkout = 'https://xn--mesv7f5toqlp.com/api/v1/user/order/checkout'
    save_re = requests.post(url_checkout, headers=headers, json=data2)
    save_data = save_re.json()["data"]
    print(save_re.json())
    print(save_data)
    print("***************************")
    print("您的流量不足10G\n正在尝试重新订阅")
    if( save_data== True):
        print("重新订阅100G成功！")
        print("***************************")
    else:
        print("重新订阅失败！")
    return save_data
def getAccount():
    if "JC_Authorization" in os.environ:
        return os.environ["JC_Authorization"],os.environ["JC_TOKEN"]
    if JC_Authorization!="" and JC_token !="":
        return JC_Authorization,JC_token
    if "JC_Account" in os.environ:
        a_mail = os.environ["JC_Account"].split("|")[0]
        a_password = os.environ["JC_Account"].split("|")[1]
        login_url = "https://xn--mesv7f5toqlp.com/api/v1/passport/auth/login"
        data = {
            'email': a_mail,
            'password': a_password
        }
        headers = {
            'Host': 'xn--mesv7f5toqlp.com',
            'Origin': 'https://xn--mesv7f5toqlp.com/',
            'Referer': 'https://xn--mesv7f5toqlp.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        login_re = requests.post(login_url, headers=headers, json=data)
        authorization = login_re.json()["data"]["auth_data"]
        token = login_re.json()["data"]["token"]
        print("***************************")
        print("当前登录方式：账号密码|" + a_mail)
        print("***************************")
        return authorization,token
    if mail!="" and password !="":
        a_mail = mail
        a_password = password
        login_url = "https://xn--mesv7f5toqlp.com/api/v1/passport/auth/login"
        data = {
            'email':a_mail,
            'password':a_password
        }
        headers ={
            'Host': 'xn--mesv7f5toqlp.com',
            'Origin': 'https://xn--mesv7f5toqlp.com/',
            'Referer': 'https://xn--mesv7f5toqlp.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        login_re = requests.post(login_url,headers = headers,json  = data)
        authorization = login_re.json()["data"]["auth_data"]
        token = login_re.json()["data"]["token"]
        print("***************************")
        print("当前登录方式：账号密码|"+a_mail)
        print("***************************")
        return authorization,token

def get_info(account_Authorization,token):

    url_info = 'https://xn--mesv7f5toqlp.com/api/v1/user/info'
    headers = {
        'authorization':account_Authorization,
        'Referer': 'https://xn--mesv7f5toqlp.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    info_re = requests.get(url_info, headers=headers)
    url_dingyue = 'https://xn--mesv7f5toqlp.com/api/v1/client/subscribe?token='+token
    email = info_re.json()["data"]["email"]
    time_stamp = info_re.json()["data"]["expired_at"]
    time_dingyue =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
    a = requests.get(url_dingyue).text

    decoded_data = str(base64.b64decode(a))
    decoded_data2 = decoded_data.split("trojan://")[1].replace("\\r\\n", "")
    decoded_data3 = str(decoded_data2.split("#")[-1]).encode().decode("utf-8")
    liuliang = str(requests.utils.unquote(decoded_data3).split("：")[1]).replace(" GB","")
    list={
        'user':email,
        'time_dingyue2':time_stamp,
        'time_dingyue':time_dingyue,
        'liuliang':float(liuliang)
    }
    print("***************************")
    print("当前剩余流量："+str(list["liuliang"]))
    print("当前订阅到期时间："+list["time_dingyue"])
    print("***************************")
    return list
if __name__ == '__main__':
    account_Authorization,token = getAccount()
    info = get_info(account_Authorization,token)
    main(account_Authorization,info,token)
