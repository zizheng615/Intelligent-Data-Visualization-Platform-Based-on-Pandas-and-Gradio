import re

import requests
import urllib.parse
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "acw_tc=0a00d56417401494637693921ea26239cbc407f0cb4f3e551d90bda7aa613a; abRequestId=f64b43a8-706b-5633-836b-fb69ce832653; webBuild=4.57.0; xsecappid=xhs-pc-web; loadts=1740149465134; a1=19528fda02eurmwdiajhl9h3t6z5khlw3oaxx75b050000408011; webId=efd00595156ca9d55c0bc59c4d7ac21a; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=0e54ac99-5911-4ee6-988a-fbedbc7ea9c7; gid=yj2JYif0DJqSyj2JYif08lW2Jd7F6Ef30Vx10D8jxq9KuC282Tx1EC88848Y8yy8jdjdi0j0; web_session=040069b38660cf2f08849bda8d354b390e1ab1; unread={%22ub%22:%2267b2b9a8000000002901425c%22%2C%22ue%22:%2267b884fc0000000029028f61%22%2C%22uc%22:29}",
    "Priority": "u=0, i",
    "Referer": "https://www.baidu.com/",
    "Sec-Ch-Ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.12181 SLBChan/105 SLBVPV/64-bit"
}
# def get_douyin_video():
#     url = 'https://www.douyin.com/discover?modal_id=7442869103049690409'
#     res = requests.get(url=url, headers=headers)
#     print(res.text)
def get_xhs_video(url):

    # data = {"source_note_id":"67b6f8560000000029032eb2","image_formats":["jpg","webp","avif"],"extra":{"need_body_topic":"1"},"xsec_source":"pc_feed","xsec_token":"AB6UPiqb7TLfZi_dfXD1o-q6rIzZ56zPQyAkGZZGP16DI="}
    res = requests.get(url, headers=headers)
    # 定义正则表达式模式
    pattern1 = r'<span data-v-14f91c23 data-v-0cdd7be0>(.*?)</span>'
    # 使用 re.findall 方法进行匹配
    title = re.findall(pattern1, res.text)
    # 定义正则表达式模式
    pattern2 = r'"backupUrls":\["(.*?\.mp4)"\]'
    # 使用 re.findall 方法进行匹配
    matches = re.findall(pattern2, res.text)
    video_url = matches[0].encode('utf-8').decode('unicode_escape').split(',')[0][ : -1]
    res = requests.get(video_url)
    with open(rf'./视频存储/{title[0]}.mp4', 'wb') as f:
        f.write(res.content)
    return f'D:/数据自动化与可视化实战/项目二/视频存储/{title[0]}.mp4'
if __name__=="__main__":
    url = 'https://www.xiaohongshu.com/explore/6793a2ff0000000018010b4e?xsec_token=ABI_6ta_cnhzkA2h_o7uT38XNlh6lJIOTkFP_4zWJ1-lw=&xsec_source=pc_feed'
    # url = 'https://www.xiaohongshu.com/explore/67b7fa4e000000000b0173f6?xsec_token=ABipoftEI1tuVe1VtCUEIBH5Hj---qv7CThr2Bxmpq1P4=&xsec_source=pc_feed'
    get_xhs_video(url)
