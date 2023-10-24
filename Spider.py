# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3

findLink = re.compile(r'<a href="(.*?)">')  # 电影链接
findImg = re.compile(r'<img.*src="(.*?)".*>', re.S)  # 图片链接 re.s 让换行符包含在字符中
findTittle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findNum = re.compile(r'<span>(\d*)人评价</span>')
findComment = re.compile(r'<span class="inq">(.*?)</span>')
findInfo = re.compile(r'<p class="">(.*?)</p>', re.S)


def get_data(baseurl):
    datalist = []
    for i in range(0, 1):  # 每一页是25个，总共250个索引是10页，调试为1页
        url = baseurl + str(i * 25)
        html = ask_url(url)

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="item"):
        data = []
        item = str(item)
        link = re.findall(findLink, item)[0]
        data.append(link)
        img = re.findall(findImg, item)[0]  # 添加图片
        data.append(img)
        title = re.findall(findTittle, item)
        if len(title) == 2:
            cn_name = title[0]
            data.append(cn_name)
            us_name = title[1]
            us_name = re.sub(r"\xa0|/", '',str(us_name))

            data.append(us_name)
        else:
            cn_name = title[0]
            data.append(cn_name)
            us_name = " "
            data.append(us_name)
        rate = re.findall(findRating, item)[0]
        data.append(rate)
        num = re.findall(findNum, item)[0]
        data.append(num)
        comment = re.findall(findComment, item)
        if len(comment) != 0 :
            comment = comment[0].replace("。",'')
            data.append(comment)
        else:
            data.append(' ')
        info = re.findall(findInfo, item)[0]
        info = re.sub(r'<br(\s+)?/>(\s+)?',' ',str(info))
        info = re.sub('/',' ',str(info))
        info = re.sub(r"\xa0",' ',str(info))
        data.append(info.strip())
        datalist.append(data)

    for item in datalist:
        print(item)
    return datalist


def ask_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
     
    get_data("https://movie.douban.com/top250?start=")
