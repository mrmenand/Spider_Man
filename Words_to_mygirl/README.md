[![Author](https://img.shields.io/badge/Author-mr__menand-yellowgreen.svg)](https://mrmenand.github.io/)
[![情话](https://img.shields.io/badge/%E7%8C%BF%E6%B0%8F%E6%B5%AA%E6%BC%AB-%E6%83%85%E8%AF%9D-green.svg)]()
[![一个](https://img.shields.io/badge/One-%E4%B8%80%E4%B8%AA-yellow.svg)](http://wufazhuce.com/)


### Acknowledgement
[用 Python + itchat 写一个爬虫脚本每天定时给多个女友发给微信暖心话](https://github.com/sfyc23/EverydayWechat)

####Ubuntun服务器部署
后台启动Python脚本，并把日志写入test.out，会返回一个pid
`nohup python3 -u words_to_mygirl.py > test.out 2>&1 &`
查询正在使用Python相关进程pid值
`ps -ef | grep python3`
杀掉进程
`kill -9 pid`
