import scrapy
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import json


class BsSpider(scrapy.Spider):
    name = "vbs2"

    my_sender = 'dnf736@vip.qq.com'  # 发件人邮箱账号
    my_pass = 'rclmyfkneolnbbid'  # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = '576305942@qq.com'  # 收件人邮箱账号，我这边发送给自己

    def start_requests(self):
        yield scrapy.Request(
            "http://cse.csu.edu.cn/system/resource/code/news/click/clicktimes.jsp?wbnewsid=3074453&owner=1520089960&type=wbnewsfile&randomid=nattach",
            callback=self.parse)

    def parse(self, response):
        link = json.loads(response.body.decode('utf-8'))['wbshowtimes']
        print(link)
        link = str(link)
        fo = open("download.txt", "r+", encoding="utf-8")
        line = fo.readline()
        # 没有内容先写入内容
        if line is None:
            fo.close()
            fo = open("download.txt", "w+", encoding="utf-8")
            line = fo.write(link)
            fo.close()
        # 判断内容是否变化
        if line is not None:
            # 没变化
            if line == (link):
                fo.close()
            # 下载次数大于原有的次数
            if line <= (link):
                fo.close()
                fo = open("download.txt", "w+", encoding="utf-8")
                line = fo.write(link)
                fo.close()
            # 下载次数小于原有的次数
            if line >= (link):
                fo.close()
                fo = open("download.txt", "w+", encoding="utf-8")
                line = fo.write(link)
                fo.close()
                self.mail()

    def mail(self):
        ret = True
        try:
            msg = MIMEText('http://cse.csu.edu.cn/info/1075/5978.htm',
                           'plain', 'utf-8')
            msg['From'] = formataddr(["豆饼大哥",
                                      self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["毛雷小老弟",
                                    self.my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "新的通知"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com",
                                      465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(self.my_sender, self.my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.my_sender, [
                self.my_user,
            ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret