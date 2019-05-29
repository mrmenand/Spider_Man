import json
import re

import aiohttp
import asyncio
import os

if not os.path.exists("./Portrait"):
    os.mkdir("./Portrait")

async def fetch_img_url(num):
    # 字符串拼接
    url = f'http://bbs.fengniao.com/forum/forum_101_{num}_lastpost.html'
    # 或者直接写成 url = 'http://bbs.fengniao.com/forum/forum_101_1_lastpost.html'
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400',
    }

    async with aiohttp.ClientSession() as session:
        # 获取轮播图地址
        async with session.get(url, headers=headers) as response:
            try:
                url_format = "http://bbs.fengniao.com/forum/pic/slide_101_{0}_{1}.html"
                html = await response.text()  # 获取到网页源码
                pattern = re.compile(r'<div class="picList">([\s\S.]*?)</div>')
                first_match = re.findall(pattern, html)
                href_pattern = re.compile(r'href="/forum/(\d+?)_p(\d+?).html')
                urls = [
                    url_format.format(
                        href_pattern.search(url).group(1),
                        href_pattern.search(url).group(2)) for url in first_match]

                for img_slider in urls:
                    try:
                        async with session.get(img_slider, headers=headers) as slider:
                            slider_html = await slider.text()  # 获取到网页源码
                            try:
                                pic_list_pattern = re.compile(
                                    r'var picList = \[(.*)?\];')
                                pic_list = "[{}]".format(
                                    pic_list_pattern.search(slider_html).group(1))
                                pic_json = json.loads(pic_list)  # 图片列表已经拿到
                                # print(pic_json)
                            except Exception as e:
                                print("代码调试错误")
                                print(pic_list)
                                print("*" * 100)
                                print(e)

                            for img in pic_json:

                                try:
                                    img = img["downloadPic"]
                                    print(img)
                                    async with session.get(img, headers=headers) as img_res:
                                        imgcode = await img_res.read()
                                        with open("Portrait/{}".format(img.split('/')[-1]), 'wb') as f:
                                            f.write(imgcode)
                                            f.close()
                                except Exception as e:
                                    print("图片下载错误")
                                    print(e)
                                    continue

                    except Exception as e:
                        print("获取图片列表错误")
                        print(img_slider)
                        print(e)
                        continue

                print("{}已经操作完毕".format(url))
            except Exception as e:
                print("基本错误")
                print(e)


# 这部分你可以直接临摹
loop = asyncio.get_event_loop()
tasks = asyncio.ensure_future(fetch_img_url(10))
results = loop.run_until_complete(tasks)
