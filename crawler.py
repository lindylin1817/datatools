import requests
from bs4 import BeautifulSoup
import os

def crawl_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 设置编码
    soup = BeautifulSoup(response.text, 'html.parser')

    # 打印网页标题
    print(soup.title.string)

    # 找到所有的链接
    links = soup.find_all('a')

    # 创建一个目录来存储所有的网页内容
    if not os.path.exists('webpages'):
        os.makedirs('webpages')

    # 遍历每个链接并保存内容
    for i, link in enumerate(links):
        href = link.get('href')
        href = url + href
        print(href)
        if href and href.startswith('http'):
            try:
                page_response = requests.get(href)
                page_response.encoding = 'utf-8'  # 设置编码
                page_soup = BeautifulSoup(page_response.text, 'html.parser')

                # 将内容写入文件
                with open(f'webpages/page_{i}.txt', 'w', encoding='utf-8') as f:
                    f.write(page_soup.text)
            except Exception as e:
                print(f"Error while trying to access {href}: {e}")

# 爬取网站
crawl_website('http://www.gaozhanzx.com/')
