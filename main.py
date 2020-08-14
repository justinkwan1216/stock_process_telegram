import os
import datetime
import pickle
import subprocess
import telepot
import time
from telepot.loop import MessageLoop, OrderedWebhook
#from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
#from pattern.web import plaintext
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import get_all_tickers
import process_df
sched = BackgroundScheduler()



sched.start()
bot = telepot.Bot('1125134505:AAFBAIJoAQ486mNDEe3wLhDKk9qvvAyL9n0')
print(bot.getMe())

bot_status=0
tg_nyse = "0"
tg_nasdaq = "0"
tg_hk = "0"
nyse_threshold = {}
nasdaq_threshold  = {}
hk_threshold  = {}
current_price_max = {}
current_price_min = {}
ATR_2_max = {}
ATR_2_min = {}
peak_difference_max = {}
peak_difference_min = {}
bot_difference_max = {}
bot_difference_min = {}
tg_reminder = 1000

admin_id = [260780380]
users = []
#----------------user_command------
def set_nyse(user_id,bot,chat_id,params):
    global admin_id
    if user_id in admin_id:
        tg_nyse = parmas[0]
        text = "Set nyse to "+tg_nyse
        bot.sendMessage(chat_id, text)
    else:
        text = "You are not admin"
        bot.sendMessage(chat_id, text)


def set_nasdaq(user_id,bot,chat_id,params):
    global admin_id
    if user_id in admin_id:
        tg_nasdaq = parmas[0]
        text = "Set nasdaq to "+tg_nasdaq
        bot.sendMessage(chat_id, text)
    else:
        text = "You are not admin"
        bot.sendMessage(chat_id, text)

def set_hk(user_id,bot,chat_id,params):
    global admin_id
    if user_id in admin_id:
        tg_hk = parmas[0]
        text = "Set hk to "+tg_hk
        bot.sendMessage(chat_id, text)
    else:
        text = "You are not admin"
        bot.sendMessage(chat_id, text)

        
def update_nyse(user_id,bot,chat_id,params):
    if tg_nyse=="0":
        get_all_tickers.save_all_tickers(market_type="nyse")
        get_all_tickers.get_data_from_yahoo(market_type="nyse")
        text = "Updated nyse"
        bot.sendMessage(chat_id, text)
    else:
        text = "update on nyse is disabled"
        bot.sendMessage(chat_id, text)
        
def update_nasdaq(user_id,bot,chat_id,params):
    if tg_nasdaq=="0":
        get_all_tickers.save_all_tickers(market_type="nasdaq")
        get_all_tickers.get_data_from_yahoo(market_type="nasdaq")
        text = "Updated nasdaq"
        bot.sendMessage(chat_id, text)
    else:
        text = "update on nasdaq is disabled"
        bot.sendMessage(chat_id, text)

def update_hk(user_id,bot,chat_id,params):
    if tg_hk=="0":
        get_all_tickers.save_all_tickers(market_type="hk")
        get_all_tickers.get_data_from_yahoo(market_type="hk")
        text = "Updated hk"
        bot.sendMessage(chat_id, text)
    else:
        text = "update on hk is disabled"
        bot.sendMessage(chat_id, text)


def update_excel(user_id,bot,chat_id,params):
    global admin_id
    if user_id in admin_id:
        if bot_status==0:
            text = "Updating nyse"
            update_nyse(user_id,bot,chat_id,params)
            bot.sendMessage(chat_id, text)

            text = "Updating nasdaq"
            update_nasdaq(user_id,bot,chat_id,params)
            bot.sendMessage(chat_id, text)

            text = "Updating hk"
            update_hk(user_id,bot,chat_id,params)
            bot.sendMessage(chat_id, text)
        else:
            text = "bot is down"
            bot.sendMessage(chat_id, text)
    else:
        text = "You are not admin"
        bot.sendMessage(chat_id, text)
            
def set_current_price_max(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        current_price_max[chat_id] = params
        text = "current_price_max set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_current_price_min(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        current_price_min[chat_id] = params
        text = "current_price_min set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_ATR_2_max(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        ATR_2_max[chat_id] = params
        text = "ATR_2_max set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_ATR_2_min(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        ATR_2_min[chat_id] = params
        text = "ATR_2_min set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_peak_difference_max(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        peak_difference_max[chat_id] = params
        text = "peak_difference_max set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_peak_difference_min(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        peak_difference_min[chat_id] = params
        text = "peak_difference_min set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_bot_difference_max(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        bot_difference_max[chat_id] = params
        text = "bot_difference_max set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_bot_difference_min(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        bot_difference_min[chat_id] = params
        text = "bot_difference_min set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_nyse_threshold(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        nyse_threshold[chat_id] = params
        text = "nyse threshold set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)
def set_nasdaq_threshold(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        nasdaq_threshold[chat_id] = params
        text = "nasdaq threshold set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)

def set_hk_threshold(user_id,bot,chat_id,params):
    params = params[0]
    try:
        params = float(params)
        hk_threshold[chat_id] = params
        text = "hk threshold set to "+str(params)
    except:
        text = "Invalid threshold"
        
    bot.sendMessage(chat_id, text)

   
def process_nyse(user_id,bot,chat_id,params):
    if bot_status==0:
        threshold = nyse_threshold[chat_id]
        text = "processing nyse"
        bot.sendMessage(chat_id, text)
        process_df.process_data(user_id=str(user_id),market_type="nyse",threshold=nyse_threshold[chat_id])
        text = "nyse done processing\nuse /get_nyse_file to download the file"
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)

def process_nasdaq(user_id,bot,chat_id,params):
    if bot_status==0:
        threshold = nasdaq_threshold[chat_id]
        text = "processing nasdaq"
        bot.sendMessage(chat_id, text)
        process_df.process_data(user_id=str(user_id),market_type="nasdaq",threshold=nasdaq_threshold[chat_id])
        text = "nasdaq done processing\nuse /get_nasdaq_file to download the file"
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)

def process_hk(user_id,bot,chat_id,params):
    if bot_status==0:
        threshold = hk_threshold[chat_id]
        text = "processing hk"
        bot.sendMessage(chat_id, text)
        process_df.process_data(user_id=str(user_id),market_type="hk",threshold=hk_threshold[chat_id])
        text = "hk done processing\nuse /get_hk_file to download the file"
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
        
def scrape_nyse(user_id,bot,chat_id,params):
    if bot_status==0:
        p1=current_price_max[chat_id]
        p2=current_price_min[chat_id]
        p3=ATR_2_max[chat_id]
        p4=ATR_2_min[chat_id]
        p5=peak_difference_max[chat_id]
        p6=peak_difference_min[chat_id]
        p7=bot_difference_max[chat_id]
        p8=bot_difference_min[chat_id]
        try:
            file = str(user_id)+"/nyse_all.csv"
            df = pd.read_csv(file)
            df = df[(df['current_price'] < p1) & (df['current_price'] > p2) & (df['ATR_2'] < p3) & \
                  (df['ATR_2'] > p4) & (df['peak_difference'] < p5) & (df['peak_difference'] > p6) & \
                  (df['bot_difference'] < p7) & (df['bot_difference'] > p8)]
            df.to_csv(str(user_id)+"/nyse_scraped.csv")
            text = "nyse done scraping\nuse /get_nyse_scrape_file to download the file"
        except:
            text = "file not founded\nuse command /process_nyse first"
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)

def scrape_nasdaq(user_id,bot,chat_id,params):

    if bot_status==0:
        p1=current_price_max[chat_id]
        p2=current_price_min[chat_id]
        p3=ATR_2_max[chat_id]
        p4=ATR_2_min[chat_id]
        p5=peak_difference_max[chat_id]
        p6=peak_difference_min[chat_id]
        p7=bot_difference_max[chat_id]
        p8=bot_difference_min[chat_id]
        try:
            file = str(user_id)+"/nasdaq_all.csv"
            df = pd.read_csv(file)
            df = df[(df['current_price'] < p1) & (df['current_price'] > p2) & (df['ATR_2'] < p3) & \
                  (df['ATR_2'] > p4) & (df['peak_difference'] < p5) & (df['peak_difference'] > p6) & \
                  (df['bot_difference'] < p7) & (df['bot_difference'] > p8)]
            df.to_csv(str(user_id)+"/nasdaq_scraped.csv")
            text = "nasdaq done scraping\nuse /get_nasdaq_scrape_file to download the file"
        except:
            text = "file not founded\nuse command /process_nasdaq first"
    else:
        text = "bot is down"
        
    bot.sendMessage(chat_id, text)

def scrape_hk(user_id,bot,chat_id,params):

    if bot_status==0:
        p1=current_price_max[chat_id]
        p2=current_price_min[chat_id]
        p3=ATR_2_max[chat_id]
        p4=ATR_2_min[chat_id]
        p5=peak_difference_max[chat_id]
        p6=peak_difference_min[chat_id]
        p7=bot_difference_max[chat_id]
        p8=bot_difference_min[chat_id]
        try:
            file = str(user_id)+"/hk_all.csv"
            df = pd.read_csv(file)
            df = df[(df['current_price'] < p1) & (df['current_price'] > p2) & (df['ATR_2'] < p3) & \
                  (df['ATR_2'] > p4) & (df['peak_difference'] < p5) & (df['peak_difference'] > p6) & \
                  (df['bot_difference'] < p7) & (df['bot_difference'] > p8)]
            df.to_csv(str(user_id)+"/hk_scraped.csv")
            text = "hk done scraping\nuse /get_hk_scrape_file to download the file"
        except:
            text = "file not founded\nuse command /process_hk first"
    else:
        text = "bot is down"
        
    bot.sendMessage(chat_id, text)

def get_user_para(user_id,bot,chat_id,params):
    text=""
    if bot_status==0:
        p1=current_price_max[chat_id]
        text+="current_price_max: "+str(p1)+"\n"
        p2=current_price_min[chat_id]
        text+="current_price_min: "+str(p2)+"\n"
        p3=ATR_2_max[chat_id]
        text+="ATR_2_max: "+str(p3)+"\n"
        p4=ATR_2_min[chat_id]
        text+="ATR_2_min: "+str(p4)+"\n"
        p5=peak_difference_max[chat_id]
        text+="peak_difference_max: "+str(p5)+"\n"
        p6=peak_difference_min[chat_id]
        text+="peak_difference_min: "+str(p6)+"\n"
        p7=bot_difference_max[chat_id]
        text+="bot_difference_max: "+str(p7)+"\n"
        p8=bot_difference_min[chat_id]
        text+="bot_difference_min: "+str(p8)+"\n"
    else:
        text += "bot is down"
        
    bot.sendMessage(chat_id, text)
    

def get_nyse_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/nyse_all.csv")
        except:
            text = "file not founded\nuse command /process_nyse first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)
        
def get_nasdaq_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/nasdaq_all.csv")
        except:
            text = "file not founded\nuse command /process_nasdaq first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)

def get_hk_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/hk_all.csv")
        except:
            text = "file not founded\nuse command /process_hk first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)

def get_nyse_scrape_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/nyse_scraped.csv")
            text="file sent"
        except:
            text = "file not founded\nuse command /scrape_nyse first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)

def get_nasdaq_scrape_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/nasdaq_scraped.csv")
            text="file sent"
        except:
            text = "file not founded\nuse command /scrape_nasdaq first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)

def get_hk_scrape_file(user_id,bot,chat_id,params):
    if bot_status==0:
        try:
            send_file(chat_id,str(user_id)+"/hk_scraped.csv")
            text="file sent"
        except:
            text = "file not founded\nuse command /scrape_hk first"
        
    else:
        text = "bot is down"
    bot.sendMessage(chat_id, text)   
        
def display_userid(user_id,bot,chat_id,params):
    if bot_status==0:
        text = "Your user id: "+str(user_id)
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
    
def display_cmd(user_id,bot,chat_id,params):
    if bot_status==0:
        global admin_id
        text="Listed are all command available\n"
        for key, value in tg_commands_description.items() :
            text+=key+"\n"+value+"\n\n"
        if user_id in admin_id:
            for key, value in tg_admin_commands_description.items() :
                text+=key+"\n"+value+"\n\n"
            
        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)
    
def start(user_id,bot,chat_id,params):
    if bot_status==0:
        global users
        text=""
        if user_id not in users:
            users.append(user_id)
            text+="Welcome new user\nYou can type in /help to display all commands\n"
            nyse_threshold[chat_id] = 0.0025
            nasdaq_threshold[chat_id] = 0.0025
            current_price_max[chat_id] = 1
            current_price_min[chat_id] = 0
            ATR_2_max[chat_id] = 0.0025
            ATR_2_min[chat_id] = 0
            peak_difference_max[chat_id] = 1000
            peak_difference_min[chat_id] = 0
            bot_difference_max[chat_id] = 1000
            bot_difference_min[chat_id] = 0
            display_cmd(user_id,bot,chat_id,params)
        else:
            text+="You are already using this bot"


        bot.sendMessage(chat_id, text)
    else:
        text = "bot is down"
        bot.sendMessage(chat_id, text)

    

def add_admin(user_id,bot,chat_id,params):
    global admin_id
    text=""
    params = params[0]
    try:
        params = int(params)
        if user_id in admin_id:
            if params not in admin_id:
                admin_id.append(params)
                text += "Admin with id "+str(params)+" added"
            else:
                text += "Admin with id "+str(params)+" already added"
        else:
            text += "You are not admin"
        
    except:
        text+="enter valid id"
            
        bot.sendMessage(chat_id, text)



def save_all_para(user_id,bot,chat_id,params):
    global tg_reminder
    global admin_id
    global users
    global tg_nyse
    global tg_nasdaq
    global nyse_threshold
    global nasdaq_threshold
    global current_price_max
    global current_price_min
    global ATR_2_max
    global ATR_2_min
    global peak_difference_max
    global peak_difference_min
    global bot_difference_max
    global bot_difference_min

    text=""
    if user_id in admin_id:
        f = open('save.pickle', 'wb')
        
        pickle.dump((tg_reminder,users,admin_id,bot_status,tg_nyse,tg_nasdaq,nyse_threshold,nasdaq_threshold,current_price_max,\
                     current_price_min,ATR_2_max,ATR_2_min,peak_difference_max,peak_difference_min,bot_difference_max,bot_difference_min), f)
        f.close()
        text += "Saved all paramaters"
    else:
        text += "You are not admin"
    bot.sendMessage(chat_id, text)


def load_all_para(user_id,bot,chat_id,params):
    global tg_reminder
    global admin_id
    global users
    global tg_nyse
    global tg_nasdaq
    global nyse_threshold
    global nasdaq_threshold
    global current_price_max
    global current_price_min
    global ATR_2_max
    global ATR_2_min
    global peak_difference_max
    global peak_difference_min
    global bot_difference_max
    global bot_difference_min
    
    text=""
    if user_id in admin_id:
        f = open('save.pickle', 'rb')

        tg_reminder,users,admin_id,bot_status,tg_nyse,tg_nasdaq,nyse_threshold,nasdaq_threshold,current_price_max,\
                     current_price_min,ATR_2_max,ATR_2_min,peak_difference_max,peak_difference_min,bot_difference_max,bot_difference_min = pickle.load(f)
        f.close()
        text += "Loaded all paramaters"
    else:
        text += "You are not admin"
    bot.sendMessage(chat_id, text)
def list_job(user_id,bot,chat_id,params):
    text=""
    if user_id in admin_id:
        jobs = sched.get_jobs()
        text += str(jobs)
    else:
        text += "You are not admin"
    
    bot.sendMessage(chat_id, text)

def set_bot_status(user_id,bot,chat_id,params):
    global bot_status
    text=""
    try:
        params = params[0]
        params = int(params)
        if user_id in admin_id:
            bot_status=params
            if bot_status !=0:
                sched.shutdown()
            else:
                sched.start()
            text += "bot status set to "+str(params)
        else:
            text += "You are not admin"
    except:
        text += "bot status not integer"
    bot.sendMessage(chat_id, text)
        
def some_job(user_id,bot,chat_id,params):
    update_excel(user_id,bot,chat_id,params)


def delete_reminder(user_id,bot,chat_id,params):
    
    try:
        sched.remove_job(str(chat_id))
    except Exception as e:
        print(e)
        
def reminder(user_id,bot,chat_id,params):
    try:
        tg_reminder = float(params[0])
        if(tg_reminder<=10):
            text = "enter a larger value >10"
            bot.sendMessage(chat_id, text)
            return 0
    except ValueError: 
        text = "not a integer or float you have entered"
        bot.sendMessage(chat_id, text)
        return 0
    
    try:
        sched.remove_job(str(chat_id))
    except Exception as e:
        print(e)
        
    try:
        sched.add_job(some_job,'interval', seconds=tg_reminder,args=[user_id,bot,chat_id,params],id=str(chat_id))
    except Exception as e:
        print(e)

tg_commands = {"/start":start,"/help":display_cmd,"/reminder":reminder,"/delete_reminder":delete_reminder,"/scrape_nyse":scrape_nyse,"/scrape_nasdaq":scrape_nasdaq,"/scrape_hk":scrape_hk,\
               "/get_user_para":get_user_para,"/get_nyse_file":get_nyse_file,\
               "/get_nasdaq_file":get_nasdaq_file,"/get_hk_file":get_hk_file,"/get_nyse_scrape_file":get_nyse_scrape_file,"/get_nasdaq_scrape_file":get_nasdaq_scrape_file,"/get_hk_scrape_file":get_hk_scrape_file,\
               "/set_current_price_max":set_current_price_max,"/set_current_price_min":set_current_price_min,"/set_ATR_2_max":set_ATR_2_max,"/set_ATR_2_min":set_ATR_2_min,"/set_peak_difference_max":set_peak_difference_max,\
               "/set_peak_difference_min":set_peak_difference_min,"/set_bot_difference_max":set_bot_difference_max,"/set_bot_difference_min":set_bot_difference_min,"/process_nyse":process_nyse,\
               "/process_nasdaq":process_nasdaq,"/process_hk":process_hk,"/set_nyse":set_nyse,"/set_nasdaq":set_nasdaq,"/set_hk":set_hk,"/set_nyse_threshold":set_nyse_threshold,"/set_nasdaq_threshold":set_nasdaq_threshold,"/set_hk_threshold":set_hk_threshold,\
               "/update_excel":update_excel,"/display_userid":display_userid,"/save_all_para":save_all_para,"/load_all_para":load_all_para,\
               "/add_admin":add_admin,"/list_job":list_job,"/set_bot_status":set_bot_status}
tg_commands_description = {"help":"<usage: /help >","/display_userid":"<usage: /display_userid >","/reminder":"<usage: /reminder (time in seconds) >","/delete_reminder":"<usage: /delete_reminder >",\
                           "/scrape_nyse":"<usage: /scrape_nyse >","/scrape_nasdaq":"<usage: /scrape_nasdaq >","/scrape_hk":"<usage: /scrape_hk >","/get_user_para":"<usage: /get_user_para >",\
                           "/get_nyse_file":"<usage: /get_nyse_file >","/get_nasdaq_file":"<usage: /get_nasdaq_file >","/get_hk_file":"<usage: /get_hk_file >",\
                           "/get_nyse_scrape_file":"<usage: /get_nyse_scrape_file >","/get_nasdaq_scrape_file":"<usage: /get_nasdaq_scrape_file >","/get_hk_scrape_file":"<usage: /get_hk_scrape_file >",\
                           "/set_current_price_max":"<usage: /set_current_price_max (thres) >","/set_current_price_min":"<usage: /set_current_price_min (thres) >",\
                           "/set_ATR_2_max":"<usage: /set_ATR_2_max (thres) >","/set_ATR_2_min":"<usage: /set_ATR_2_min (thres) >",\
                           "/set_peak_difference_max":"<usage: /set_peak_difference_max (thres) >","/set_peak_difference_min":"<usage: /set_peak_difference_min (thres) >",\
                           "/set_bot_difference_max":"<usage: /set_bot_difference_max (thres) >","/set_bot_difference_min":"<usage: /set_bot_difference_min (thres) >",\
                           "/process_nyse":"<usage: /process_nyse >","/process_nasdaq":"<usage: /process_nasdaq >","/process_hk":"<usage: /process_hk >",\
                           "/set_nyse":"<usage: /set_nyse (0 is true/other) >","/set_nasdaq":"<usage: /set_nasdaq (0 is true/other) >",\
                           "/set_nyse_threshold":"<usage: /set_nyse_threshold (thres) >","/set_nasdaq_threshold":"<usage: /set_nasdaq_threshold (thres) >","/set_hk_threshold":"<usage: /set_hk_threshold (thres) >"
                           "/update_excel":"<usage: /update_excel >","/display_userid":"<usage: /display_userid >"
                           
                           }
tg_admin_commands_description = {"/save_all_para":"<usage: /save_all_para >","/load_all_para":"<usage: /load_all_para >","/add_admin":"<usage: /add_admin (admin_id)>",\
                                 "/list_job":"<usage: /list_job >","/set_bot_status":"<usage: /set_bot_status (status)>"}

#----------------inside_command------
def send_file(chat_id,filename):
    bot.sendDocument(chat_id, open(filename, 'rb'))
    
def delete_file(filename):
    os.remove(filename)

def delete(chat_id,reply):
    messageId = reply['message_id']
    bot.deleteMessage((chat_id, messageId))
    
def parse_cmd(cmd_string):
    text_split = cmd_string.split()
    # return cmd, params
    return text_split[0], text_split[1:]

def add_command(cmd, func):
    global tg_commands
    tg_commands[cmd] = func


def remove_command(cmd):
    global tg_commands
    del tg_commands[cmd]

#----------------------------
        



def handle(msg):
    
    global bot
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    jobs = sched.get_jobs()

    if len(jobs)<=5:

        if content_type == "text":
            user_id = msg['from']['id']
            msg_text = msg['text']
            chat_id = msg['chat']['id']
            msg_id = msg['message_id']
            #print("[MSG] {uid} : {msg}".format(uid=msg['from']['id'], msg=msg_text))
            if msg_text[0] == '/':
                cmd, params = parse_cmd(msg_text)
                try:
                    sched.add_job(tg_commands[cmd], args=[user_id,bot,chat_id, params])
                    #tg_commands[cmd](user_id,bot,chat_id, params)
                    

                except KeyError:
                    bot.sendMessage(chat_id, "Unknown command: {cmd}".format(cmd=cmd))



    else:
        bot.sendMessage(chat_id, "Bot is very busy")
   

MessageLoop(bot, handle).run_as_thread()
print("I'm listening...")


while(1):
    
    time.sleep(0.01)
