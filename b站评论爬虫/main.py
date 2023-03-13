import os
import random

import requests
import json
from lxpy import copy_headers_dict
import time
import pandas as pd
import traceback

headers = copy_headers_dict(
    '''
accept: */*
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: no-cache
cookie: buvid3=AA095F01-1CE7-53E9-B2EE-B07AFC3B460403570infoc; _uuid=5C858E89-5AB5-2655-D8BA-5D9862533DC103335infoc; buvid_fp=AA095F01-1CE7-53E9-B2EE-B07AFC3B460403570infoc; CURRENT_FNVAL=2000; blackside_state=1; rpdid=|(kmRl~uul0J'uYJm|m)kuk; PVID=1; fingerprint=8c9cdb699b14561fec2ddaa3f1d5077a; sid=55vtu9qc; buvid_fp_plain=AA095F01-1CE7-53E9-B2EE-B07AFC3B460403570infoc; DedeUserID=411453145; DedeUserID__ckMd5=1885d1433d4fe273; SESSDATA=984c49e3%2C1655872426%2C2a76c*c1; bili_jct=36781b8183fe6197be4af58a967872c0; b_ut=5; i-wanna-go-back=2; bp_t_offset_411453145=608030385432451379; LIVE_BUVID=AUTO4116404111024989; b_lsid=A611066D10_17DF5B6F859; bsource=search_baidu; innersign=1
pragma: no-cache
referer: https://www.bilibili.com/video/BV1dt4y1C7tV
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: script
sec-fetch-mode: no-cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62
'''
)
url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery172004993633833089839_1640505035653&jsonp=jsonp&next={}&type=1&oid={}&mode=3&plat=1&_=1640505036464"


# 时间戳转时间(秒)
def convert_time_(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)
    return otherStyleTime


def InstallCsv(FileName, ContentName, Content, SaveType):
    try:
        if not os.path.exists(FileName):
            os.makedirs(FileName)
        df = pd.DataFrame(
            Content, index=[1])
        if os.path.exists(FileName + "/" + ContentName):
            df.to_csv(FileName + "/" + ContentName, mode=SaveType, header=False, index=False, encoding="utf-8_sig")
        else:
            df.to_csv(FileName + "/" + ContentName, mode=SaveType, index=False, encoding="utf-8_sig")
    except Exception as e:
        with open(f"{FileName}/error.txt", "a") as f:
            f.write("\n文件名：" + str(FileName) + ",\n内容名:" + str(ContentName) + "\n内容：" + str(Content) + str(
                e) + "\n=====================")


def get_main_comment(video_id,link_url,all_count,item):
    # next 默认是0
    next_tem = "0"
    ji = str(item + 1)
    fname = '第'+ ji + '集data.csv'
    while True:
        time.sleep(random.uniform(0.1,0.3))
        url_tem = url.format(next_tem, video_id)
        res = requests.get(url=url_tem, headers=headers).text
        start_index = res.index("(")
        res_json_raw = res[start_index + 1:-1]
        json_data = json.loads(res_json_raw)
        next_tem = json_data["data"]["cursor"]["next"]
        replies = json_data["data"]["replies"]
        count = json_data['data']['cursor']['all_count']
        try:
            if len(replies) == 0:
                break
            for reply in replies:
                member = reply['member']
                uname = member['uname']
                avatar = member['avatar']
                current_level = member['level_info']['current_level']
                comment = reply["content"]["message"]
                time_ = convert_time_(reply['ctime'])
                like = reply['like']
                rcount = reply['rcount']
                dic = {
                    "原始链接":link_url,
                    '评论用户': uname,
                    '头像': avatar,
                    '等级': current_level,
                    '评论时间': time_,
                    '评论内容': comment,
                    '评论点赞数': like,
                    '评论回复数': rcount,
                    "评论类型": "主评论"
                }
                all_count = all_count + 1
                print('总评论数：{}，当前评论数：{}，写入：{}。'.format(count, all_count, fname))
               # print(str(dic).encode("gbk", "ignore").decode("gbk"))
                
                InstallCsv("File", fname, dic, "a+")
                rpid_str = reply['rpid_str']
                get_son_comment(video_id, rpid_str,link_url,all_count,count,fname)
        except Exception as e:
            traceback.print_exc()
            break


url_son_comment = "https://api.bilibili.com/x/v2/reply/reply?callback=jQuery172004993633833089839_1640505035657&jsonp=jsonp&pn={}&type=1&oid={}&ps=10&root={}&_=1640506133143"


def get_son_comment(video_id, comment_id,link_url,all_count,count,fname):
    page = 1
    while True:
        time.sleep(random.uniform(0.1,0.3))
        url_son_comment_tem = url_son_comment.format(page, video_id, comment_id)
        res = requests.get(url=url_son_comment_tem, headers=headers).text
        start_index = res.index("(")
        res_json_raw = res[start_index + 1:-1]
        json_data = json.loads(res_json_raw)
        try:
            replies = json_data["data"]["replies"]
            if len(replies) == 0:
                break
            for reply in replies:
                member = reply['member']
                uname = member['uname']
                avatar = member['avatar']
                current_level = member['level_info']['current_level']
                comment = reply["content"]["message"]
                time_ = convert_time_(reply['ctime'])
                like = reply['like']
                rcount = reply['rcount']
                dic = {
                    "原始链接": link_url,
                    '评论用户': uname,
                    '头像': avatar,
                    '等级': current_level,
                    '评论时间': time_,
                    '评论内容': comment,
                    '评论点赞数': like,
                    '评论回复数': rcount,
                    "评论类型": "子评论"
                }
                all_count = all_count + 1
                print('总评论数：{}，当前评论数：{}，写入：{}。'.format(count, all_count, fname))
                #print(str(dic).encode("gbk", "ignore").decode("gbk"))
                InstallCsv("File", fname, dic, "a+")
        except Exception as e:
            traceback.print_exc()
            break
        page = page + 1


def main():
    arr = [
        [
            "https://www.bilibili.com/bangumi/play/ep261461",
            "https://www.bilibili.com/bangumi/play/ep261466",
            "https://www.bilibili.com/bangumi/play/ep261468",
            "https://www.bilibili.com/bangumi/play/ep261820",
            "https://www.bilibili.com/bangumi/play/ep262055",
            "https://www.bilibili.com/bangumi/play/ep262056",
            "https://www.bilibili.com/bangumi/play/ep262057",
        ],
        [
            "41880123",
            "41879836",
            "41879729",
            "42230484",
            "42230515",
            "42231317",
            "42231338",
        ]
    ]
    for item in range(0,39):
        link_url = arr[0][item]
        video_id = arr[1][item]
        all_count=0
        get_main_comment(video_id,link_url,all_count,item)


if __name__ == '__main__':
    main()
