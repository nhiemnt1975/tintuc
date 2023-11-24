from telegram.ext import (Updater, CommandHandler, CallbackContext)
from typing import List, Union
from telegram import (KeyboardButton, ParseMode, ReplyKeyboardMarkup, Update)
import requests
from bs4 import BeautifulSoup
import schedule
import time

# hàm thực hiện
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Xin sẵn lòng được phục vụ ngài {update.effective_user.first_name}')

# key board
_keyboard: List[List[Union[str, KeyboardButton]]] = [
            ['/News', '/Vanban', '/Stock']
        ]
reply_markup = ReplyKeyboardMarkup(_keyboard, resize_keyboard=True)

def get_news():
    list_news = []
    r = requests.get("https://vnexpress.net/")
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("h3", {"class": "title-news"})

    for new in mydivs:
        newdict = {}
        newdict["link"] = new.a.get("href")
        newdict["title"] = new.a.get("title")
        list_news.append(newdict)

    return list_news

def get_luatvietnam():
    list_news = []
    r = requests.get("https://luatvietnam.vn/")
    soup = BeautifulSoup(r.text, 'html.parser')
    mydivs = soup.find_all("h2", {"class": "doc-title"})
    for new in mydivs:
        newdict = {}
        newdict["link"] = 'https://luatvietnam.vn/'+new.a.get("href")
        newdict["title"] = new.a.get("title")
        list_news.append(newdict)
    return list_news


def get_vietstock():
  list_news = []
  r = requests.get("https://www.tinnhanhchungkhoan.vn/")
  soup = BeautifulSoup(r.text, 'html.parser')
  mydivs = soup.find_all("h2", {"class": "story__heading"})
  for new in mydivs:
    newdict = {}
    newdict["link"] = 'https://www.tinnhanhchungkhoan.vn/' + new.a.get("href")
    newdict["title"] = new.a.get("title")
    list_news.append(newdict)
  return list_news


def luatvietnam(update: Update, context: CallbackContext) -> None:
    data = get_luatvietnam()

    for item in data:

        update.message.reply_text(f'{item["link"]}')



def news(update: Update, context: CallbackContext) -> None:
    data = get_news()
    # str1 = ""

    for item in data:
    #     str1 += item["title"] + "\n"
    # update.message.reply_text(f'{str1}')
        update.message.reply_text(f'{item["link"]}')


def vietstock(update: Update, context: CallbackContext) -> None:
  data = get_vietstock()

  for item in data:
    update.message.reply_text(f'{item["link"]}')

updater = Updater('6132912662:AAHUYpZSrlxEHfSJoOkySWZSX3yOveYFDpY')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('vanban', luatvietnam))
updater.dispatcher.add_handler(CommandHandler('news', news))
updater.dispatcher.add_handler(CommandHandler('stock', vietstock))


updater.start_polling()
updater.idle()

schedule.every().day.at("16:15").do(get_news)

while True:
    schedule.run_pending()
    time.sleep(1)
