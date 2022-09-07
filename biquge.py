import re

import parsel
import requests

import color


def download(num):
    url = f'https://www.bbiquge.net/book_{num}/'
    response = requests.get(url)
    selector = parsel.Selector(response.text)
    novel_name = selector.css('#info h1::text').get()  # 小说名字
    href = selector.css('.zjlist dd a::attr(href)').getall()  # 小说章节链接
    for link in href:
        chapter_url = url + link
        response_chapter = requests.get(chapter_url)
        novel_content_url = parsel.Selector(response_chapter.text)
        chapter_name = novel_content_url.css('#main h1::text').get()  # 章节名
        novel_content = novel_content_url.css('#content::text').getall()  # 小说内容
        content = '\n'.join(novel_content)  # 将获取的小说内容，不停的换行加入
        with open(f'{novel_name}.txt', mode='a', encoding='utf-8') as file:
            file.write(chapter_name)
            file.write('\n')
            file.write(content)
            file.write('\n')
        print(chapter_name + '  \t ---------Download OK')  # 下载完该章节后自动打印章节名
        print('按Ctrl+C终止下载')
    return print('\n \t 任务完成')


def get_hot_list():  # sourcery skip: avoid-builtin-shadow
    index = requests.get('https://www.bbiquge.net/')
    hot_list = parsel.Selector(index.text)
    hot_novel = hot_list.css(
        '#mainright .titletop h3::text').getall()  # 收藏榜，全本榜，下载榜
    hot_novel_autho_list = hot_list.css(
        '#mainright .titletop ul li .txt-right-gray::text').getall()  # 榜单中的作者列表
    hot_novel_list = hot_list.css(
        '#mainright .titletop ul li .s1::text').getall()  # 榜单中的类别列表
    hot_novel_name = hot_list.css(
        '#mainright .titletop ul li a::text').getall()  # 书名列表
    hot_novel_link = hot_list.css(
        '#mainright .titletop ul li a::attr(href)').getall()  # 书本链接列表
    for i in range(len(hot_novel_list)):
        id_num = re.findall('book\/(.*?)\/', hot_novel_link[i])
        list = '\t id: '+id_num[0] + '-----《' + \
            hot_novel_name[i] + '》-----' + hot_novel_autho_list[i]
        print(list)
    print('==================================================')
    print('''打开笔趣阁网站，找到您要下载的书本查看地址栏的编号也可以

         eg:https://www.bbiquge.net/book/133312/---《宇宙职业选手》

             那么133312就是他的id
             更多书籍打开  https://www.bbiquge.net/  搜索便可
    ''')
    return 0


def setST():
    color.os.system('title 笔趣阁txt下载 By 依旧归七')
    color.printBlueWhite()
    return 0


if __name__ == '__main__':
    setST()
    get_hot_list()
    n = input('\t请输入你要下载的书本id:\n\t按0回车退出')
    if n =='0':
        print("       :) 感谢使用！")
        exit()
    else:
        download(str(n))
