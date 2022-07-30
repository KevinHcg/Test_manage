import time
import random
import json


def gps_list():
    gps_body = {"address": '中国广西壮族自治区南宁市青秀区南湖街道合作路',
                "baidu_Time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                "coorType": 'bd09ll',
                "deviceId": '862545031564033',
                "has_speed": 'false',
                "id": '2641',
                "isUpload": 'false',
                "latitude": 22.814624,
                "locType": 161,
                "local_time": int(time.time()),
                "longitude": 108.403864,
                "policeNo": '',
                "radius": 10.0,
                "speed": random.uniform(1, 10),
                "userId": 1111,
                }


    b = json.dumps(json.dumps(gps_body, ensure_ascii=False),
               ensure_ascii=False
               )  # python默认的库，放在第一行 from __future__ import unicode_literals

    return b