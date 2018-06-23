import time
import json
import base64
import requests
from urllib.parse import urlencode

class GetDynamicAPI(object):
    def __init__(self, date=time.strftime("%Y-%m-%d"), page=1):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.qimai.cn/rank/release",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/59.0"
        }

        self.params = {
            # "country": "cn",
            "date": date,
            "genre": "36",
            "page": page
        }

        
    # 自定义加密函数
    def encrypt(self, a, n="9d1abd758c043319aee5ee1c0e3f26c6"):
        s = list(a)
        n = list(n)
        sl = len(s)
        nl = len(n)
        for i in range(0, sl):
            s[i] = chr(ord(s[i]) ^ ord(n[i % nl]))
        return "".join(s)

    def main(self):
        # 提取查询参数值并排序
        s = "".join(sorted([str(v) for v in self.params.values()]))
        # Base64 Encode
        s = base64.b64encode(bytes(s, encoding="ascii"))
        # 时间差
        t = str(int((time.time() * 1000 - 1515125653845)))
        # 拼接自定义字符串  MTIwMTgtMDYtMjMzNg==@#/rank/release@#14609635794@#1
        s = "@#".join([s.decode(), "/rank/release", t, "1"])
        # 自定义加密 & Base64 Encode
        s = base64.b64encode(bytes(self.encrypt(s), encoding="ascii"))
        # 拼接 URL
        self.params["analysis"] = s.decode()
        url = "https://api.qimai.cn/rank/release?{}".format(urlencode(self.params))
        # 发起请求
        return url


if __name__ == '__main__':
    c1 = GetDynamicAPI("2018-03-12", 1)
    print(c1.main())
