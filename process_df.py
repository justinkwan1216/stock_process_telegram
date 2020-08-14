import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import pandas_datareader.data as web
#---------------
def get_close_date(pd,date):
    while (1):
        date_close = pd.loc[pd['Date']==date]
        if (date_close.empty)==False:
            return date_close
        date+=1
        
def plot(minimum,length,new_df_ohlc,num=365):
    total=[]
    special_date=[0,91,182,242]
    special_date_2=[121,274]
        
    for k in range(num):
            
        analysis = pd.DataFrame()
        start=minimum+k
        #print(k)
        for i in range(length-362):
            j=i%365
            
            now=start+i

            if j in special_date:
                if k==364:
                    ax1.axvline(x=now,color='b',linewidth=0.5)
                date_close = get_close_date(new_df_ohlc,now)
                analysis = pd.concat([analysis,date_close])
            elif j in special_date_2:
                if k==364:
                    ax1.axvline(x=now,color='r',linewidth=0.5)
                date_close = get_close_date(new_df_ohlc,now)
                analysis = pd.concat([analysis,date_close])

                
        close = analysis.filter(['Close'])
        date = analysis.filter(['Date'])
        analysis['close_shift']=(close-close.shift(1))/close.shift(1)
        analysis['date_shift']=date-date.shift(1)
        analysis['slope']=((1+analysis['close_shift'])**(1/analysis['date_shift'])-1)*100
        analysis['abs_slope'] = abs(analysis['slope'])
        temp_point=[0,0]
        for index, row in analysis.iterrows():
            if temp_point!=[0,0]:
                if k==364:
                    ax1.plot([temp_point[0],row['Date']], [temp_point[1],row['Close']],'black',linewidth=1)
                temp_point=[row['Date'],row['Close']]
            else:
                temp_point=[row['Date'],row['Close']]
        #ax1.plot([734000,734091], [18,30],'m-',linewidth=1)
        total.append(analysis['abs_slope'].sum())

    total = np.array(total)
    sort_index = np.argsort(total)
    #print(total)
    sort_index_reverse=sort_index[::-1]
    cycle_max_relationship=sort_index_reverse[0]
    #print(cycle_max_relationship)
    return cycle_max_relationship,-np.sort(-total)
def return_positive(array):
    array = [item for item in array if item > 0]
    return array
def check_hit_rate(array):
    
    array = return_positive(array)
    #print(array)
    fib_hit=0
    three_hit=0
    five_hit=0
    seven_hit=0
    eight_hit=0
    twelve_hit=0
    ratio_hit=0
    fib=[5,13,34,55,89,233,377]
    ratio_array=[]
    special_number=[3,5,7,8,12]
    #special_number=[2,5,3,9,11]
    try:
        r=array[8]
    except:
        r=1
    try:
        while r<=array[-1]:
            r*=1.05946309436

            ratio_array.append(int(r))
            ratio_array.append(int(r)+1)
    except:
        return 0,0,0,0,0,0,0,0
    for each in array:
        if each in fib:
            fib_hit+=1
        if each in ratio_array:
            ratio_hit+=1
        if each%special_number[0]==0:
            three_hit+=1
        if each%special_number[1]==0:
            five_hit+=1
        if each%special_number[2]==0:
            seven_hit+=1
        if each%special_number[3]==0:
            eight_hit+=1
        if each%special_number[4]==0:
            twelve_hit+=1
    ratio_hit/=len(array)
    three_hit/=len(array)
    five_hit/=len(array)
    seven_hit/=len(array)
    eight_hit/=len(array)
    twelve_hit/=len(array)
    fib_hit/=len(array)
    
    
    return 0.2*ratio_hit+1.2*three_hit+0.7*five_hit+2*seven_hit+0.3*eight_hit+1*twelve_hit+0.5*fib_hit,ratio_hit,three_hit,five_hit,seven_hit,eight_hit,twelve_hit,fib_hit
import random
def process_peak_bot(df,np_array):
    result=[]
    for each in np_array:
        new=np_array-each
        b = check_hit_rate(new)
        result.append([each,b])
        
    result.sort(key=lambda x:x[1],reverse=True)
    number=0
    #number = random.randint(0, len(result))
    result_date=result[number][0]
    hit=result[number][1]
    #remove all number smaller than 0
    date_pattern=return_positive(np_array-result_date)

    date = df.iloc[[result_date]].index[0].date()
    array=[]
    for temp_date in date_pattern:
        array.append(df.iloc[[temp_date+result_date]].index[0].date())

    return result,result_date,list(hit),date_pattern,date,array,len(np_array)
def plot_all(plot):
    peak_dif,bot_dif,x,high_data,low_data,peak_x,bot_x,peak_df,bot_df = plot[0],plot[1],plot[2],plot[3],\
                                                                        plot[4],plot[5],plot[6],plot[7],plot[8]
    #plt.figure(figsize=(12, 5))
    fig1, ax3 = plt.subplots()
    fig2, ax4 = plt.subplots()
    ax3.plot(np.arange(len(peak_dif)),peak_dif)
    ax3.plot(np.arange(len(bot_dif)),bot_dif)

    ax4.plot(x,high_data, color='grey')
    ax4.plot(x,low_data, color='grey')
    ax4.plot(peak_x, peak_df['peak'].values, "o", label="max", color='b')
    ax4.plot(bot_x, bot_df['bot'].values, "o", label="min", color='r')
    #plt.plot(x[c], data[c], "o", label="max", color='b')
def process_df(df):
    new_df_ohlc=df[['Open','High','Low','Close','Volume']]
    new_df_ohlc.reset_index(inplace=True)
    new_df_ohlc['Date'] = new_df_ohlc.index
    
    #df_volume = new_df_ohlc['Volume']

    minimum=new_df_ohlc.iloc[0]['Date']
    maximum=new_df_ohlc.iloc[-1]['Date']

    length = int(maximum-minimum)

    #ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    #ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)


    #candlestick_ohlc(ax1, new_df_ohlc.values, colorup='g')
    #ax2.fill_between(df_volume.index, df_volume.values, 0)

    new_df = new_df_ohlc
    x = new_df['Date'].values
    high_data = new_df['High'].values
    low_data = new_df['Low'].values

    new_df["max"] = ((new_df["High"].shift(-3) < new_df["High"]) &
                (new_df["High"].shift(-2) < new_df["High"]) &
                (new_df["High"].shift(-1) < new_df["High"]) &
                (new_df["High"].shift(1) < new_df["High"]) &
                (new_df["High"].shift(2) < new_df["High"]) &
                (new_df["High"].shift(3) < new_df["High"])).astype(int)

    new_df["min"] = ((new_df["Low"].shift(-3) > new_df["Low"]) &
                (new_df["Low"].shift(-2) > new_df["Low"]) & 
                (new_df["Low"].shift(-1) > new_df["Low"]) &
                (new_df["Low"].shift(1) > new_df["Low"]) &
                (new_df["Low"].shift(2) > new_df["Low"]) &
                (new_df["Low"].shift(3) > new_df["Low"])).astype(int)

    new_df['peak'] = new_df["max"]*new_df_ohlc['High']
    new_df['bot'] = new_df["min"]*new_df_ohlc['Low']

    peak_df = new_df[(new_df['peak'] > 0)]
    bot_df = new_df[(new_df['bot'] > 0)]
    peak_x=peak_df['Date'].values
    bot_x=bot_df['Date'].values
    peak_dif = np.diff(peak_x)
    bot_dif = np.diff(bot_x)
    peak_all = process_peak_bot(df,peak_x)
    bot_all = process_peak_bot(df,bot_x)
    peak_date = peak_all[4]
    bot_date = bot_all[4]

    last_date = df.tail(1).index[0].date()
    df.reset_index(inplace=True)
    
    
    peak_last_difference = len(df)-1-df.set_index('Date').index.get_loc(peak_date)
    bot_last_difference = len(df)-1-df.set_index('Date').index.get_loc(bot_date)
    
    #peak_result_cor_list,peak_result_no,peak_hit,peak_date_pattern,peak_result_date,peak_array,peak_count
    #bot_result_cor_list,bot_result_no,bot_hit,bot_date_pattern,bot_result_date,bot_array,bot_count
    plot_all = (peak_dif,bot_dif,x,high_data,low_data,peak_x,bot_x,peak_df,bot_df)
    return peak_all,bot_all,last_date,peak_last_difference,bot_last_difference,plot_all

import csv
import os
style.use('ggplot')
def process_data(user_id="",market_type="nyse",threshold=0.025):
    directory = "stock_"+market_type+"/"
    file_list=[]
    if not os.path.exists(user_id):
        os.makedirs(user_id)
    
    with open(user_id+"/"+market_type+"_all.csv", 'w+', newline='') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile, delimiter =",")


            writer.writerow(['ticker', 'peak_cycle_date','bot_cycle_date','peak_pattern','bot_pattern','peak_date',\
                             'bot_date','peak_hit','bot_hit','all_peak_count','all_bot_count','last_date','peak_difference','bot_difference','ATR_2','current_price','signal'])
            
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_list.append(filename)

    flag=True
    for file in file_list:
        print(file)
        
        try:
            if flag:
                df = pd.read_csv(directory+file, parse_dates=True, index_col=0)
                if df['ATR_2'].iloc[-1]<=threshold:
                    signal=True
                else:
                    signal=False
                result = process_df(df)
                
                
                
                with open(user_id+"/"+market_type+"_all.csv", 'a+', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile, delimiter =",")

                    peak_date_array=[]
                    bot_date_array=[]
                    for each in result[0][5]:
                        peak_date_array.append(str(each))
                    for each in result[1][5]:
                        bot_date_array.append(str(each))
                    if signal:
                        writer.writerow([file.replace(".csv",""),result[0][4],result[1][4],result[0][3],result[1][3],\
                                     peak_date_array,bot_date_array,result[0][2],result[1][2],result[0][6],result[1][6],result[2],result[3],result[4],df["ATR_2"].iloc[-1],df["Close"].iloc[-1],"T"])
                    else:
                        writer.writerow([file.replace(".csv",""),result[0][4],result[1][4],result[0][3],result[1][3],\
                                     peak_date_array,bot_date_array,result[0][2],result[1][2],result[0][6],result[1][6],result[2],result[3],result[4],df["ATR_2"].iloc[-1],df["Close"].iloc[-1],"F"])                    
        except:
            continue
        #if file=="FWP.csv":
        #    flag=True
              
    #plot_all(result[2])



    

#---------------------
plt.show()
