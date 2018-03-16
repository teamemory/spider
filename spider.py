#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import lxml
import requests
import xlsxwriter


class Spider():
    # 初始化参数
    def __init__(self, urlList):
        self.urlList = urlList
        self.num = 0
        self.row = 0
        self.col = 0
        self.wookbook = ''
        self.wooksheet = ''

    # 下载
    def downLoad(self, add_url):
        res = requests.get(add_url)
        html = res.content
        if self.num == 0:
            self.analy(html)
        else:
            self.second_analy(html)

    # 一级页面解析html
    def analy(self, html):
        self.num += 1
        soup = BeautifulSoup(html, 'lxml')
        alist = soup.select('#daquan_list li a')
        for a in alist:
            new_html = a['href']
            self.downLoad(new_html)
        

    # 二级页面的解析
    def second_analy(self, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            title = soup.select('.news_neirong p strong')[1].string
            detail = soup.select('.news_neirong p')[5].string
            self.save_data(title, detail)

        except:
            print('没有信息')

    # 保存数据
    def save_data(self, title, detail):
        self.row += 1
        self.wooksheet.write(self.row, self.col, title)
        self.wooksheet.write(self.row, self.col+1, detail)

    # 主调度函数
    def main(self):
        self.wookbook = xlsxwriter.Workbook('/home/code/cy.xlsx')
        self.wooksheet = self.wookbook.add_worksheet()
        self.wooksheet.write(self.row, self.col, '标题')
        self.wooksheet.write(self.row, self.col+1, '内容')
        for url in self.urlList:
            self.num = 0
            self.downLoad(url)
        self.wookbook.close()


# 入口函数
if __name__ == "__main__":
    urlList = ["http://ktccy.gamedog.cn/gonglue/shibo.html","http://ktccy.gamedog.cn/gonglue/jiubo.html","http://ktccy.gamedog.cn/gonglue/babo.html","http://ktccy.gamedog.cn/gonglue/qibo.html","http://ktccy.gamedog.cn/gonglue/liubo.html","http://ktccy.gamedog.cn/gonglue/wubo.html","http://ktccy.gamedog.cn/gonglue/yibo.html","http://ktccy.gamedog.cn/gonglue/one.html","http://ktccy.gamedog.cn/gonglue/sanbo.html","http://ktccy.gamedog.cn/gonglue/sibo.html"]
    craw = Spider(urlList)
    craw.main()
