from selenium import webdriver
import time
import re
from tqdm import tqdm

#全局变量
driver = webdriver.Chrome()


def loginWeibo(username, password):
    driver.get('https://passport.weibo.cn/signin/login')
    time.sleep(3)

    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()
    cookies = driver.get_cookies()
    cookie_list = []
    for dict in cookies:
        cookie = dict['name'] + '=' + dict['value']
        cookie_list.append(cookie)
    cookie = ';'.join(cookie_list)

    #driver.close()


def visitUserInfo(userId):
    driver.get('http://weibo.cn/' + userId)

    print('********************')   
    print('用户资料')
    
    # 1.用户id
    print('用户id:' + userId)
    
    # 2.用户昵称
    strName = driver.find_element_by_xpath("//div[@class='ut']")
    strlist = strName.text.split(' ')
    nickname = strlist[0]
    print('昵称:' + nickname)
    
    # 3.微博数、粉丝数、关注数
    strCnt = driver.find_element_by_xpath("//div[@class='tip2']")
    pattern = r"\d+\.?\d*"      # 匹配数字，包含整数和小数
    cntArr = re.findall(pattern, strCnt.text)
    print(strCnt.text)
    print("微博数：" + str(cntArr[0]))
    print("关注数：" + str(cntArr[1]))
    print("粉丝数：" + str(cntArr[2]))
    
    print('\n********************')
    # 4.将用户信息写到文件里
    with open("userinfo.txt", "w", encoding = "utf-8") as file:
        file.write("用户ID：" + userId + '\r\n')
        file.write("昵称：" + nickname + '\r\n')
        file.write("微博数：" + str(cntArr[0]) + '\r\n')
        file.write("关注数：" + str(cntArr[1]) + '\r\n')
        file.write("粉丝数：" + str(cntArr[2]) + '\r\n')
    print('用户信息爬取完成！')
    print('准备爬取微博内容...')
        
    
def visitWeiboContent(userId):
    pageList = driver.find_element_by_xpath("//div[@class='pa']")
    # print(pageList.text)
    pattern = r"\d+\d*"         # 匹配数字，只包含整数
    pageArr = re.findall(pattern, pageList.text)
    totalPages = pageArr[1]     # 总共有多少页微博
    print('共'+totalPages+'页')
    
    pageNum = 1                 # 第几页
    numInCurPage = 1            # 当前页的第几条微博内容
    curNum = 0                  # 全部微博中的第几条微博
    contentPath = "//div[@class='c']"
    #while(pageNum <= 3):   
    # while(pageNum <= int(totalPages)):
    for pageNum in range(1, int(totalPages)+1):
        print('正在爬取第 %d 页' % pageNum)
        contentUrl = "http://weibo.cn/" + userId + "?page=" + str(pageNum)
        try:
            driver.get(contentUrl)
            content = driver.find_elements_by_xpath(contentPath.format(numInCurPage))
            for i in tqdm(content[:-1]):
                if "设置:皮肤.图片.条数.隐私" not in i.text:
                    numInCurPage += 1
                    curNum += 1
                    with open("weibocontent.txt", "a", encoding = "utf-8") as file:
                        file.write(str(curNum) + '\r\n' + i.text + '\r\n\r\n')
                else:
                    continue

            pageNum += 1                        # 抓取新一页的内容
            numInCurPage = 1  
            print('\n请等待20s 准备爬取第%d页...' % pageNum)
            for j in tqdm(range(20)):
                time.sleep(1)
                
        except:
            print('抓取失败！')
    print("Load weibo content finished!")          
    
        
if __name__ == '__main__':
    username = '手机号或者邮箱'             # 输入微博账号
    password = 'password'             # 输入密码
    loginWeibo(username, password)      # 要先登录，否则抓取不了微博内容
    
    time.sleep(3)
    uid = '6584156654'
    visitUserInfo(uid)                  # 获取用户基本信息
    visitWeiboContent(uid)              # 获取微博内容

