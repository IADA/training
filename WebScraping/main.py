# coding: UTF-8
# 参考:
# PythonとBeautiful Soupでスクレイピング https://qiita.com/itkr/items/513318a9b5b92bd56185
from bs4 import BeautifulSoup
import re, csv

with open("output.csv", "wt", newline = "", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["link", "title", "company", "tags", "description"])

    with open("test.html", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        for case in soup.find_all("div", class_="clm1 mb16 appended-element"):
            case_a_tag = case.div.div.div.find("a", href=re.compile("case"))
            link = "=HYPERLINK(\"" + case_a_tag.get("href") + "\", \"link\")"
            title = case_a_tag.string
            company = case.div.div.div.find_all("p", class_="ttl mb8")[1].string
            description = case.div.div.div.find("p", class_="txt mb8").string
            tags = ""
            for tag in case.div.div.div.ul.find_all("a"):
                tags += "[" + tag.string + "] "

            row = [link, title, company, tags, description]
            writer.writerow(row)