from pprint import pprint

import requests
import pandas as pd

url = 'https://cc.oceanengine.com/creative_radar_api/v1/material/user_interact?material_id=7324257775353446426&app_code=4&past_days=3&list_type=10&msToken=COLuMqt0WnHCwuOn06LeJO-5jveP53DDJBg0mrjsLR7UCcLuNSklRVi5GeuFOG8ktjbPSKCV9z2d8QQB7F9oTalMywYBypAdVVlfJJ9yEdhCVI-VyUXPiEk=&X-Bogus=DFSzswVOdWXANewDtDKAj0kX95zO&_signature=_02B4Z6wo000013FcnsgAAIDDRnhal0t0F19xXJpAALvtrRxTGbWCMO43zHAWDOJBq11WV-WMj6gDu-L-QLXkcOSQep9WNuOUF5sLySV-xFOKc93ELW632ZvwDNGkvu2qObufI9ibqtxbf9hpa3'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'caller':'cc',
    'cookie':'_tea_utm_cache_4031=undefined; ttcid=3b76c7df6bc24d9d8ee477c0ff69e91114; passport_csrf_token=c549d2dbce42495461d8cd72c0c6674d; passport_csrf_token_default=c549d2dbce42495461d8cd72c0c6674d; ttwid=1%7C_QU-YyClfyy7JvjFKFSffzp9zeR4zV5C5YeZFLRow10%7C1740033616%7C90ab0df553e287ed25fe793f83c29517bf225ad74d12e48efb2ecd9ddac34ce4; passport_mfa_token=CjBeAEsxFK0RhL7GG%2FieadOqHroEYhCUx2VW0dID6kahiqZPNxed4v5QfcZuxjdRghkaSgo8KvZ3lYnpUupEXu8GjN1ijW3u8Jr6t%2BdR0l62k5cMfWX41exsWPGYyaRri9%2FG8FFaddTQZyopJ%2BJDEMoXEOqE6g0Y9rHRbCACIgEDHSHtvg%3D%3D; d_ticket=89a209e460608da66a8fdf83793215d187226; odin_tt=02b6af2e1d0d4e90106a2bbab165c55e0b37ffb7db4887a4355da24ba8b32f6d86a219a80cf0084780b8149131dc7b5fbd0165798744c8f390c4319cbcdd84c3; n_mh=lccf6IUe4H-xpLq55826UmB2zFBjNXrE9UwEXbpmhuU; passport_auth_status=eb71565240cd67e2050ed4a4a81a0b3d%2C; passport_auth_status_ss=eb71565240cd67e2050ed4a4a81a0b3d%2C; sid_guard=8b8cd439cabf6a0140446f7a76edb466%7C1740033643%7C5184000%7CMon%2C+21-Apr-2025+06%3A40%3A43+GMT; uid_tt=601582f28d57ab8d2eb612dc5c46a9a9; uid_tt_ss=601582f28d57ab8d2eb612dc5c46a9a9; sid_tt=8b8cd439cabf6a0140446f7a76edb466; sessionid=8b8cd439cabf6a0140446f7a76edb466; sessionid_ss=8b8cd439cabf6a0140446f7a76edb466; is_staff_user=false; sid_ucp_v1=1.0.0-KDI5Nzc4YWI0NTI3NDVhMTdmOWQ5OTU3ZjNiNzM0NmYwNzNkYjZlODkKHwjq1JDnts3zAhDrnNu9BhiyDCAMMOuc270GOAJA7AcaAmxmIiA4YjhjZDQzOWNhYmY2YTAxNDA0NDZmN2E3NmVkYjQ2Ng; ssid_ucp_v1=1.0.0-KDI5Nzc4YWI0NTI3NDVhMTdmOWQ5OTU3ZjNiNzM0NmYwNzNkYjZlODkKHwjq1JDnts3zAhDrnNu9BhiyDCAMMOuc270GOAJA7AcaAmxmIiA4YjhjZDQzOWNhYmY2YTAxNDA0NDZmN2E3NmVkYjQ2Ng; store-region=cn-sc; store-region-src=uid; csrftoken=FMDz3oJeuk9scfNNykgzJgFG; cc_part=stable; msToken=2mDh2bg0c8wJumBDi6FK3D22pNjM5v9Ln0cMqbG2xwCvy5JtayzWc3nrsJfgV6esf1DkSMXI2C2CLc-0Xg-AHtV5dGIHtoXVJ9hrVpw0JdJY_j0BU6o5xQw=; tt_scid=36rjEnH6kGuOLFCpreVFeW.mOJ5xWSw3MPlFcMXzAoMlDl-Y-QC7j7fRC0e7oECY5fdc',
    'priority':'u=1, i',
    'referer':'https://cc.oceanengine.com/inspiration/creative-hot/ad/detail/7324257775353446426?appCode=4&period=3&listType=10&materialType=3',
    'sec-ch-ua':'"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-origin',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'x-csrftoken':'FMDz3oJeuk9scfNNykgzJgFG'
}
# params = {
#     'material_id': 7324257775353446426,
#     'app_code': 4,
#     'past_days': 3,
#     'list_type': 10,
#     'msToken': 'COLuMqt0WnHCwuOn06LeJO-5jveP53DDJBg0mrjsLR7UCcLuNSklRVi5GeuFOG8ktjbPSKCV9z2d8QQB7F9oTalMywYBypAdVVlfJJ9yEdhCVI-VyUXPiEk=',
#     'X-Bogus': 'DFSzswVOdWXANewDtDKAj0kX95zO',
#     '_signature': '_02B4Z6wo000013FcnsgAAIDDRnhal0t0F19xXJpAALvtrRxTGbWCMO43zHAWDOJBq11WV-WMj6gDu-L-QLXkcOSQep9WNuOUF5sLySV-xFOKc93ELW632ZvwDNGkvu2qObufI9ibqtxbf9hpa3'
# }
def get_mp4(vid, mid, title):
    url = 'https://cc.oceanengine.com/creative_radar_api/v1/video/info?msToken=X1QJO2woqjS5xk7QDZUF6cN3zyrIWoA5BGGJ8ToNf4ASBhsCV46JqIEdWrfsRX-_40AcRe0UcKQiqFoKpmWFpGeNXAQz-3n2fvUtzgAllqcNmT8_NhtOwd4go4LYigVW&X-Bogus=DFSzswVOQfk9xFwDtDKYe0kX95Fy&_signature=_02B4Z6wo00001GKlgJAAAIDAVYFEzJVOmjhipYQAAH8n7nK2iVuzZ-uDbxQyqvzBBesMrUQLvfVhhJrllt-5XJoXgthHxDBVEHSrIuQ7KZMy9Tx92Cn90FcTqI1Zb-di9kY3UQOtgsGLN-AS81'
    data = {"video_infos": [{"vid": vid,
                             "mid": str(mid)}],
            "water_mark": "creative_center",
            "queryParams": {}}
    res = requests.post(url, json=data, headers=headers)
    video_url = res.json()['data'][mid]['video_url']
    res = requests.get(video_url)
    with open(f'./视频存储/{title}.mp4', 'wb') as f:
        f.write(res.content)

if __name__ == '__main__':
    # data = requests.get(url, headers=headers)
    # data.encoding = 'utf-8'
    # print(data.text)

