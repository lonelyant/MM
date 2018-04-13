from urllib import request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


class DownloadMM():
    def __init__(self, num=1, totalnum=0):
        self.totalnum = totalnum
        self.num = num
        self.desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        self.desired_capabilities[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'],
                                          executable_path='C:/Users/Administrator/Downloads/phantomjs_xpgod/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        self.driver.start_session(self.desired_capabilities)

    def url_open_simply(self, url):
        req = request.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')
        response = request.urlopen(req)
        html = response.read()
        print('开始返回未解析页面...')
        return html

    def url_open(self, url):
        # 隐式等待3秒，可以自己调节
        self.driver.implicitly_wait(3)
        print('3秒等待完成...')
        # 设置20秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self.driver.set_page_load_timeout(20)
        # 设置20秒脚本超时时间
        self.driver.set_script_timeout(20)

        try:
            self.driver.get(url)
            print('超时检测正常...')
        except BaseException as e:
            print('超时！！！')
            raise BaseException
        print('开始返回解析后页面...')
        return self.driver.page_source

    def get_max_page(self, url):
        '''
        根据URL获取页面并分离出HTML中的最大页信息
        <span class="current-comment-page">[103]</span>
        :param url:煎蛋网XXOO页地址
        :return:最大页数
        '''
        html = self.url_open_simply(url).decode('utf-8')

        a = html.find('current-comment-page') + 23
        b = html.find(']', a)
        print('获取最大页面数成功...')
        return html[a:b]

    def find_imgs(self, page_url):
        '''
        从给page_url页面中找到所需图片地址
        :param page_url: 煎蛋网妹子页面带页数
        :return: 页面中图片地址
        '''
        html = self.url_open(page_url)
        img_addrs_list = []
        a = html.find('img src=')
        while a != -1:
            b = html.find('.jpg', a, a + 255)
            if b != -1:
                img_addrs_list.append(html[a + 9:b + 4])
            else:
                b = a + 9
            a = html.find('img src=', b)
        print('获取图片地址列表成功...')
        return img_addrs_list

    def save_imgs(self, img_addrs_list, folder):
        '''
        根据图片地址保存图片到本地
        :param img_addrs_list: 图片地址列表
        :param folder: 本地文件夹名称
        :return:
        '''
        for each in img_addrs_list:
            filename = each.split('/')[-1]
            with open(filename, 'wb') as f:
                img = self.url_open_simply(each)
                print(each)
                f.write(img)
                self.totalnum += 1
        print('保存图片成功...')

    def downloadMM(self, folder='学习资料', pages=0):
        pages = self.num
        # 创建存储图片的文件夹，并切换到文件夹
        os.mkdir(folder)
        os.chdir(folder)

        url = "http://jandan.net/ooxx"
        page_num = int(self.get_max_page(url))
        i = 0
        while i < pages:
            current_page = page_num - i
            page_url = url + '/page-' + str(current_page) + '#comments'
            print(page_url)
            try:
                img_addrs_list = self.find_imgs(page_url)
            except BaseException as e:
                print('准备重新开始此次爬取...')
                current_page = page_num + i
                continue
            self.save_imgs(img_addrs_list, folder)
            i += 1

        print('\n*********** 本次爬取任务结束,总共爬取了 %s 张图片 ***********' % self.totalnum)


if __name__ == '__main__':
    DownloadMM(3).downloadMM()
