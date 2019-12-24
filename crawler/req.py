# coding=utf-8

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3'}


# 实习僧主页
def get_sxs_index():
    url = 'https://www.shixiseng.com/'
    response = requests.get(url)
    with open('test.html', 'w+') as f:
        f.write(response.text)


# 登陆实习僧
def login_sxs():
    login_url = 'https://www.shixiseng.com/user/login'
    req = requests.Session()
    param = {
        'username': '18728263016',
        'password': '45X35X25X15X05X94',
        'remember_login': '1'
    }

    resp = req.post(login_url, headers=headers, data=param)
    # resp = req.post(login_url, headers=headers, data=param, proxies={'http': '0.0.0.0:8888'})  # ip代理
    print(resp.text)
    return req.cookies


def login_sxs_sit1():
    login_url = 'http://sit1-sxs-web.mshare.cn/user/login'
    req = requests.Session()
    param = {
        'username': '15196801320',
        'password': '45X35X25X15X05X94',
        'remember_login': '1'
    }

    resp = req.post(login_url, headers=headers, data=param)
    print(resp.text)
    return req.cookies


# 我的投递
def get_delivers():
    c = login_sxs_sit1()
    url2 = 'http://sit1-sxs-web.mshare.cn/my/delivered'
    response2 = requests.get(url2, headers=headers, cookies=c)
    # response2 = requests.get(url2, headers=headers)
    with open('test2.html', 'w+') as f:
        f.write(response2.text)


# 首页职位
def get_index_interns():
    url = 'https://www.shixiseng.com/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features='lxml')
    # print(soup.prettify())
    interns = soup.find_all('div', {"class": "intern-content-href"})
    for intern in interns:
        # print(intern)

        tags = intern.find_all('div', {"class": "job-tags-text"})
        tags = [tag.text for tag in tags if tag.text != '···']
        img = intern.find('img').attrs.get('src')

        a_tags = intern.find_all('a')
        name = a_tags[0].text
        company = a_tags[2].text

        spans = intern.find_all('span')
        salary = spans[0].text
        city = spans[1].text
        work_day = spans[2].text
        month = spans[3].text
        industry = spans[4].text
        scale = spans[5].text.replace('丨', '')
        print(name, salary, tags, city, work_day, month, img, company, industry, scale)


if __name__ == '__main__':
    # get_sxs_index()
    # get_index_interns()
    get_delivers()
    # intern_search()
