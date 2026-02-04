import datetime
import hashlib
import math
import time
import urllib.parse
import pandas as pd
import schedule
import sqlalchemy
from pprint import pprint

import requests

# 爬取B站UP主投稿数据
from openpyxl import load_workbook
from sqlalchemy import create_engine


def get_rid(params):
    sorted_dict = dict(sorted(params.items()))
    o = "ea1db124af3c7062474693fa704f4ff8"
    h = urllib.parse.urlencode(sorted_dict)
    combined = h + o
    md5 = hashlib.md5(combined.encode()).hexdigest()
    params['w_rid'] = md5
    return params

def get_data(url, header, mid, pn):
    url = url
    header = header
    params = {
        'pn': pn,
        'ps': 40,
        'tid': 0,
        'special_type': '',
        'order': 'pubdate',
        'mid': mid,
        'index': 0,
        'keyword': '',
        'order_avoided': 'true',
        'platform': 'web',
        'web_location': '333.1387',
        'dm_img_list': '[]',
        'dm_img_str': 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',
        'dm_cover_img_str': 'QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgUlRYIDMwNTAgTGFwdG9wIEdQVSAoMHgwMDAwMjVFMikgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSlHb29nbGUgSW5jLiAoTlZJRElBKQ',
        'dm_img_inter': '{"ds":[],"wh":[3699,3263,89],"of":[95,190,95]}',
        'w_webid': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcG1faWQiOiIzMzMuOTk5IiwiYnV2aWQiOiI3OTA5MERDRi1DN0JGLUZFOTMtQjFFMi01OTI1OTU2Rjc2NEY4Mjc5M2luZm9jIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzMuMC4wLjAgU2FmYXJpLzUzNy4zNiBFZGcvMTMzLjAuMC4wIiwiYnV2aWRfZnAiOiJmZmUxMTBhYWFkN2Y4MjcyZTI1YTk2Y2FiOWYzMmIwOCIsImJpbGlfdGlja2V0IjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNkluTXdNeUlzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNOREF4TXprd01ESXNJbWxoZENJNk1UY3pPVGczT1RjME1pd2ljR3gwSWpvdE1YMC5BQXhhU2ZIM0N5c1p2NEhMWm84bVFvTmhOYTNPT2hCeDNNRS1aaEhlMlBJIiwiY3JlYXRlZF9hdCI6MTczOTg3OTg0MSwidHRsIjo4NjQwMCwidXJsIjoiLzg2NzU4NjEwL3VwbG9hZC92aWRlbyIsInJlc3VsdCI6MCwiaXNzIjoiZ2FpYSIsImlhdCI6MTczOTg3OTg0MX0.Fg9i8WbxUfx1ZawbBg8Szrn-Zi_wQoXTU6OPlthwk4sRvUZZXOhA5AnPGGQI4X3pL26OGv3BPaNplmn6SOFoUsr3oyARhu1_yAachI9Bqq_ChRmHHt6qHO-yG6G6zXsFKPuZBhi1ngRITzYFRACGFLKIb8JCtGG4YIy5RToMgx5I0ELO1JPbeYFk3PSJR-UPIZ_t8AoPoPt87yjAh3KhRCHBtZQ9tK72eKG_GoS4Pd3-TwYPHBbhwrWFrl1nH0sDl3lM9CP0BWd4h0hBTU_eu41eGVyMFEnn4SxuYSi5tFftAe8ZnXbA85zTGAWS9zcI6vdVdKjg_X9gLWDVo-mPbg',
        # 'w_rid': '50a88768f5bd0bda63a8a7ab06a10677',
        'wts': int(time.time())
    }
    params = get_rid(params)
    return requests.get(url, headers=header, params=params).json()
def get_batch_data(url, header, mid):
    all_data = []
    res = get_data(url=url, header=header, mid=mid, pn=1)
    all_data.append(res)
    count = res['data']['page']['count']
    page = math.ceil(count / 40)
    if page == 1:
        pass
    else:
        for i in range(2, page + 1):
            res = get_data(url=url, header=header, mid=mid, pn=i)
            all_data.append(res)
    return all_data
def parse_data(all_data):
    empty_df = pd.DataFrame()
    for data in all_data:
        vlist = data['data']['list']['vlist']
        empty_df = pd.concat([empty_df, pd.DataFrame(vlist)])
    now = datetime.datetime.now().replace(microsecond=0)
    empty_df['获取时间'] = now
    empty_df['创建时间'] = pd.to_datetime(empty_df['created'], unit='s')
    empty_df['meta'] = empty_df['meta'].astype('str')
    book = pd.DataFrame(pd.read_excel(r'D:\数据自动化与可视化实战\test.xlsx'))
    pd.concat([book, empty_df]).to_excel(r'D:\数据自动化与可视化实战\test.xlsx', index=False)
    return empty_df
def parse_data_GUI(all_data):
    empty_df = pd.DataFrame()
    for data in all_data:
        vlist = data['data']['list']['vlist']
        empty_df = pd.concat([empty_df, pd.DataFrame(vlist)])
    now = datetime.datetime.now().replace(microsecond=0)
    empty_df['获取时间'] = now
    empty_df['创建时间'] = pd.to_datetime(empty_df['created'], unit='s')
    empty_df['meta'] = empty_df['meta'].astype('str')
    return empty_df

def sava_data(df):
    engine = create_engine(f'mysql+pymysql://root:1234@localhost:3306/bilibili')
    try:
        # 尝试连接数据库
        connection = engine.connect()
        print("成功连接到 MySQL 数据库")
        df.to_sql('UP投稿数据', connection, if_exists='append', index=False)
        # 关闭连接
        connection.close()
    except Exception as e:
        print(f"连接失败: {e}")
def demo_for_GUI(mid):
    url = "https://api.bilibili.com/x/space/wbi/arc/search?"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Cookie": "header_theme_version=CLOSE; buvid4=902B2BE0-C5D3-DF1F-51C2-40113835646583602-022070311-0gBoswW8oqDLeIml%2FM6WaGMOwV6huqW2%2FhahmHVrNFdfqnmROizLAg%3D%3D; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; CURRENT_QUALITY=64; _uuid=1064967E3-7CFF-C93D-F10FF-F3DDF8683AF162373infoc; hit-dyn-v2=1; DedeUserID=291245814; DedeUserID__ckMd5=f764aa65158f1dbd; LIVE_BUVID=AUTO1317349485877302; fingerprint=ffe110aaad7f8272e25a96cab9f32b08; buvid_fp_plain=undefined; buvid_fp=ffe110aaad7f8272e25a96cab9f32b08; home_feed_column=5; browser_resolution=1528-738; buvid3=79090DCF-C7BF-FE93-B1E2-5925956F764F82793infoc; b_nut=1737734186; enable_feed_channel=DISABLE; PVID=4; bsource=search_bing; rpdid=|(um~Rku~~J|0J'u~Jmk)u)~m; bp_t_offset_291245814=1032703334177308672; CURRENT_FNVAL=4048; b_lsid=339426BA_19518EAE937; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDAxMzkwMDIsImlhdCI6MTczOTg3OTc0MiwicGx0IjotMX0.AAxaSfH3CysZv4HLZo8mQoNhNa3OOhBx3ME-ZhHe2PI; bili_ticket_expires=1740138942; SESSDATA=24130b03%2C1755431803%2C28f02%2A21CjAMmwyu0GV8FrNjIOKftMTOgvooyfm40KYeRidR11Z__pA33JZASKUnN-nZaEnXLPESVkhWUndKa0V1YzM2MkNwSV9BVVZDcVh2OU1LWFlRWTNGdERndmhuZHFvYlNxTTg5XzBBcXB6NnlPdWN1YkRXZDhfMGhMRzZpSzlPbmYtMVZvcFF0dHRBIIEC; bili_jct=0ae123a2017459c37befff9cb3c93738; sid=fgpuykbg",
        "Referer": "https://space.bilibili.com"
    }
    all_data = get_batch_data(url, header, mid)
    df = parse_data_GUI(all_data)
    return df
def parse_for_BI():
    df = pd.read_excel(r'D:\数据自动化与可视化实战\test.xlsx')
    df.rename(columns={'author' : 'UP主', 'title' : '视频标题', 'play' : '播放数', 'comment' : '评论数'}, inplace=True)
    gp = df.groupby(['UP主', '视频标题', 'bvid'], as_index=False)
    df['昨日播放数'] = gp['播放数'].shift(-1)
    df['播放增长'] = df['播放数'] - df['昨日播放数']
    df.to_excel('up_投稿数据_p.xlsx',  index=False)
def job():
    bili_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Cookie": "header_theme_version=CLOSE; buvid4=902B2BE0-C5D3-DF1F-51C2-40113835646583602-022070311-0gBoswW8oqDLeIml%2FM6WaGMOwV6huqW2%2FhahmHVrNFdfqnmROizLAg%3D%3D; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; CURRENT_QUALITY=64; _uuid=1064967E3-7CFF-C93D-F10FF-F3DDF8683AF162373infoc; hit-dyn-v2=1; DedeUserID=291245814; DedeUserID__ckMd5=f764aa65158f1dbd; LIVE_BUVID=AUTO1317349485877302; fingerprint=ffe110aaad7f8272e25a96cab9f32b08; buvid_fp_plain=undefined; buvid_fp=ffe110aaad7f8272e25a96cab9f32b08; home_feed_column=5; browser_resolution=1528-738; buvid3=79090DCF-C7BF-FE93-B1E2-5925956F764F82793infoc; b_nut=1737734186; enable_feed_channel=DISABLE; PVID=4; bsource=search_bing; rpdid=|(um~Rku~~J|0J'u~Jmk)u)~m; bp_t_offset_291245814=1032703334177308672; CURRENT_FNVAL=4048; b_lsid=339426BA_19518EAE937; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDAxMzkwMDIsImlhdCI6MTczOTg3OTc0MiwicGx0IjotMX0.AAxaSfH3CysZv4HLZo8mQoNhNa3OOhBx3ME-ZhHe2PI; bili_ticket_expires=1740138942; SESSDATA=24130b03%2C1755431803%2C28f02%2A21CjAMmwyu0GV8FrNjIOKftMTOgvooyfm40KYeRidR11Z__pA33JZASKUnN-nZaEnXLPESVkhWUndKa0V1YzM2MkNwSV9BVVZDcVh2OU1LWFlRWTNGdERndmhuZHFvYlNxTTg5XzBBcXB6NnlPdWN1YkRXZDhfMGhMRzZpSzlPbmYtMVZvcFF0dHRBIIEC; bili_jct=0ae123a2017459c37befff9cb3c93738; sid=fgpuykbg",
        "Referer": "https://space.bilibili.com"
    }
    url = "https://api.bilibili.com/x/space/wbi/arc/search?"
    mid = 86758610
    # mid = 18684696
    # all_data是一个列表
    all_data = get_batch_data(url, bili_headers, mid)
    # sava_data(parse_data(all_data))
    parse_data(all_data)
if __name__=="__main__":
    # schedule.every().day.at("9:30").do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # job()
    url = "https://api.bilibili.com/x/space/wbi/arc/search?"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Cookie": "header_theme_version=CLOSE; buvid4=902B2BE0-C5D3-DF1F-51C2-40113835646583602-022070311-0gBoswW8oqDLeIml%2FM6WaGMOwV6huqW2%2FhahmHVrNFdfqnmROizLAg%3D%3D; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_HEADER_LIVE_NO_POP; CURRENT_QUALITY=64; _uuid=1064967E3-7CFF-C93D-F10FF-F3DDF8683AF162373infoc; hit-dyn-v2=1; DedeUserID=291245814; DedeUserID__ckMd5=f764aa65158f1dbd; LIVE_BUVID=AUTO1317349485877302; fingerprint=ffe110aaad7f8272e25a96cab9f32b08; buvid_fp_plain=undefined; buvid_fp=ffe110aaad7f8272e25a96cab9f32b08; home_feed_column=5; browser_resolution=1528-738; buvid3=79090DCF-C7BF-FE93-B1E2-5925956F764F82793infoc; b_nut=1737734186; enable_feed_channel=DISABLE; PVID=4; bsource=search_bing; rpdid=|(um~Rku~~J|0J'u~Jmk)u)~m; bp_t_offset_291245814=1032703334177308672; CURRENT_FNVAL=4048; b_lsid=339426BA_19518EAE937; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDAxMzkwMDIsImlhdCI6MTczOTg3OTc0MiwicGx0IjotMX0.AAxaSfH3CysZv4HLZo8mQoNhNa3OOhBx3ME-ZhHe2PI; bili_ticket_expires=1740138942; SESSDATA=24130b03%2C1755431803%2C28f02%2A21CjAMmwyu0GV8FrNjIOKftMTOgvooyfm40KYeRidR11Z__pA33JZASKUnN-nZaEnXLPESVkhWUndKa0V1YzM2MkNwSV9BVVZDcVh2OU1LWFlRWTNGdERndmhuZHFvYlNxTTg5XzBBcXB6NnlPdWN1YkRXZDhfMGhMRzZpSzlPbmYtMVZvcFF0dHRBIIEC; bili_jct=0ae123a2017459c37befff9cb3c93738; sid=fgpuykbg",
        "Referer": "https://space.bilibili.com"
    }
    # parse_for_BI()
    print(demo_for_GUI(mid=86758610))



