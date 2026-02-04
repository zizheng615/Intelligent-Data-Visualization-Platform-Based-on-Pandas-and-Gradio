import os.path
from pprint import pprint

import requests
import re

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "abRequestId=f64b43a8-706b-5633-836b-fb69ce832653; webBuild=4.57.0; xsecappid=xhs-pc-web; a1=19528fda02eurmwdiajhl9h3t6z5khlw3oaxx75b050000408011; webId=efd00595156ca9d55c0bc59c4d7ac21a; gid=yj2JYif0DJqSyj2JYif08lW2Jd7F6Ef30Vx10D8jxq9KuC282Tx1EC88848Y8yy8jdjdi0j0; web_session=040069b38660cf2f08849bda8d354b390e1ab1; acw_tc=0a00d86f17402276652954236e89d2c0457928b2e0f14ca7ae78dbb2af5747; loadts=1740227667994; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=cc702531-ed71-41fd-bafa-44291620d601; unread={%22ub%22:%2267b88420000000000e00471c%22%2C%22ue%22:%2267b89ad7000000002903870f%22%2C%22uc%22:27}",
        "Priority": "u=0, i",
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
def extract_initial_state(html_content):
    # 正则表达式模式（支持多行匹配）
    pattern = re.compile(
        r'window\.__INITIAL_STATE__\s*=\s*(.*?)\s*;?\s*</script>',
        flags=re.DOTALL  # 允许匹配换行符
    )

    # 搜索匹配内容
    match = pattern.search(html_content)
    if match:
        return match.group(1).strip()  # 返回捕获组并去除首尾空格
    else:
        return None
def get_xhs_pictures(url):
    pattern = re.compile(r'explore/.*?\?')
    matches = pattern.findall(url)[0][ : -1][8 : ]
    res = requests.get(url, headers=headers)
    result = extract_initial_state(res.text)
    true = 'true'
    false = 'false'
    undefined = None
    null = None
    title = eval(result)['note']['noteDetailMap'][f'{matches}']['note']['title'].replace('|', '')
    imageList = eval(result)['note']['noteDetailMap'][f'{matches}']['note']['imageList']
    imageList = [image['urlDefault'] for image in imageList]
    # pprint(imageList)
    # pprint(title)
    if not os.path.exists(f'D:/数据自动化与可视化实战/项目三/图片存放/{title}'):
        os.mkdir(f'D:/数据自动化与可视化实战/项目三/图片存放/{title}')
    img_list = []
    for i in range(len(imageList)):
        res = requests.get(imageList[i])
        with open(f'D:/数据自动化与可视化实战/项目三/图片存放/{title}/{i}_{title}.jpg', 'wb') as f:
            img_list.append(f'D:/数据自动化与可视化实战/项目三/图片存放/{title}/{i}_{title}.jpg')
            f.write(res.content)
    return f'D:/数据自动化与可视化实战/项目三/图片存放/{title}', img_list
if __name__ == "__main__":
    url = 'https://www.xiaohongshu.com/explore/644d27bc000000002701340f?xsec_token=AByywxj-VLfwXt2rCRqLKHnBDUfmb81YtIlKzNyO3w97w=&xsec_source=pc_cfeed'
    get_xhs_pictures(url)