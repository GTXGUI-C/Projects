# 这个文件主要是用于爬取目标用户小红书账号的整体信息。

import requests
import json
import pymysql
import datetime

if __name__ == '__main__':
    # connect to the database
    database = pymysql.Connection(host='117.78.18.51', user='root', password='Jyz123456!', database='XIDA', port=3306)

    # create table
    with database.cursor() as cursor:
        sql = "use XIDA;"
        cursor.execute(sql)
        sql = "create table if not exists xhs (likes_Count int, collects_Count int, notes_Count int, fans_Count int, time varchar(20));"
        cursor.execute(sql)

    # get the data
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/91.0.4472.124 Safari/537.36'}
    res = requests.get(url = 'https://xhs.bihukankan.com/xhs/api/blogger?pageNum=1&pageSize=10&searchPattern=Sloane')
    data = json.loads(res.text)
    print('爬到的数据为:')
    print(data)

    # insert data into database
    with database.cursor() as cursor:
        sql = "insert into xhs values({},{},{},{},\'{}\');".format(data['data'][0]['likesCount'],
                                                                   data['data'][0]['collectsCount'],
                                                                   data['data'][0]['notesCount'],
                                                                   data['data'][0]['fansCount'],
                                                                   datetime.datetime.now().strftime("%Y-%m-%d"))
        cursor.execute(sql)
        database.commit()
    database.close()
