# 这个文件主要是用于爬取目标用户小红书网页首页上出现的博客的相关信息，包括：博客id，博客标题，点赞，收藏，评论，发送时间等数据。

from selenium import webdriver
import time
import pymysql
from lxml import etree
import datetime

if __name__ == '__main__':
    # connect our target website with selenium
    bro = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    bro.get('https://www.xiaohongshu.com/user/profile/5d40aff00000000012015fb0?xhsshare=CopyLink&appuid=5b700a8ef6730000014f157c&apptime=1625576539')
    time.sleep(3)

    # get the source code of the fully loaded page
    page_source=bro.page_source

    # we can find that data are loaded by the java script, so we can execute the JS code to get the data. script is a json object.
    script = bro.execute_script('return window.__INITIAL_SSR_STATE__')
    #print(script['Main']['notesDetail'][0])

    tree = etree.HTML(page_source)
    div_list = tree.xpath('//div[@class="note-info"]')
    url_list=[]
    for i in div_list:
        url_list.append('https://www.xiaohongshu.com'+str(i.xpath('./a/@href')[0]))
    print(url_list)

    # put the data into the database
    connection = pymysql.Connection(host='117.78.18.51', user='root', password='Jyz123456!', database='XIDA', port=3306)
    with connection.cursor() as cursor:
        sql="""use XIDA;"""
        cursor.execute(sql)
        sql="""create table if not exists xhs_note_record (
        id varchar(255),
        title varchar(255),
        url varchar(255),
        collects int,
        comments int,
        likes int,
        published_time varchar(50),
        query_time varchar(50))DEFAULT CHARACTER SET=utf8;"""
        cursor.execute(sql)

    for i in range(len(url_list)):
        temp_dic = script['Main']['notesDetail'][i]
        id = temp_dic['id']
        title = temp_dic['title']
        url = url_list[i]
        collects = temp_dic['collects']
        comments = temp_dic['comments']
        likes = temp_dic['likes']
        published_time = temp_dic['time']
        query_time = datetime.datetime.now().strftime('%Y-%m-%d')
        with connection.cursor() as cursor:
            sql = """insert into xhs_note_record values (
            \'{}\',\'{}\',\'{}\',{},{},{},\'{}\',\'{}\'
            );""".format(str(id),str(title),str(url),collects,comments,likes,str(published_time),str(query_time))
            cursor.execute(sql)
            connection.commit()
    connection.close()
