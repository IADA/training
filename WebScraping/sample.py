# coding: UTF-8
# 参考:
# Python Webスクレイピング 実践入門 https://qiita.com/Azunyan1111/items/9b3d16428d2bcc7c9406
# python のModule urllib2 を利用する方法を教えて下さい https://teratail.com/questions/47744
import urllib.request, urllib.error
from bs4 import BeautifulSoup

# アクセスするURL
url = "http://www.nikkei.com/"

# URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
html = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

# タイトル要素を取得する → <title>経済、株価、ビジネス、政治のニュース:日経電子版</title>
title_tag = soup.title

# 要素の文字列を取得する → 経済、株価、ビジネス、政治のニュース:日経電子版
title = title_tag.string

# タイトル要素を出力
print(title_tag)

# タイトルを文字列を出力
print(title)