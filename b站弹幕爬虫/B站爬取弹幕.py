# -*- coding:utf-8 -*-
import requests
import re
from Bztm_pb2 import DmSegMobileReply
import json
from google.protobuf.json_format import MessageToJson
import csv
import os
import datetime
from tqdm import tqdm
import time
import pandas as pd
import random

'获取弹幕api：https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=252900431&date=2021-05-20'
orgin_url='https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={}&date={}'


#获取cid
def get_cid(bvid):
    video_url = 'https://www.bilibili.com/bangumi/play/' + bvid
    page = requests.get(video_url, headers=header).text
    #cid = re.search(r'"cid":+([0-9])+,"cover"', page).group()[6:-8]
    cid = 93000416
    return cid
#获取txt中的bvid和cid
def readTxt():
    with open("那兔第一季bvid和cid.txt","r",encoding='utf-8') as f:
        data=f.read()
        bvid = re.search(r'第一集bvid:(\w+)', data).group()[8:]
        cid = re.search(r'第一集cid:(\w+)', data).group()[7:]
        print(bvid)
        print(cid)
    return bvid,cid

#生成日期序列
def create_assist_date(datestart = None,dateend = None):
	# 创建日期辅助表

	if datestart is None:
		datestart = '2016-01-01'
	if dateend is None:
		dateend = datetime.datetime.now().strftime('%Y-%m-%d')

	# 转为日期格式
	datestart=datetime.datetime.strptime(datestart,'%Y-%m-%d')
	dateend=datetime.datetime.strptime(dateend,'%Y-%m-%d')
	date_list = []
	date_list.append(datestart.strftime('%Y-%m-%d'))
	while datestart<dateend:
		# 日期叠加一天
		datestart+=datetime.timedelta(days=+1)
		# 日期转字符串存入列表
		date_list.append(datestart.strftime('%Y-%m-%d'))
	return date_list


#获取日期输入
def get_dates():
	des=input('输入爬取弹幕的“开始日期 结束日期”：')
	dates=des.split()
	date_list=create_assist_date(dates[0],dates[-1])
	return date_list

#时间戳转换成日期
def get_time(ctime):
    timeArray = time.localtime(int(ctime))
    otherStyleTime = time.strftime("%Y.%m.%d", timeArray)
    return str(otherStyleTime)

#时间戳转换成时间
def get_time2(t):
    t1 = float(t)/1000
    t2 = time.localtime(t1)
    t3 = time.strftime("%M:%S", t2)
    return t3

if __name__=='__main__':
    ##第一个运行软件创建设置文件
    f_path = os.getcwd()
    fnames = os.listdir(f_path)

    if 'cookie.init' not in fnames:
        cookie= input('请输入cookie：')
        with open(r'cookie.init', 'w+', encoding='utf8') as f:
            f.writelines(cookie)
            f.close()
    else:
        with open(r'cookie.init', 'r', encoding='utf8') as f:
            cookie = f.readline()
            f.close()
    
    cookie_pool=[
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; blackside_state=0; CURRENT_BLACKGAP=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; b_ut=7; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; innersign=0; b_lsid=B5CFB7ED_180604D7444; fingerprint=8852141fcfdc9c3d7979cda89ca20532; buvid_fp=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; SESSDATA=c5301d86,1666435148,f1859*41; bili_jct=270537029d80e0d699948dacc5317aaf; DedeUserID=1852246931; DedeUserID__ckMd5=2101072df9dc0712; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; CURRENT_FNVAL=80",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_BLACKGAP=1; CURRENT_FNVAL=4048; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; b_nut=1650800882; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; innersign=1; b_lsid=9F131166_1806013E0BB; PVID=2; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; SESSDATA=7f4431a8,1666435240,b19f3*41; bili_jct=5908726aa791929f4dc13699ab5a9e5d; DedeUserID=1852246931; DedeUserID__ckMd5=2101072df9dc0712; sid=993v2414",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1010453476; DedeUserID__ckMd5=9db702b93ab2d2c4; SESSDATA=ed293f6e,1666435316,42c1e*41; bili_jct=6cdfc50e4be8d4e30656f09a95808d63; b_ut=5; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1; CURRENT_FNVAL=4048",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; sid=993v2414; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; DedeUserID=1010453476; DedeUserID__ckMd5=9db702b93ab2d2c4; SESSDATA=bef60e9c,1666435391,04072*41; bili_jct=33adef00598cfb56a2fda3218e7ed9da; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; innersign=1; CURRENT_FNVAL=4048",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=299704892; DedeUserID__ckMd5=ab6b75601b41e3be; SESSDATA=cfe07a09,1666435544,1d21e*41; bili_jct=952750c01c7f121cea54aed4cbc11a5c; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1; CURRENT_FNVAL=4048",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; innersign=1; CURRENT_FNVAL=4048; fingerprint=c0d1c0bfc8b45b0e0b5cc737e04bd16e; SESSDATA=1abb882b,1666435565,e18e2*41; bili_jct=452f9c6c1ce10c32365fbe0a0d68283a; DedeUserID=299704892; DedeUserID__ckMd5=ab6b75601b41e3be; sid=bi87zdrd; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; bp_video_offset_299704892=651951768974917800",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; CURRENT_FNVAL=4048; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1458177816; DedeUserID__ckMd5=9569170046877c4f; SESSDATA=2dd42711,1666435949,4a876*41; bili_jct=c3f197f1a112e0873c58d92f81f49846; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; innersign=1; CURRENT_FNVAL=4048; fingerprint=c0d1c0bfc8b45b0e0b5cc737e04bd16e; bp_video_offset_299704892=651951768974917800; SESSDATA=1748acc3,1666435735,218f7*41; bili_jct=6bf73e7e4b501dbd11abef614cec411f; DedeUserID=1458177816; DedeUserID__ckMd5=9569170046877c4f; sid=jh1wteqz; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; CURRENT_FNVAL=4048; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1056224014; DedeUserID__ckMd5=1b5d57b8801e07e9; SESSDATA=437a1921,1666436147,c0f1e*41; bili_jct=ab27e59961904d058c7a2f3c56527004; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; sid=jh1wteqz; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; DedeUserID=1056224014; DedeUserID__ckMd5=1b5d57b8801e07e9; SESSDATA=96fea063,1666435941,9fbfb*41; bili_jct=2d888375394685ce9819287750e13980; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; bp_video_offset_1056224014=undefined; innersign=1; CURRENT_FNVAL=4048",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1664329369; DedeUserID__ckMd5=b8a52a06599d1826; SESSDATA=7edb9a6a,1666436251,66e81*41; bili_jct=9f65cd4f6dd3cceeecc96a6d5864e42e; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1; CURRENT_FNVAL=4048",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; sid=jh1wteqz; bp_video_offset_1056224014=undefined; CURRENT_FNVAL=4048; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; DedeUserID=1664329369; DedeUserID__ckMd5=b8a52a06599d1826; SESSDATA=29bf00fb,1666436329,eb3b5*41; bili_jct=1a95219c4a7f03f3e574524760779ed0; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; innersign=1",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1993665907; DedeUserID__ckMd5=e0dc39d3770b6637; SESSDATA=df9ea22b,1666436398,a1cdb*41; bili_jct=6e703ef1d565e6a7715b95415a2af499; b_ut=5; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1; CURRENT_FNVAL=4048",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; sid=jh1wteqz; bp_video_offset_1056224014=undefined; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; DedeUserID=1993665907; DedeUserID__ckMd5=e0dc39d3770b6637; SESSDATA=ea49489f,1666436495,24cd8*41; bili_jct=948cc426736130f401d2e9bb1a396e1b; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; innersign=1; CURRENT_FNVAL=4048",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1328893953; DedeUserID__ckMd5=7d36a70e41f88fc0; SESSDATA=f6d0f275,1666436656,da120*41; bili_jct=8564ba1e8b7259250fb4a1e93bfe04fd; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1; CURRENT_FNVAL=4048",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; b_lsid=9F131166_1806013E0BB; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; sid=jh1wteqz; bp_video_offset_1056224014=undefined; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; DedeUserID=1328893953; DedeUserID__ckMd5=7d36a70e41f88fc0; SESSDATA=f95a6199,1666436711,f38bd*41; bili_jct=a921be4aeaf7dcaf1fe16f3e4cee303d; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; innersign=1; CURRENT_FNVAL=4048",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; sid=jsv0jbpt; bp_video_offset_1852246931=652718863031468000; b_ut=5; CURRENT_FNVAL=4048; fingerprint=436f15a21d38b5f1e56bccb012cb09a1; DedeUserID=1033951691; DedeUserID__ckMd5=417c379a352c1147; SESSDATA=33f8fc1e,1666436802,7e8a6*41; bili_jct=0fe2ae615e58c0c9a92dc832d8388417; buvid_fp=8852141fcfdc9c3d7979cda89ca20532; innersign=1",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; b_nut=1650800882; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; sid=jh1wteqz; bp_video_offset_1056224014=undefined; b_lsid=D8FD61B2_180606730DE; fingerprint=6162a2fa0425921f2ffb0dd03b275abf; DedeUserID=1033951691; DedeUserID__ckMd5=417c379a352c1147; SESSDATA=f33e4745,1666436889,f6b3e*41; bili_jct=fbb744063d9270d125d7ba54085a379d; bp_video_offset_1033951691=undefined; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e; innersign=1; CURRENT_FNVAL=4048",
    "buvid3=9CE072EE-E89F-37A9-977E-8571AFFA3DA618022infoc; CURRENT_BLACKGAP=0; blackside_state=0; rpdid=|(J~J|)kll~m0J'uYR)mYYJk|; _uuid=5BACC1101-C362-2BE2-A2BC-910A4B8B5C1C423771infoc; buvid4=0C7969B3-30B9-CFB1-018C-1205C7C8F85923849-022040314-QNSSPBkStCz+fzhvQbib7A==; PVID=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; nostalgia_conf=-1; CURRENT_QUALITY=0; b_lsid=B5CFB7ED_180604D7444; bp_video_offset_1852246931=652718863031468000; b_ut=5; CURRENT_FNVAL=4048; fingerprint=8852141fcfdc9c3d7979cda89ca20532; SESSDATA=13516d7d,1666437461,28978*41; bili_jct=b00b3cd8afb4e9843570750118696069; DedeUserID=1389441380; DedeUserID__ckMd5=e0b37c6331e3d33e; sid=l6usxdde; buvid_fp=2c10474b0cbb00068739c2c1ee3c92fa; innersign=1",
    "_uuid=34E510B66-CC10B-F18C-3ACF-C83C18ABDA5681925infoc; CURRENT_QUALITY=0; buvid4=70F1DCAE-065E-554C-465A-AE5F7764F73754826-022012517-Y9nqlHliUbCiKrdoBMyFgQ==; buvid3=1FFD497C-57F5-9EDE-0AB3-573E7A966E5582579infoc; b_nut=1650800882; rpdid=|(umk~u~~RJR0J'uYl|)||))J; nostalgia_conf=-1; buvid_fp_plain=undefined; blackside_state=0; fingerprint3=4e49bfe6044a74d5b467cd14bcb3319a; i-wanna-go-back=-1; b_ut=5; PVID=2; bp_video_offset_1010453476=undefined; CURRENT_BLACKGAP=0; bp_video_offset_299704892=651951768974917800; bp_video_offset_1056224014=undefined; b_lsid=D8FD61B2_180606730DE; bp_video_offset_1033951691=undefined; innersign=1; CURRENT_FNVAL=4048; fingerprint=c0d1c0bfc8b45b0e0b5cc737e04bd16e; SESSDATA=188c0ea5,1666437560,b4300*41; bili_jct=b13bc71b2dea963770ff76a7f1f6a0c3; DedeUserID=1389441380; DedeUserID__ckMd5=e0b37c6331e3d33e; sid=cp0jwn6y; buvid_fp=c0d1c0bfc8b45b0e0b5cc737e04bd16e",
    ]
    user_agent_pool=[ # User-Agent池
    # Cent Browser 4.3.9.248，Chromium 86.0.4240.198
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
 
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38', # 2021.09
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.37',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47', # 2021.10
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44', # 2021.11
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41', # 2021.12
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55', # 2022.01
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43', # 2022.02
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.55',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30', # 2022.03
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29', # 2022.04
 
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', # 2021.10
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', # 2021.11
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36', # 2021.12
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36', # 2022.01
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36', # 2022.02
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', # 2022.03
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
 
    # Chrome Beta
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.41 Safari/537.36', # 2021.09
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.17 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.32 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.40 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.49 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.18 Safari/537.36', # 2021.10
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.27 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.35 Safari/537.36', # 2021.11
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
 
    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0', # 2021.09
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0', # 2021.10
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', # 2021.11
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0', # 2021.12
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0', # 2022.01
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0', # 2022.02
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0', # 2022.03
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0', # 2022.04
]

    header = {
        'accept': 'application/json, text/plain, */*',
		#'Cookie': cookie,
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.bilibili.com',
        #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
	#bvid=input('输入Bvid：')
	#cid = get_cid(bvid)
	
    bvid,cid = readTxt()
    dates=get_dates()
    fname = bvid + '_弹幕2.csv'
    with open(fname, 'w+', newline='', encoding='utf_8_sig') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["时间","弹幕", "发送时间", "弹幕dmID", "弹幕类型", "弹幕字号", "弹幕颜色"])
        for ditem in tqdm(dates):
            url=orgin_url.format(cid,ditem)
            try:
                header['user-agent']=random.choice(user_agent_pool)
                header['Cookie']=random.choice(cookie_pool)
                html = requests.request(url=url, method='get', headers=header)
            except:
                print(ditem,':爬取获取数据失败')
                continue
            DM = DmSegMobileReply()
            DM.ParseFromString(html.content)
            data_json = json.loads(MessageToJson(DM))
            for i in data_json['elems']:
                try:
                    ctime = get_time(i['ctime'])
                    message = i['content']
                    ptime = get_time2(i['progress'])
                    id = i['id']
                    mode = i['mode']
                    fontsize = i['fontsize']
                    color = i['color']
                except:
                    continue
                csv_writer.writerow([ptime, message, ctime, id, mode, fontsize, color])
            time.sleep(5)
        f.close()

		#去重
        data = pd.read_csv(fname)

        total1 = len(open(fname,"r",encoding='utf-8').readlines())
        print("去重前数据：",total1)

        datalist =data.drop_duplicates(subset = None, keep = 'first',inplace=False)

        fname1 = bvid + '_弹幕改2.csv'
        datalist.to_csv(fname1,index=False,encoding='utf_8_sig')

        total2 = len(open(fname1,"r",encoding='utf-8').readlines())
        print("去重后数量：",total2)