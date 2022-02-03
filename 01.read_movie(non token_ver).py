# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 21:45:47 2022

@author: seoyu
"""

import requests
from bs4 import BeautifulSoup
import time


# html에 상영정보만 포함이 되지 않음을 확인
#with open("cgv.html", "w", encoding="utf8") as f:
#    f.write(soup.prettify())

#driver = webdriver.Chrome('Chromedriver.exe')

#driver.get("http://www.cgv.co.kr/arthouse/show-times.aspx?theatercode=0004")
#driver.switch_to.frame('ifrm_movie_time_table')
#html = driver.page_source


import telegram
from telegram.ext import Updater, CommandHandler

bot = telegram.Bot(token ='token')

# https://api.telegram.org/bot5027753346:AAEIKBEv-DrekFl7QXdgR6--RhJ4gEBd-mE/getUpdates
chat_id = 'chat_id'

url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?theatercode=0105&date=20220121&screencodes=&screenratingcode=16"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

movies = soup.select("div.col-times")

if movies:
    for movie in movies:
        # 영화제목
        title = movie.parent.select("div.info-movie > a > strong")[0].text.strip()
        bot.sendMessage(chat_id=chat_id, text = title)
        #print(title)
        # 예매정보
        informations = movie.find("div", attrs = {"class":"info-timetable"}).find_all('a')
        
        for info in informations:

            # 예매링크 
            link = "[예매하기](http://www.cgv.co.kr" + info["href"] + ")"
        
            # 극장정보
            if info.select("span") == "마감":
                theater = info.select("span").get_text()
                
            else:
                theater = info["data-screenkorname"]
            
            # 시간표
            for time in info.select("em"):
                #print("{} | {}".format(time.get_text(), theater))
                #print(link)
                message = f"\n{time.get_text()} | {theater}\n{link}"
                bot.sendMessage(chat_id=chat_id, text = message, parse_mode = "Markdown",disable_web_page_preview = True)
            
   