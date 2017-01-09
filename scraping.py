# -*- coding: utf8 -*-
from __future__ import unicode_literals
import requests
import re
import os
import os.path
import json
from prettyprint import pp
from bs4 import BeautifulSoup

def detect_yearlypages():
    response = requests.get("http://www.onmyo-za.net/biography/")
    html = response.text.encode(response.encoding)
    soup = BeautifulSoup(html, "lxml")
    ul_ = soup.find("ul", attrs={"class": "sub_menu"})
    lis_ = []
    for li_ in ul_.find_all("li"):
        pattern = r"(\d{4}|index)"
        matchOB = re.search(pattern, li_.find("a").get("href"))
        if matchOB:
            lis_.append(matchOB.group())
    pp(lis_)
    return lis_

def detect_detailpages(url):
    print url
    response = requests.get(url)
    html = response.text.encode(response.encoding)
    soup = BeautifulSoup(html, "lxml")
    links = []
    for link in soup.find_all("a", attrs={"title": "演奏曲目"}):
        pattern = r"\d{8}.html"
        matchOB = re.search(pattern, link.get("onclick"))
        if matchOB:
            links.append(matchOB.group())
    pp(links)
    return links

def scraping(url):
    # get a HTML response
    response = requests.get(url)
    html = response.text.encode(response.encoding) # prevent encoding errors
    # parse the response
    soup = BeautifulSoup(html, "lxml")
    # extract
    header_ = soup.find(attrs={"class": "header"})
    tour = header_.find("h1").text
    tmp = re.findall("(\d+)", header_.find("p").text.split("/")[0].strip())
    date = tmp[0] + "-" + tmp[1] + "-" + tmp[2]
    place = header_.find("p").text.split("/")[1].strip()
    uls_ = soup.find_all("ul", attrs={"class": "right"})
    
    records = []
    for ul_ in uls_:
        for song in ul_.find_all("li"):
            if song.string is not None:
                song = song.text
                # output
                record = {
                    "tour": tour, 
                    "place": place, 
                    "date": date,
                    "song": song
                    }
                pp(record)
                # put_datastore(record)
                records.append(record)
    return records

def dump_json(records, fname):
    text = json.dumps(records, sort_keys=True, ensure_ascii=False, indent=2)
    with open(fname + ".json", "w") as fh:
        fh.write(text.encode("utf_8"))
    
if __name__ == '__main__':
    baseurl = "http://www.onmyo-za.net/"

    for yearlypage in detect_yearlypages():
    # for yearlypage in [2016]:
        if os.path.exists(str(yearlypage) + ".json"):
            os.remove(str(yearlypage) + ".json")
        yearlyurl = baseurl + "biography/" + str(yearlypage) + ".html"
        records = []
        for detailpath in detect_detailpages(yearlyurl):
            detailurl = baseurl + "setlist/" + detailpath
            records.extend(scraping(detailurl))
        dump_json(records, str(yearlypage))
        
