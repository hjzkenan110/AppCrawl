import base64
import http.cookiejar as cookielib
import json
import random
import string
import time
from urllib.parse import urlencode, urljoin

import requests
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar

AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
HEADER = {
    "HOST" : "api.qimai.cn",
    "Referer" : "https://www.qimai.cn/rank/release",
    'User-Agent' : AGENT,
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

class GetDynamicAPI(object):
    def __init__(self, middle_url=None, **kargs):
        if middle_url == 1:
            self.middle_url = "/rank/release"
        elif middle_url == 2:
            self.middle_url = "/app/appinfo"
        elif middle_url == 3:
            self.middle_url = "/account/signinForm"

        self.params = kargs
    
    # 自定义加密函数
    def encrypt(self, a, n="a12c0fa6ab9119bc90e4ac7700796a53"):
        s, n = list(a), list(n)
        sl, nl = len(s), len(n)
        for i in range(0, sl):
            s[i] = chr(ord(s[i]) ^ ord(n[i % nl]))
        return "".join(s)

    def get_url(self):
        base_url = "https://api.qimai.cn"
        # 提取查询参数值并排序
        s = "".join(sorted([str(v) for v in self.params.values()]))
        # Base64 Encode
        s = base64.b64encode(bytes(s, encoding="ascii"))
        # 时间差
        t = str(int((time.time() * 1000 - 1515125653845)))
        # 拼接自定义字符串  MTIwMTgtMDYtMjMzNg==@#/rank/release@#14609635794@#1
        s = "@#".join([s.decode(), self.middle_url, t, "1"])
        # 自定义加密 & Base64 Encode
        s = base64.b64encode(bytes(self.encrypt(s), encoding="ascii"))
        self.params["analysis"] = s.decode()
        url = urljoin(base_url, self.middle_url) + "?{}".format(urlencode(self.params))
        return url

def qimai_login(account, password):
    # 获取登陆的api接口
    signin_api = GetDynamicAPI(middle_url=3).get_url()
    post_data = {
                "username": account,
                "password": password,
            }

    session = requests.session()

    # session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
    # try:
    #     session.cookies.load(ignore_discard=True)
    # except:
    #     print ("cookie未能加载")
    
    sessionID = ''.join(random.sample(string.ascii_letters + string.digits, 26))
    session.cookies['PHPSESSID'] = sessionID
    # print(sessionID)
    session.post(signin_api, data=post_data, verify=False, allow_redirects=False)
    
    cookies = dict_from_cookiejar(session.cookies)
    with open("cook.txt", "w") as fp:
        json.dump(cookies, fp)

    
def judge_login():
    #通过返回json内容来判断是否为登录状态'
    session = requests.session()
    jar = RequestsCookieJar()
    with open("cook.txt", "r") as fp:
        cookies = json.load(fp)
        for key, value in cookies.items():
            jar.set(key, value)

    test_url = GetDynamicAPI(middle_url=1, genre=36, page=10, date="2018-06-27").get_url()
    response = session.get(test_url, headers=HEADER, cookies=jar, verify=False)
    # print(response.text)
    res = json.loads(response.text)
    if res["code"] == 10011:
        return False
    elif res["code"] == 10000:
        return True
    else:
        print("Others condition!")

    
if __name__ == '__main__':
    # c1 = GetDynamicAPI(middle_url = 1, appid = "1391039541", country = "cn")
    #c2 = GetDynamicAPI(middle_url=1, genre=36, page=1, date="2018-07-01")
    # c3 = GetDynamicAPI(middle_url=3)
    #print(c2.get_url())
    # qimai_login("15816659260", "qwe123")
    a = judge_login()
    if a == False:
        print(a)
    if a == True:
<<<<<<< HEAD
        print("AMD YES!")
=======
        print("AMD YES!")
>>>>>>> 3799fbc4abf287e45352812957705dc057da7e26
