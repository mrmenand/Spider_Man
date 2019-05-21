[![Author](https://img.shields.io/badge/Author-mr__menand-yellowgreen.svg)](https://mrmenand.github.io/)
[![情话](https://img.shields.io/badge/%E7%8C%BF%E6%B0%8F%E6%B5%AA%E6%BC%AB-%E6%83%85%E8%AF%9D-green.svg)]()
[![一个](https://img.shields.io/badge/One-%E4%B8%80%E4%B8%AA-yellow.svg)](http://wufazhuce.com/)

## 每日情话
>  爬虫还是非常有用的，毕竟可以说骚话，但我是个菜鸡呀 
### Acknowledgement
[每天不同时间段通过微信发消息提醒女友](https://github.com/shengqiangzhang/examples-of-web-crawlers/tree/master/4.%E6%AF%8F%E5%A4%A9%E4%B8%8D%E5%90%8C%E6%97%B6%E9%97%B4%E6%AE%B5%E9%80%9A%E8%BF%87%E5%BE%AE%E4%BF%A1%E5%8F%91%E6%B6%88%E6%81%AF%E6%8F%90%E9%86%92%E5%A5%B3%E5%8F%8B)    
[用 Python + itchat 写一个爬虫脚本每天定时给多个女友发给微信暖心话](https://github.com/sfyc23/EverydayWechat)   
[wxpy文档](https://wxpy.readthedocs.io/zh/latest/bot.html)    
[Python3爬虫抓取网易云音乐热评实战](https://blog.csdn.net/fengxinlinux/article/details/77950209)


### 首先，祝每个程序员能有个女朋友
- 每天定时问候，早上起床，中午吃饭，晚上吃饭，晚上睡觉
-  情感分析
-  节日问候
-  词霸每日一句
-  播报小天使
-  One一个每日一句
-  ~~撩妹会翻车~~
-  [每日壁纸](https://unsplash.com/)
-  九点下班网易云音乐分享及热评

### 然后只要胆子够大,你可以有几个女朋友
-  只要你车开的够快，你女朋友的???就跟不上你！[你好污呀](https://www.nihaowua.com/)
-  只要把[config.ini](./config.ini)的`my_lady_wechat_name` 多来几个，无限畅聊


### Ubuntun服务器部署
后台启动Python脚本，并把日志写入test.out，会返回一个pid   
`nohup python3 -u words_to_mygirl.py > test.out 2>&1 &`   
查询正在使用Python相关进程pid值   
`ps -ef | grep python3`  
杀掉进程  
`kill -9 pid`
### Problems
- 2017年5月后注册的微信登陆不上网页版微信，如果登陆客户端，会LOG OUT   
- 传输大一点的文件/图片、视频发送失败，限制512KB,（通过`pip install --upgrade itchat`），但是还是没解决

### 最后 
小心车翻，珍爱女友    
如果你有更好的情话,评论区留言呀  




