# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 2022 - Tue Feb 03 2022

@author: seoyu

@memo: 메세지 내용 수정을 위한 코드 수정
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

bot = telegram.Bot(token ='5027753346:AAEIKBEv-DrekFl7QXdgR6--RhJ4gEBd-mE')

# https://api.telegram.org/bot5027753346:AAEIKBEv-DrekFl7QXdgR6--RhJ4gEBd-mE/getUpdates
chat_id = '5043724522'

theatercode = '0105'
date = '20220204'
screenratingcode = '16'


url = f"http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode={theatercode}&date={date}&screenratingcode={screenratingcode}"

res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

movies = soup.select("div.col-times")
movie_dict = {}
title_list = []

if movies:
    # 영화제목
    title_list = [movie.parent.select("div.info-movie > a > strong")[0].text.strip() for movie in movies]
    #bot.sendMessage(chat_id=chat_id, text = title)

    # 상영
    for movie in movies:
        informations = movie.find("div", attrs = {"class":"info-timetable"}).find_all('a')
        for info in informations:
            current_playnum = int(info["data-playnum"])
            for title in title_list:
                movie_dict[title] = info["data-theatername"]
                if current_playnum >= int(info["data-playnum"]):
                    pass
                else:
                    past_palynum = current_playnum
                    current_playnum = int(info["data-playnum"])

for movie, theater in movie_dict.items():
    print(f"{theater} : {movie} 예매 오픈 준비")
                        
                
#message = f"\n{time.get_text()} | {link}"
#bot.sendMessage(chat_id=chat_id, text = message, parse_mode = "Markdown",disable_web_page_preview = True)
            
       