#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   notify.py
@Time    :   2021/10/17 16:28:34
@Author  :   Tang Chuan 
@Contact :   tangchuan20@mails.jlu.edu.cn
@Desc    :   定时发送信息到邮箱
'''
import datetime
import json
import os
import poplib
# -*- coding=utf-8 -*-
import smtplib
import time
from email import parser
from email.header import Header
from email.mime.text import MIMEText

import schedule

content_file = 'arxiv-filtered'

def sendEmail(msg_from, msg_to, auth_id, title, content):
    """发送邮件：目前只支持qq邮箱自动发送邮件

    Args:
        msg_from ([type]): [description]
        msg_to ([type]): [description]
        auth_id ([type]): [description]
        title ([type]): [description]
        content ([type]): [description]
    """
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, auth_id)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except s.SMTPException:
        print("发送失败")
    finally:
        s.quit()


def collect_data():
    os.system('zsh arxiv-rss.sh')

def send_arxiv_data():
    # 读取信息                       
    filename = './info.json'
    with open(filename, 'r') as f:
        dic = json.load(f)
    msg_from = dic['msg_from'] #发送方邮箱
    passwd = dic['passwd']  #填入发送方邮箱的授权码
    msg_to = dic['msg_to']  #收件人邮箱

    subject = "Arxiv-{}".format(datetime.date.today()) # 主题     
    with open(content_file,'r') as f:
        content = f.read()
    sendEmail(msg_from, msg_to, passwd, subject, content)

def main():
    schedule.every().day.at("10:00").do(send_arxiv_data) # 每天在 10:30 时间点运行 job 函数
    schedule.every().day.at("10:30").do(send_arxiv_data) # 每天在 10:30 时间点运行 job 函数
    while True:
        schedule.run_pending() # 运行所有可以运行的任务
        time.sleep(1)


if __name__ == "__main__":
    main()




