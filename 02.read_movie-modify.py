# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 2022 - Tue Feb 03 2022

@author: seoyun

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

bot = telegram.Bot(token ='token')

# https://api.telegram.org/bot'chat_id':'token'/getUpdates
chat_id = 'chat_id'

# 모든 일정에 대한 반복을 위해 url에 극장코드, 날짜, 작품코드를 입력받을 수 있게 함
theatercode = '0105'
date = '20220204'
screenratingcode = '16'


url = f"http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode={theatercode}&date={date}&screenratingcode={screenratingcode}"

res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

movies = soup.select("div.col-times")

# {영화제목 : 극장정보} 형식의 딕셔너리 생성
movie_dict = {}

if movies:
    # 영화제목 리스트
    title_list = [movie.parent.select("div.info-movie > a > strong")[0].text.strip() for movie in movies]
    #print(title_list)

    # 극장정보 가져오기
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
            
       