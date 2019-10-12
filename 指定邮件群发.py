# coding: utf-8
#!/usr/bin/python
import zmail
import time
# 群发邮件 
import os,sys
import datetime
import traceback
import poplib
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
import email
def wo_mail(xinxi):
    #如何登陆邮件
    #按目的分为为发送邮件而登陆 还是为了读取邮件而登录
    #发送邮件登录 一般来说登录使用 SMTP,接收邮箱用POP
    _user = "xxxxxx.com"
    _pwd  = "xxxxxx"  #qq邮箱为授权码(16位)
    sent =smtplib.SMTP_SSL('smtp.163.com',465)#设置了SMTP服务器为stmp.qq.com 其端口号为465
    sent.login(_user, _pwd)#登陆

    #发送邮件
    #刚才已经登录，现在需要设置发送内容，然后发送即可

    current_time = datetime.datetime.now().weekday ()+1  #周一是0，周五是4
    if current_time <= 5:   #设置如果是周五前面的星期

        try:
            to=['xxxxxxxxxxx'] # 这里设置了邮件要发送的地址，可以群发
            content=MIMEText(xinxi)#MIMEText表示邮件发送具体内容
            content['Subject']='xxxxxxxxxxx'#设置邮箱标题
            content['From']='xxxxxxxxxxx'#设置邮箱有哪里发送
            content['To']=','.join(to)
            sent.sendmail(_user,to,content.as_string())#三个参数
            sent.close()#关闭邮箱
            print ("邮件发送成功")
        except smtplib.SMTPException as e:
            print ("Error: 无法发送邮件")
            print (e)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~收取邮件转发模块
mail_user = "xxxxxxxxxxx.com"
mail_pwd = "xxxxxxxxxxxx" #邮箱授权密码
mail_host = "pop.qq.com" # 邮件服务器填写

server = zmail.server(mail_user, mail_pwd, pop_host = mail_host)
mail = server.get_latest()
id = mail["id"] - 1
print('正在运行')

while datetime.datetime.now() <= datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:30', '%Y-%m-%d%H:%M') :
    try:
        mail = server.get_latest()
        maxid = mail["id"]
        while id < maxid:
            id += 1
            mail = server.get_mail(id)
 # 主体加正文

            content = "".join(mail["content_text"]) if mail["content_text"] != [] else "".join(mail["content_html"])
            message = f"""\n主题：\n{mail['subject']}\n正文：\n{content}"""
            #send_ip = mail["raw"][17].decode("utf-8").split(":")[1].replace(" ", "")
            #print(message)
            if 'xxxxxxx' in mail['subject']: # 邮件标题
                wo_mail("".join(mail["content_text"]))
                            
    # 如果邮箱有邮件被删除
        if id > maxid:
            id = maxid
    # 如果超时，则重新登陆
    except Exception as e:
        server = zmail.server(mail_user, mail_pwd, pop_host =  mail_host)
        print (e)
     #显示当前时间
    sys.stdout.write('\r' + str(time.strftime('%I.%M.%S',time.localtime(time.time()))))
    sys.stdout.flush()
     # 每30秒检查一次
    time.sleep(30)
print('程序结束运行')
