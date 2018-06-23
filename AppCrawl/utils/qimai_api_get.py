import time
import json
import base64
import requests
from urllib.parse import urlencode,urljoin


class GetDynamicAPI(object):
    def __init__(self, middle_url = None, **kargs):
        self.params = kargs
        self.middle_url = middle_url
    
    # 自定义加密函数
    def encrypt(self, a, n="9d1abd758c043319aee5ee1c0e3f26c6"):
        s = list(a)
        n = list(n)
        sl = len(s)
        nl = len(n)
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
        #                   MTI5ODM4NTIwNWNu@#/app/appinfo@#14966911244@#1
        s = "@#".join([s.decode(), self.middle_url, t, "1"])
        # 自定义加密 & Base64 Encode
        s = base64.b64encode(bytes(self.encrypt(s), encoding="ascii"))
        # 拼接 URL
        self.params["analysis"] = s.decode()
        url = urljoin(base_url, self.middle_url) + "?{}".format(urlencode(self.params))
        # app/appinfo
        # 发起请求
        return url


if __name__ == '__main__':
    # c1 = GetDynamicAPI(middle_url = "/app/appinfo", appid = "1391039541", country = "cn")
    c2 = GetDynamicAPI(middle_url = "/rank/release", genre = "36", page = 1)
    print(c2.get_url())
