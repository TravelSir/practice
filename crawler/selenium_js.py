from bs4 import BeautifulSoup
from selenium import webdriver

cookies = {}


def init_browser():

    path = "/Users/tsir/study/code/practice/crawler/chromedriver"  # 注意这个路径需要时可执行路径（chmod 777 dir or 755 dir）

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')  # 无界面模式
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument("--proxy-server=http://202.20.16.82:10152")  # 设置ip代理
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # 手动指定使用的浏览器位置

    browser = webdriver.Chrome(options=options, executable_path=path)
    browser.implicitly_wait(10)  # 定位元素时的等待时间
    return browser


def demo(browser):

    browser.get('www.baidu.com')
    print(browser.page_source)
    browser.save_screenshot('baidu.png')  # 截图


def login(browser):
    browser.get('http://sit1-sxs-web.mshare.cn/user/login')
    account = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/input')
    password = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/input')
    account.send_keys('15196801320')
    password.send_keys('123456')
    browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]').click()
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/ul/li[2]/a')
    global cookies
    if not cookies:
        cookies = browser.get_cookies()


def my_deliver(browser):
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        browser.add_cookie(cookie)
    browser.get('http://sit1-sxs-web.mshare.cn/my/delivered')
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]')
    with open('test3.html', 'w+') as f:
        f.write(browser.page_source)
    # bs4 直接解析browser.page_source...


if __name__ == '__main__':
    browser = init_browser()
    login(browser)
    my_deliver(browser)

    browser.close()  # 记得关闭浏览器节省资源
