# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import re
import requests
from  datetime import datetime
from wxpy import *
from requests import get
from requests import post
from platform import system
from random import choice, randint
from threading import Thread
import configparser
import time
from bs4 import BeautifulSoup


class Words():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }

    def get_weather_info(self, city_code='101250101'):
        # url = "http://t.weather.sojson.com/api/weather/city/" + city_code
        # content = urllib.request.urlopen(url).read().decode("utf-8")
        url = "http://t.weather.itboy.net/api/weather/city/" + city_code

        # all_data = json.loads(content)
        all_data = requests.get(url).json()

        # print(all_data)

        data = all_data['data']
        forecast = data["forecast"][0]
        # print(forecast)
        ymd = forecast["ymd"]
        week = forecast["week"]
        notice = forecast["notice"]
        type = forecast["type"]
        low = forecast["low"].split()[1]
        high = forecast["high"].split()[1]
        fx = forecast["fx"]

        # weather_msg = "小可爱,今天是" + ymd + "," + week + "\n" + notice + "\n" + "天气:" + type + "\n" \
        #               + "气温:" + low + "~" + high + "\n" + "遇事不决,可问" + fx + "\n"
        weather_msg = "小可爱,今天是{ymd},{week}\n {notice} \n 天气:{type} \n 气温:{low}~{high} \n 遇事不决,可问{fx}哦 \n" \
            .format(ymd=ymd, week=week, notice=notice, type=type, low=low, high=high, fx=fx)

        return weather_msg

    def get_dictum_info(self):
        print('获取格言信息..')
        user_url = 'http://wufazhuce.com/'
        resp = requests.get(user_url, headers=self.headers)
        soup_texts = BeautifulSoup(resp.text, 'lxml')
        # 『one -个』 中的每日一句
        every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
        return every_msg + "\n"

    # 获取每日励志精句
    def get_message(self):
        r = get("http://open.iciba.com/dsapi/")
        note = r.json()['note']
        content = r.json()['content']
        return note, content
    ## 污话
    def get_train_word(self):
        url = "https://www.nihaowua.com/"
        r = requests.get(url)
        pattern = re.compile("<section>.*</section>", re.S)
        section = re.findall(pattern, r.text)
        train_words = section[0].split(">")[3].split("<")[0]
        # print(train_words)
        return train_words

    def get_all_song(self):
        ### 评论过十万的华语单曲（不定期更新）
        url = "https://music.163.com/playlist?id=2193426092"
        r = requests.get(url)
        pattern = r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'
        song = re.findall(pattern, r.text)
        # print(song)
        pattern_name = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'
        pattern_id = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'
        song_name = re.findall(pattern_name, song[0])
        song_id = re.findall(pattern_id, song[0])
        # print(song_name)
        # print(song_id)
        return song_name, song_id

    def get_music_msg(self,song_name, song_id):
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + song_id + '?csrf_token='  # 歌评url
        data = {
            "params": "w7dsLfmFlYLbnkeu/5uwDQiRNdohVjDmCgUiLce56Wp41EUbnybKG3mQo2gz56Kly4x3gb8W+kbfWcWndnzXPfikLrgpQ83KbeMzxje0MihelK5IHhfOG+lg+ZvY068+bg9Vn8/M97KFoSwhF1k5BWwVkcxB99pqB7aJ1DO6bxjjClpc4mfTQyI6bSiugIV9Xr5NCsAdXO/iWbafxua1XTtbQSST81hWksznBq6bKwY=",
            "encSecKey": "c972a5e9546868e97d430e494e2358e3b2bf59eb78210765a1913201dfa1fd5b0c406d3fc33c738e9a3de018691f47c18acac283604e6d850ef5fb2a686fac6513b964db14e5caf79cf95686646c691b7bcebe059c7624e19694db35baa6ef6e775979cf471fe211747264ab60db004207eb11c8cb1ffb5429650f8e97007239"}

        r = requests.post(url, data=data)
        hot_commit = r.json()["hotComments"]
        music_msg = "小宝贝，今天的工作也辛苦啦~~听首歌，放松一下吧\n" + "https://music.163.com/#/song?id=" + song_id + "  《" + song_name + "》\n"
        # + "精彩评论：" + \
                    # hot_commit[1]["content"] + "\n" \
                    # + hot_commit[2]["content"] + "\n"

        return music_msg


# 发送消息给她
def send_message(your_message):
    try:
        # 对方的微信名称
        my_friend = bot.friends().search(my_lady_wechat_name)[0]
        # 发送消息给对方
        my_friend.send(your_message)
    except:
        # 出问题时，发送信息到文件传输助手
        bot.file_helper.send(u"守护女友出问题了，赶紧去看看咋回事~")

# 发送图片给她
def send_img():
    url = "https://source.unsplash.com/random/1280x720"
    r = requests.get(url)
    # with open("./image/{}.jpg".format(time.ctime()), "wb") as f:
    #     img_path = "./image/" + time.ctime() + ".jpg"
    #     f.write(r.content)
    with open("toyugg.jpg","wb") as f:
        f.write(r.content)

    path = "./toyugg.jpg"

    my_friend = bot.friends().search(my_lady_wechat_name)[0]
    my_friend.send_image(path)




# 在规定时间内进行关心她操作
def start_care():
    # 待发送的内容，先置为空
    message = ""
    word = Words()
    song_name, song_id = word.get_all_song()
    # 来个死循环，24小时关心她
    while (True):
        # 提示
        print("守护中，时间:%s" % time.ctime())
        # 每天定时问候，早上起床，中午吃饭，晚上吃饭，晚上睡觉
        # 获取时间，只获取时和分，对应的位置为倒数第13位到倒数第8位
        now_time = time.ctime()[-13:-8]
        if (now_time == say_good_morning):
            # 随机取一句问候语
            message = choice(str_list_good_morning)

            # 是否加上随机表情
            if (flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            send_img()
            print("提醒女友早上起床:%s" % time.ctime())

        elif (now_time == say_weather):

            message = word.get_weather_info()
            if (flag_wx_emoj):
                message = word.get_weather_info() + choice(str_list_emoj)
            send_message(message)
            print("你的播报小天使已经上线:%s" % time.ctime())

        elif (now_time == say_good_lunch):
            message = choice(str_list_good_lunch)

            # 是否加上随机表情
            if (flag_wx_emoj):
                message = message + choice(str_list_emoj)+"\n" + "ONE一个:" + word.get_dictum_info()

            send_message(message)
            send_img()
            print("提醒女友中午吃饭:%s" % time.ctime())

        elif (now_time == say_good_dinner):
            message = choice(str_list_good_dinner)

            # 是否加上随机表情
            if (flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            send_img()
            print("提醒女友晚上吃饭:%s" % time.ctime())
        elif (now_time == say_music):
            i = (datetime.today() - datetime(2019, 5, 21)).days
            if i < len(song_id):
                music_msg = word.get_music_msg(song_name[i], song_id[i])
            if len(list_zhihu):
                _,zhihu_word = list_zhihu.pop(randint(0,len(list_zhihu))).split(".")


            send_message(music_msg+"\n"+zhihu_word)


        elif (now_time == say_good_dream):

            # 是否在结尾加上每日学英语
            if (flag_learn_english):
                note, content = word.get_message()
                message = choice(str_list_good_dream) + "\n\n" + "顺便一起来学英语哦：\n" + content
            else:
                message = choice(str_list_good_dream)

            # 是否加上随机表情
            if (flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            send_img()
            print("提醒女友晚上睡觉:%s" % time.ctime())


        # 每60秒检测一次
        time.sleep(60)


if __name__ == "__main__":

    # 若发现读取取配置文件出错，可以取消注释下面这行，一般在pycharm环境下才需要增加
    # 设置当前文件所在的目录为当前工作路径
    # chdir(sys.path[0])

    # 启动微信机器人，自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if ('Windows' in system()):
        # Windows
        bot = Bot()
    elif ('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif ('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2, cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")

    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read("./config.ini", encoding='UTF-8')

    # 设置女友的微信名称，记住，不是微信ID也不是微信备注
    # 你女友的微信名称，记住，不是微信ID也不是微信备注
    my_lady_wechat_name = cf.get("configuration", "my_lady_wechat_name")

    # 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
    say_good_morning = cf.get("configuration", "say_good_morning")
    say_weather = cf.get("configuration", "say_weather")
    say_good_lunch = cf.get("configuration", "say_good_lunch")
    say_good_dinner = cf.get("configuration", "say_good_dinner")
    say_good_dream = cf.get("configuration", "say_good_dream")
    say_music =cf.get("configuration","say_music")

    # 设置女友生日信息
    # 几月，注意补全数字，为两位数，比如6月必须写成06
    birthday_month = cf.get("configuration", "birthday_month")
    # 几号，注意补全数字，为两位数，比如6号必须写成08
    birthday_day = cf.get("configuration", "birthday_day")

    # 读取早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间的随机提示语
    # 一般这里的代码不要改动，需要增加提示语可以自己打开对应的文件修改
    # 早上起床问候语列表，数据来源于新浪微博
    with open("./remind_sentence/zhihu","r",encoding="utf-8") as f:
        list_zhihu = f.readlines()


    str_list_good_morning = ''
    with open("./remind_sentence/sentence_good_morning.txt", "r", encoding='UTF-8') as f:
        str_list_good_morning = f.readlines()
    # print(str_list_good_morning)

    # 中午吃饭问候语列表，数据来源于新浪微博
    str_list_good_lunch = ''
    with open("./remind_sentence/sentence_good_lunch.txt", "r", encoding='UTF-8') as f:
        str_list_good_lunch = f.readlines()
    # print(str_list_good_lunch)

    # 晚上吃饭问候语列表，数据来源于新浪微博
    str_list_good_dinner = ''
    with open("./remind_sentence/sentence_good_dinner.txt", "r", encoding='UTF-8') as f:
        str_list_good_dinner = f.readlines()
    # print(str_list_good_dinner)

    # 晚上睡觉问候语列表，数据来源于新浪微博
    str_list_good_dream = ''
    with open("./remind_sentence/sentence_good_dream.txt", "r", encoding='UTF-8') as f:
        str_list_good_dream = f.readlines()
    # print(str_list_good_dream)

    # 设置晚上睡觉问候语是否在原来的基础上再加上每日学英语精句
    # False表示否 True表示是

    if ((cf.get("configuration", "flag_learn_english")) == '1'):
        flag_learn_english = True
    else:
        flag_learn_english = False
    # print(flag_learn_english)

    # 设置所有问候语结束是否加上表情符号
    # False表示否 True表示是
    str_emoj = "(•‾̑⌣‾̑•)✧˖°----(๑´ڡ`๑)----(๑¯ิε ¯ิ๑)----(๑•́ ₃ •̀๑)----( ∙̆ .̯ ∙̆ )----(๑˘ ˘๑)----(●′ω`●)----(●･̆⍛･̆●)----ಥ_ಥ----_(:qゝ∠)----(´；ω；`)----( `)3')----Σ((( つ•̀ω•́)つ----╰(*´︶`*)╯----( ´´ิ∀´ิ` )----(´∩｀。)----( ื▿ ื)----(｡ŏ_ŏ)----( •ิ _ •ิ )----ヽ(*΄◞ิ౪◟ิ‵ *)----( ˘ ³˘)----(; ´_ゝ`)----(*ˉ﹃ˉ)----(◍'౪`◍)ﾉﾞ----(｡◝‿◜｡)----(ಠ .̫.̫ ಠ)----(´◞⊖◟`)----(。≖ˇェˇ≖｡)----(◕ܫ◕)----(｀◕‸◕´+)----(▼ _ ▼)----( ◉ืൠ◉ื)----ㄟ(◑‿◐ )ㄏ----(●'◡'●)ﾉ♥----(｡◕ˇ∀ˇ◕）----( ◔ ڼ ◔ )----( ´◔ ‸◔`)----(☍﹏⁰)----(♥◠‿◠)----ლ(╹◡╹ლ )----(๑꒪◞౪◟꒪๑)"
    str_list_emoj = str_emoj.split('----')
    if ((cf.get("configuration", "flag_wx_emoj")) == '1'):
        flag_wx_emoj = True
    else:
        flag_wx_emoj = False
    # print(str_list_emoj)

    # 设置节日祝福语
    # 情人节祝福语
    str_Valentine = cf.get("configuration", "str_Valentine")
    # print(str_Valentine)

    # 三八妇女节祝福语
    str_Women = cf.get("configuration", "str_Women")
    # print(str_Women)

    # 平安夜祝福语
    str_Christmas_Eve = cf.get("configuration", "str_Christmas_Eve")
    # print(str_Christmas_Eve)
    #
    # 圣诞节祝福语
    str_Christmas = cf.get("configuration", "str_Christmas")
    # print(str_Christmas)

    # 她生日的时候的祝福语
    str_birthday = cf.get("configuration", "str_birthday")
    # print(str_birthday)

    # 开始守护女友
    t = Thread(target=start_care, name='start_care')
    t.start()

# 接收女友消息监听器

# 女友微信名
my_girl_friend = bot.friends().search(my_lady_wechat_name)[0]


@bot.register(chats=my_girl_friend, except_self=False)
def print_others(msg):
    # 输出聊天内容
    print(msg.text)

    # 可采用snownlp或者jieba等进行分词、情感分析，由于打包后文件体积太大，故暂时不采用这种方式
    # 仅仅是直接调用网络接口

    # 做极其简单的情感分析
    # 结果仅供参考，请勿完全相信
    postData = {'data': msg.text}
    response = post('https://bosonnlp.com/analysis/sentiment?analysisType=', data=postData)
    data = response.text

    # 情感评分指数(越接近1表示心情越好，越接近0表示心情越差)
    now_mod_rank = (data.split(',')[0]).replace('[[', '')
    print("来自女友的消息:%s\n当前情感得分:%s\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n" % (msg.text, now_mod_rank))

    # 发送信息到文件传输助手
    mood_message = u"来自余格格的消息:" + msg.text + "\n当前情感得分:" + now_mod_rank + "\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n"
    bot.file_helper.send(mood_message)
