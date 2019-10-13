import requests
import csv
from lxml import etree
import pymysql

class ConnMyql(object):
    def __init__(self):
        #连接数据库
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  passwd='123456',
                                  port=3306,
                                  db='business'
                                  )
        self.cursor = self.db.cursor()
    def insert(self,dict1):
        # 将数据添加到数据库中的movie1表中
        sql = "insert into movie1(m_name,typle,box,price,people_time,country,m_time,detail_href) values ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" 

        data= [dict1['m_name'],dict1['typle'],dict1['box'],dict1['price'],dict1['people_time'],dict1['country'],dict1['m_time'],dict1['detail_href']]
        
        self.cursor.execute(sql,data)

        self.db.commit()# 提交操作




class pachong(object):
    def __init__(self):
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
    }

    def work(self,url):
        response = requests.get(url = url,headers=self.headers)
        html_doc = etree.HTML(response.text)

        list1=['m_name','typle','box','price','people_time','country','m_time','detail_href']
        for j in range(2,27):
            dict_data = {}
            for num in range(0,8):
                try:
                    if num ==7:#详情页网址
                        value = html_doc.xpath('//tr[%d]/td[1]/a/@href' %j)[0]
                    elif  num == 0: #电影名称
                        value = html_doc.xpath('//tr[%d]/td[1]/a/p/text()'%j)[0]
                    else:
                        value = html_doc.xpath('//tr[%d]/td[%d]/text()'%(j,num+1))[0]
                except:
                    value = None
                dict_data[list1[num]]= value  # 将数据存入字典
            save_data(dict_data)  # 执行保存函数用于选择存储方式
            print(j)

def save_data(dict_data):
    #存数据库
    database = ConnMyql()
    database.insert(dict_data)

if __name__ =='__main__':
    test = pachong()
    base_url = 'http://www.cbooo.cn/year?year='
    for i in range(2008,2019): # 这里因为爬取的好几页的内容，而每页的网址通过base_url与数字拼接
        url = base_url + str(i)

        test.work(url)
