# -*- coding: utf-8 -*-


import argparse
import csv
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument("--data1",default="./data/台灣電力公司_過去電力供需資訊_All_2.csv",help="Input your power data.")
parser.add_argument("--data2",default="./data/本年度每日尖峰備轉容量率_2.csv",help="Input your power data.")
parser.add_argument("--data3",default="./data/Weather_2/",help="Input your weather data.")
parser.add_argument("--data4",default="./data/Holiday_2/csv/",help="Input your holiday data.")
parser.add_argument("--output",default="./data/training_data_test.csv",help="Output your training data.")
args=parser.parse_args()

data=[]#建立空矩陣，之後用來儲存CSV檔中的資料
with open(args.data1,newline='',encoding="utf-8") as csvfile:
    rows=csv.reader(csvfile)
    
    for row in rows:
        data.append(row)

#將資料轉成正確的格式（淨尖峰供電能力、尖峰負載）
supply_pw=[]
load_pw=[]
#operating_reserve=[]
for date in data:
    try:
        supply_pw.append(float(date[1]))
        load_pw.append(float(date[2]))
        #operating_reserve.append(float(date[3]))
    except:
        pass
    
supply_pw=np.asarray(supply_pw)
load_pw=np.asarray(load_pw)

#data2=[]
#with open(args.data2,newline='',encoding="utf-8") as csvfile:
#    rows=csv.reader(csvfile)
    
#    for row in rows:
#        data2.append(row)
        
#for date in data2[32:]:
#    try:
#        operating_reserve.append(float(date[1])*10)
#    except:
#        pass
    
#operating_reserve=np.asarray(operating_reserve)

'''
#觀察資料（淨尖峰供電能力、尖峰負載）
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
'''
xpt=[]
for date in data:
    xpt.append(date[0])
'''
fig, ax = plt.subplots(1,1)
ax.plot(xpt[1:],supply_pw,label='Supply Power',color='g')#以綠線表示淨尖峰供應電力
ax.plot(xpt[1:],load_pw,label='Load Power',color='r')#以紅線表示尖峰負載
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))#設定X軸標籤每30比顯示1比
plt.xlabel('Date')
plt.xticks(rotation='vertical')
plt.ylabel('Power(MW)')
plt.title('Supply & Load Power')
plt.legend(loc = 'upper left')
plt.savefig('./figure/Power.png')
plt.show()
'''
#是否為假日（民國108年至民國110年）（0為上班日、2為假日）（資料來源：行政院人事行政總處）
import os
path=args.data4
allFileList=os.listdir(path)
holiday=[]
for holiday_csv in allFileList:
    with open (path+holiday_csv,newline='') as csvfile:
        rows=csv.reader(csvfile)            
        for row in rows:
            holiday.append(row)   

T_holiday=[]            
for date in holiday:
    try:
        T_holiday.append(int(date[2]))
    except:
        pass
    
for date in holiday[1131:1159]:
    xpt.append(date[0])

#觀察資料（各地天氣）

path=args.data3
city=['Taipei','New_Taipei','Taoyuan','Taichung','Tainan','Kaohsiung']
taipei=[]
new_taipei=[]
taoyuan=[]
taichung=[]
tainan=[]
kaohsiung=[]
for city_name in city:
    allFileList=os.listdir(path+city_name)
    for weather_csv in allFileList:
        data=[]
        with open(path+city_name+"/"+weather_csv,newline='',encoding="utf-8") as csvfile:
            rows=csv.reader(csvfile)            
            for row in rows:
                data.append(row)              
        for weather in data:
            try:
                if city_name==city[0]:
                    taipei.append(float(weather[7]))
                elif city_name==city[1]:
                    new_taipei.append(float(weather[7]))
                elif city_name==city[2]:
                    taoyuan.append(float(weather[7]))
                elif city_name==city[3]:
                    taichung.append(float(weather[7]))
                elif city_name==city[4]:
                    tainan.append(float(weather[7]))
                elif city_name==city[5]:
                    kaohsiung.append(float(weather[7]))
            except:
                pass

taipei=np.asarray(taipei)
new_taipei=np.asarray(new_taipei)
taoyuan=np.asarray(taoyuan)
taichung=np.asarray(taichung)
tainan=np.asarray(tainan)
kaohsiung=np.asarray(kaohsiung)            
'''
fig, ax = plt.subplots(1,1)
ax.plot(xpt[1:],taipei,label=city[0],color='g')#以綠線表示臺北市
ax.plot(xpt[1:],new_taipei,label=city[1],color='r')#以紅線表示新北市
ax.plot(xpt[1:],taoyuan,label=city[2],color='b')#以藍線表示桃園市
ax.plot(xpt[1:],taichung,label=city[3],color='y')#以黃線表示臺中市
ax.plot(xpt[1:],tainan,label=city[4],color='k')#以黑線表示臺南市
ax.plot(xpt[1:],kaohsiung,label=city[5],color='c')#以藍綠色表示高雄市
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))#設定X軸標籤每30比顯示1比
plt.xlabel('Date')
plt.xticks(rotation='vertical')
plt.ylabel('Temperature(℃)')
plt.title('Weather of Special Municipality in Taiwan')
plt.legend(loc = 'upper left')
plt.savefig('./figure/Temperature.png')
plt.show()
'''
#天氣資料預處理，氣溫依據六都人口比重加權平均（六都人口資料統計至2021年二月）
p_taipei=2504597      # 2,504,597
p_new_taipei=3999305  # 3,999,305
p_taoyuan=2269997     # 2,269,997
p_taichung=2810285    # 2,810,285
p_tainan=1858650      # 1,858,650
p_kaohsiung=2738002   # 2,738,002
p_total=p_taipei+p_new_taipei+p_taoyuan+p_taichung+p_tainan+p_kaohsiung
temperature=[]
for i in range(len(xpt)-13):
    t_average=(taipei[i]*p_taipei+new_taipei[i]*p_new_taipei+taoyuan[i]*p_taoyuan+taichung[i]*p_taichung+tainan[i]*p_tainan+kaohsiung[i]*p_kaohsiung)/p_total
    temperature.append(t_average)
    

#將電力資料、天氣資料與放假資料整合
with open(args.output,'w',newline='') as csvfile:
    csv_write=csv.writer(csvfile)
    
    csv_write.writerow(["Date","Supply Power","Load Power","Temperature","Holiday"])
    #csv_write.writerow(["Date","Operating Reserve","Temperature","Holiday"])
    for i in range(len(xpt)-29):
        data_csv=[xpt[i+1],supply_pw[i],load_pw[i],temperature[i],T_holiday[i]]
        #data_csv=[xpt[i+1],operating_reserve[i],temperature[i],T_holiday[i]]
        csv_write.writerow(data_csv)