import os
import threading
import time
import json
import re
from Fengniao.http_help import R

img_list = []
imgs_lock = threading.Lock()  # 图片操作锁


class Product(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.__headers = {"Referer": "http://image.fengniaos.com/",
                          "Host": "image.fengniaos.com",
                          "X-Requested-With": "XMLHttpRequest"
                          }
        # 链接模板
        self.__start = "http://image.fengniaos.com/index.php?action=getList&class_id=192&sub_classid=0&page={}&not_in_id={}"
        self.__res = R(headers=self.__headers)

    def run(self):

        # 因为不知道循环次数，所有采用while循环
        index = 2  # 起始页码设置为1
        not_in = "5356548,5356425,5356337,5356302"
        while True:
            url = self.__start.format(index, not_in)
            print("开始操作:{}".format(url))
            index += 1

            content = self.__res.get_content(url, charset="gbk")

            if content is None:
                print("数据可能已经没有了====")
                continue

            time.sleep(3)  # 睡眠3秒
            json_content = json.loads(content)

            if json_content["status"] == 1:
                for item in json_content["data"]:
                    title = item["title"]
                    child_url = item["url"]   # 获取到链接之后

                    img_content = self.__res.get_content(
                        child_url, charset="gbk")
                    print(img_content)

                    pattern = re.compile('"pic_url_1920_b":"(.*?)"')
                    imgs_json = re.findall(pattern, img_content)
                    if len(imgs_json) > 0:

                        if imgs_lock.acquire():
                            img_list.append(
                                {"title": title, "urls": imgs_json})
                            imgs_lock.release()


class Consumer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.__res = R()

    def run(self):
        if not os.path.exists("./HomeImage"):
            os.mkdir("./HomeImage")

        while True:
            if len(img_list) <= 0:
                continue  # 进入下一次循环

            if imgs_lock.acquire():

                data = img_list[0]
                imgs_lock.release()

            urls = [url.replace("\\", "") for url in data["urls"]]

            # 创建文件目录
            for item_url in urls:
                try:
                    file = self.__res.get_file(item_url)

                    with open("./HomeImage/{}".format(str(time.time()) + ".jpg"), "wb+") as f:
                        f.write(file)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    p = Product()
    p.start()

    c = Consumer()
    c.start()
