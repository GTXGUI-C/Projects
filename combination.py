import json
from selenium import webdriver
import time
from lxml import etree
import pymysql
import datetime

if __name__ == '__main__':
    bro = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    bro.get('https://creator.xiaohongshu.com/creator/notes')
    time.sleep(6)

    # *****************************************************************************
    # 第一次登录时，需要执行以下的操作以完成cookie的获取 [第一次登录时使用该代码，其后将其整段注释掉]
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/input').send_keys('18875093545')

    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/input').click()
    # bro.find_element_by_xpath('//*[@id="beer-portal-container-229"]/div/div/div/div[7]').click()
    # # 输入电话号码
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/input').send_keys('2368893751')
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]').click()
    # verification_code = input()
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/input').send_keys(verification_code)
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/button').click()
    # time.sleep(4)
    #
    # with open(r'D:\Files\cookies.txt', 'w') as f:
    #     # 将cookies保存为json格式
    #     f.write(json.dumps(bro.get_cookies()))
    # *********************************************************************************

    # 每次打开网页时，均会形成新的cookie，因此可以把原始cookie清除掉后，使用新的cookie去恢复登录后的状态。
    bro.delete_all_cookies()
    with open(r'D:\Files\cookies.txt', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)

        # 方法1 将expiry类型变为int
        for cookie in cookies_list:
            # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            bro.add_cookie(cookie)

    bro.refresh()

    #************************************************************************8
    # 获取数据
    time.sleep(5)
    bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/main/div[1]/div/div[2]/div/div[6]').click()
    # 获得所有的note—card-container,我们需要从note-card-container里获取的数据有：
    #  (1) URL
    #  (2) 笔记题目 -- Title
    #  (3) 笔记发布时间 -- PublishedTime
    #  (4) 浏览人数 -- PageView
    #  (5) 点赞数 -- Likes
    #  (6) 收藏数 -- Collects
    #  (7) 评论数 -- Comments
    #  (8) 分享人数 -- Shares
    #  (9) 涨粉数 -- FansIncrease

            # 用于检查获取的结果的准确性
            # print(url)
            # print(PulishedTime)
            # print(Title)
            # print(PageViews)
            # print(FansIncrease)

    # ***********************************************************************
    # 创建新的表格
    connection = pymysql.Connection(host='117.78.18.51', user='root', password='Jyz123456!', database='XIDA',
                                    port=3306)
    with connection.cursor() as cursor:
        sql = """use XIDA;"""
        cursor.execute(sql)
        sql = """create table if not exists xhs_data (
            URL varchar(255),
            Title varchar(255),
            PublishedTime varchar(255),
            PageViews int,
            Likes int,
            Collects int,
            Comments int,
            Shares int,
            FansIncrease int,
            query_time varchar(50)) DEFAULT CHARACTER SET = utf8mb4;"""
        cursor.execute(sql)

    # 翻页，同时插入数据
    while True:
        time.sleep(6)
        page_source = bro.page_source
        tree = etree.HTML(page_source)
        note_card_list = tree.xpath('//div[@class="note-card-container"]')
        for note_card in note_card_list:
            URL = note_card.xpath('./div[@class="info-box"]/a/@href')[0]
            Title = note_card.xpath('./div[1]/div[1]/span[1]/text()')[0]
            PulishedTime = note_card.xpath('./div[1]/div[1]/span[2]/text()')[0].split()[1]
            PageViews = note_card.xpath('./div[2]/ul[1]/li[1]/b/text()')[0]
            Likes = note_card.xpath('./div[2]/ul[1]/li[2]/b/text()')[0]
            Collects = note_card.xpath('./div[2]/ul[1]/li[3]/b/text()')[0]
            Comments = note_card.xpath('./div[2]/ul[1]/li[4]/b/text()')[0]
            Shares = note_card.xpath('./div[2]/ul[2]/li[1]/b/text()')[0]
            FansIncrease = note_card.xpath('./div[2]/ul[2]/li[3]/b/text()')[0]
            QueryTime = datetime.datetime.now().strftime('%Y-%m-%d')
            with connection.cursor() as cursor:
                sql = """insert into xhs_data values (\'{}\',\'{}\',\'{}\',{},{},{},{},{},{},\'{}\');""".format(
                URL,Title,PulishedTime,PageViews,Likes,Collects,Comments,Shares,FansIncrease,QueryTime
                )
                cursor.execute(sql)
                connection.commit()
        if bro.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[4]/div[2]/button[7]').is_enabled():
            bro.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[4]/div[2]/button[7]').click()
        else:
            print('Data Collected.Ready to exit')
            break



