import json
from selenium import webdriver
import time

if __name__ == '__main__':
    bro = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    bro.get('https://creator.xiaohongshu.com/creator/notes')
    time.sleep(6)

    # *****************************************************************************
    # 第一次登录时，需要执行以下的操作以完成cookie的获取
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/input').send_keys('15622767793')
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]').click()
    # verification_code = input()
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/input').send_keys(verification_code)
    # bro.find_element_by_xpath('//*[@id="CreatorPlatform"]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/button').click()
    # time.sleep(4)
    #
    # #bro.delete_all_cookies()
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



