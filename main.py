# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# import time
# import pymysql
# import requests
# import re
# import urllib3
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# import json
#
#
# class Fuck_xhs(object):
#     def __init__(self):
#         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#         self.conn = pymysql.connect(host='117.78.18.51', user='root', password='Jyz123456!', database='XIDA', port=3306)
#         self.cursor = self.conn.cursor()
#         self.url = 'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?'
#         self.key_dict = {
#             '1': 'Xd44b23783ad8f18c2e41c045a0cda867',
#             '2': 'Xe8b3f71b7585c080e9ca55e7d1b034e0',
#             '3': 'X2351ff0514bb05145e8171975fe1d96d',
#             '4': 'X2422fd5312cf50b12c722e1d63b2f9aa',
#             '5': 'X44d5cf63fb658c609be10404b77291d5',
#         }
#         # with open('D:/entertainment/Projects/url.txt', 'r', encoding='utf-8')as f:
#         #     r = f.read().replace('\ufeff', '')
#         #     self.old_list = r.split('\n')
#         #     print(self.old_list)
#         options = Options()
#         options.add_argument('--headless')
#         self.chrome = Chrome(options=options)
#
#     def get_detail_url(self):
#         for key, value in self.key_dict.items():
#             headers = {
#                 'Host': 'www.xiaohongshu.com',
#                 'Connection': 'keep-alive',
#                 'Authorization': 'wxmp.4aad8f54-3422-4d76-b440-5f4cce8d0907',
#                 'Device-Fingerprint': 'WHJMrwNw1k/Ff2NfArpikjizTJkAdQe2Y1P0AQTa74gJcSlBSWoMjTXYq+VUDRGsE9VCMBXrfD5W9YT2GqNMbnISuxoWerClbdCW1tldyDzmauSxIJm5Txg==1487582755342',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
#                 'X-Sign': value,
#                 'content-type': 'application/json',
#                 'Referer': 'https://servicewechat.com/wxffc08ac7df482a27/378/page-frame.html',
#                 'Accept-Encoding': 'gzip, deflate, br',
#             }
#             params = {
#                 'keyword': '揭阳周边游',
#                 'sortBy': 'general',
#                 'page': key,
#                 'pageSize': '20',
#                 'needGifCover': 'true',
#             }
#             res = requests.get(self.url, headers=headers, params=params, verify=False).text
#             print(res)
#             res_dict = json.loads(res)
#             notes = res_dict['data']['notes']
#             for note in notes:
#                 id = note['id']
#                 print(id)
#                 self.detail_url = 'https://www.xiaohongshu.com/discovery/item/' + id
#                 print(self.detail_url)
#                 # if self.detail_url in self.old_list:
#                 #     print('链接已存在。')
#                 #     continue
#                 # else:
#                 #     with open(r'D:\entertainment\Projects\小红书url.txt', 'a', encoding='utf-8') as w:
#                 #         w.write('\n')
#                 #         w.write(self.detail_url)
#                 #     self.get_detail()
#                 #     continue
#         self.conn.close()
#
#     def get_detail(self):
#         self.chrome.get(self.detail_url)
#         time.sleep(1.5)
#         try:
#             video = self.chrome.find_element_by_xpath('//div[@class="videoframe"]')
#             if video:
#                 return None
#         except:
#             pass
#         self.content_pic = '<ul>' + str(
#             self.chrome.find_element_by_class_name("slide").get_attribute('innerHTML')) + '</ul>'
#         print(self.content_pic)
#         urls = re.findall(r'style="background-image.*?;"', self.content_pic, re.DOTALL)
#         for ur in urls:
#             print('ur的值为%s' % ur)
#             u = ''.join(re.findall(r'url\((.*?)\)', ur))
#             url = 'http:' + u.replace('&quot;', '').replace('&quot', '').replace('https:', '').replace('http:',
#                                                                                                        '') + '.jpg'
#             print(url)
#             self.content_pic = str(self.content_pic).replace(ur, 'src=' + '"' + url + '"').replace('span',
#                                                                                                    'img').replace(
#                 '<i data',
#                 '<img data').replace(
#                 '</i>', '</img>')
#         print(self.content_pic)
#         self.content = self.chrome.find_element_by_class_name('content').get_attribute('innerHTML')
#         try:
#             self.author = self.chrome.find_element_by_class_name('name-detail').text
#             print(self.author)
#         except:
#             self.author = ' '
#         try:
#             self.title = self.chrome.find_element_by_class_name('title').text
#             if not self.title:
#                 self.title = self.chrome.find_element_by_class_name('as-p').text
#             print(self.title)
#         except:
#             self.title = ' '
#         try:
#             span = self.chrome.find_elements_by_xpath('//div[@class="operation-block"]/span')
#             self.like = span[0].find_element_by_xpath('./span').text
#             self.comment = span[1].find_element_by_xpath('./span').text
#             self.star = span[2].find_element_by_xpath('./span').text
#             print(self.like, self.comment, self.star)
#         except:
#             self.like = ' '
#             self.comment = ' '
#             self.star = ' '
#         try:
#             self.b_q = self.chrome.find_elements_by_xpath('//div[@class="keywords"]/a[@class="keyword category"]')
#             print(self.b_q)
#             a_l = []
#             for bq in self.b_q:
#                 a = bq.text
#                 a_l.append(a)
#             self.a_l = str(a_l).replace('[', '').replace(']', '').replace("'", '').replace(',', '，')
#             print(self.a_l)
#         except:
#             self.a_l = ' '
#         try:
#             self.pub_time = str(self.chrome.find_element_by_xpath('//div[@class="publish-date"]/span').text).replace(
#                 '发布于', '')
#             print(self.pub_time)
#         except:
#             self.pub_time = ' '
#         try:
#             self.author_img = self.chrome.find_element_by_xpath('//div[@class="left-img"]/img').get_attribute('src')
#             print(self.author_img)
#         except:
#             self.author_img = ' '
#         time.sleep(5)
#         self.create_time = time.strftime("%Y-%m-%d %H:%M:%S")
#         print(self.create_time)
#         self.is_import = '0'
#         time.sleep(3)
#         self.deposit_mysql()
#
#     def deposit_mysql(self):
#         sql = "insert into xhs_article(id, author, author_img, title, text_img, content, like_count, review_count, " \
#               "collect_count, org_url, publish_time, keyword_tag, create_time, is_import, import_time) values(null," \
#               "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,null) "
#         self.cursor.execute(sql, (
#             str(self.author), str(self.author_img), str(self.title), str(self.content_pic), str(self.content),
#             str(self.like), str(self.comment),
#             str(self.star), str(self.detail_url), str(self.pub_time), str(self.a_l), str(self.create_time),
#             str(self.is_import)))
#         self.conn.commit()
#         return None
#
#
# if __name__ == '__main__':
#     xhs = Fuck_xhs()
#     xhs.get_detail_url()
# # Press the green button in the gutter to run the script.
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
