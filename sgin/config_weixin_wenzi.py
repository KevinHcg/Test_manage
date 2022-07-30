# -*- coding:utf-8 -*-
import requests,os

class SendWeiXinWenZi:
    #传入文件
    def post_file(self,text1):
        headers = {"Content-Type": "text/plain"}

        send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9a9f5560-1f55-49dc-b692-ba95a4b7ceeb"
        send_data = {
            "msgtype": "markdown",  # 消息类型,markdown,text
            "markdown": {
                "content": text1,  # 文本内容，最长不超过2048个字节，必须是utf8编码
                # "mentioned_list": ["@all"],
                # userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
                "mentioned_mobile_list": ["17302665996","19195632726"]  # 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print(res.text)
if __name__ == '__main__':
    text1="测试开始"
    SendWeiXinWenZi().post_file(text1)