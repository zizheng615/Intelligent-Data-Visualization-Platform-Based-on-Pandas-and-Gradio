import requests

def get_cid(bvid):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Cookie": "SESSDATA=566c40d5%2C1755706238%2C4cb97%2A21CjAXmmHGH_kaiFJN013so93qZ-PDxlF2Arc6yLq8yM8qDcWPaIHdqKIdJdwxJIm00G0SVjYtOXlEVDM1T2tWR19pdjV1MFBfekUxWmgxZzg4UFFYRHpzRDRlai1LSFpTWWVsVzEzbTI4VHY0UkhXb01GaDlma0FfTXd6YWNTdVlaQ2FyQzgwbHF3IIEC"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            return data["data"]["cid"]
        else:
            print("cid获取失败：", data["message"])
    return None


def get_video(bvid, quality=64):
    cid = get_cid(bvid)
    url = "https://api.bilibili.com/x/player/playurl"
    params = {
        "bvid": bvid,
        "cid": cid,
        "qn": quality,  # 清晰度参数（如 80=1080P, 64=720P）
        "fnval": 0,  # 视频格式（0=flv, 16=dash）
        "fnver": 0,
        "fourk": 0  # 是否允许4K
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Cookie": "SESSDATA=566c40d5%2C1755706238%2C4cb97%2A21CjAXmmHGH_kaiFJN013so93qZ-PDxlF2Arc6yLq8yM8qDcWPaIHdqKIdJdwxJIm00G0SVjYtOXlEVDM1T2tWR19pdjV1MFBfekUxWmgxZzg4UFFYRHpzRDRlai1LSFpTWWVsVzEzbTI4VHY0UkhXb01GaDlma0FfTXd6YWNTdVlaQ2FyQzgwbHF3IIEC"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            # 提取视频分片的URL（可能有多个分段）
            video_urls = [segment["url"] for segment in data["data"]["durl"]]
            # return video_urls
        else:
            print("接口返回错误：", data["message"])
    else:
        print("HTTP请求失败：", response.status_code)
    # return []
    # 获取视频内容
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Cookie": "SESSDATA=566c40d5%2C1755706238%2C4cb97%2A21CjAXmmHGH_kaiFJN013so93qZ-PDxlF2Arc6yLq8yM8qDcWPaIHdqKIdJdwxJIm00G0SVjYtOXlEVDM1T2tWR19pdjV1MFBfekUxWmgxZzg4UFFYRHpzRDRlai1LSFpTWWVsVzEzbTI4VHY0UkhXb01GaDlma0FfTXd6YWNTdVlaQ2FyQzgwbHF3IIEC"
    }
    res = requests.get(video_urls[0], headers=headers)
    # print(res.content)
    with open(r'D:/数据自动化与可视化实战/B站视频/B站视频.mp4', 'wb') as f:
        f.write(res.content)
    return r'D:/数据自动化与可视化实战/B站视频/B站视频.mp4'

if __name__ == "__main__":
    bvid = "BV1hZc5eWEGV"  # 替换为目标视频的BV号
    # 调用示例
    print(get_video(bvid))




