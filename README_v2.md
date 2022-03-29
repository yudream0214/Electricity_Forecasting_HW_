# Electricity-Forecasting
## 簡介
使用台灣電力公司提供之過去電力供需資訊搭配天氣資料以及是否為上班日，並基於長短期記憶（Long Short-Term Memory，LSTM）建立一預測模型，用以預測未來14天之電力備轉容量。
## 使用數據
使用基本的便利資料，並加上氣象資料(溫度)以及工作日資料表，經過整理後合併為訓練資料集。並藉由此資料來建構備轉容量之預測模型進行未來14天之電力備轉容量。
其中電力備轉容量為系統運轉尖峰能力減去系統瞬時負載，並擷從2019年1月1日至2022年2月28日該期間的數據。

#### 電力
* 資料來源：[台灣電力股份有限公司（台灣電力公司_過去電力供需資訊）]( https://data.gov.tw/dataset/19995)
* 時間範圍：2019年1月1日至2022年2月28日（由於本年度3月份有斷電的情況，故不將該期間的資料列入考量）

### 天氣
* 資料來源：[中央氣象局（觀測資料）]( https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp)
* 時間範圍：2019年1月1日至2022年2月28日
* 地區：臺北市、新北市、桃園市、台中市、台南市、高雄市
* 說明：台灣人口約70％集中於六個直轄市中（臺北市、新北市、桃園市、臺中市、臺南市、高雄市），在六個直轄市中各取一個氣象觀測站作為代表。由北至南分別為臺北 TAIPEI （466920）、板橋 BANQIAO （466880）、中壢 Zhongli （C0C700）、臺中 TAICHUNG （467490）、臺南 TAINAN （467410）、高雄 KAOHSIUNG （467440)。
並依據當地人口數將氣溫加權平均，取得訓練用之平均氣溫。各地區人口數如下表所示，這些地區人口數約佔台灣總人口數七成，台灣總人口為23319776人。（統計至2022年2月）資料來源：[內政部統計處 內政統計查詢網](https://statis.moi.gov.tw/micst/stmain.jsp?sys=100)

| Location| Population
| --- | ---:
|臺北市|2504597
|新北市|3999305
|桃園市|2269997
|臺中市|2810285
|臺南市|1858650
|高雄市|2738002
|Total|16180836

### 是否為工作日
* 資料來源：[行政院人事行政總處（中華民國政府行政機關辦公日曆表）](https://data.gov.tw/dataset/14718)
* 時間範圍：2019年（民國108年）至2022年（民國111年）
* 說明：紀錄台灣行政機關當日是否為工作日，資料中包含日期、星期、是否放假（0：否，2：是）以及備註。

| 西元日期 |星期 |是否放假 | 備註
|:---:|---:|---:|---:
|20220101|六|2|開國紀念日
|20220102|日	|2|
|20220103|一	|0|
|20220104|二	|0|
|20220105|三	|0|


### 數據相關性分析
以python pandas來對整體數據進行探索性分析，並以圖表的形式來觀察數據之間的相關性。
* 相關性混淆矩陣
![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/corr_all_heatmap.png "Corr All")  
可透過上面的圖表可以得知數據中個欄位之間的相關訊息(+: 正相關, -:負相關)
如果只單一觀察[台灣電力公司_過去電力供需資訊]的資料欄位，可以發現出大多的特徵與預測目標(備轉容量)的相關性非常低。

為此將特徵欄位藉由上述圖表進行第一次的特徵選擇，並加入是否為上班日的特徵進行相關性檢視。
![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/corr.png "Corr Value")  
由此圖可得知備轉容量該目標與[淨尖峰供電能力、尖峰負載]有非常高的相關性，而[淨尖峰供電能力、尖峰負載]與否為上班日有著一定的關係。

### 可視化圖表
由上入的相關性分析流程找出本案例所需的主要特徵，接續透過可視化圖表檢視數據分布情況，以利於後續的分析決策。

#### 一.電力資料可視化

資料中包含台灣每日各發電廠發電量與民生、工業用電量，進而推算淨尖峰供電能力、尖峰負載、備轉容量以及備轉容率。在時間範圍中系統運轉尖峰能力與系統瞬時負載大致呈現M形曲線。

![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/Power_v2.png "Power")

#### 二.溫度時間可視化

在時間範圍中各地氣溫大致呈現M形曲線。 

![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/Temperature_v2.png "Temperature")

#### 三.是否為工作日與電力分布可視化

觀察數據後發現工作日之系統運轉尖峰能力及系統瞬時負載明顯比非工作日高, 且部分數據會有呈現連續高峰約5天後再下降2天。
此外下列三張圖表的時間段包含連假特性，更方便做觀察。

![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/Holiday.png "Holiday")

![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/尖峰負載_MW.png "尖峰負載")

![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/淨尖峰供電能力_MW_.png "淨尖峰供電能力")

## 數據清洗
依據上述可視化方法與相關性分析挑選出的特徵進行training data的建構。
在實作上需去除掉用不到的特徵，如電力資料中各發電廠的發電量、天氣資料中測站位置資訊, 此數據前處理的程序會建構在[**data_processing_main.py**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/data_processing_main.py)去除不需要的數據，並將其整合為[**training_data_3.csv**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/data/training_data_3.csv)輸出以方便後續訓練，其中包含日期、尖峰電量、負載電量、加權後之氣溫以及是否為工作日。  

training data.csv的資料格式:

| Date| Supply Power| Load Power | Temperature | Holiday
|:---:|---:|---:|---:|---:
|20220223|33885|31318|21.74403735|0
|20220224|33609|31098|20.60402425|0
|20220225|33527|30121|15.63952502|0
|20220226|31259|27822|16.49920859|2
|20220227|29926|26196|19.43096822|2
|20220228|31464|27337|20.17672128|2


### 環境要求

| Name| Version
|:---:|---:
|Python|3.6.7
|Numpy|1.15.4
|Pandas|0.23.4
|matplotlib|3.0.2

### 命令參數

|Name|Input|Default
|:---:|---|---
|--data1|電力資料|./data/台灣電力公司_過去電力供需資訊_All_2.csv
|--data2|至2022年2月28日之備載容量|./data/本年度每日尖峰備轉容量率_2.csv
|--data3|天氣資料所在資料夾|./data/Weather_2/
|--data4|辦公日曆表所在資料夾|./data/Holiday_2/
|--output|輸出資料格式(訓練資料)|./data/training_data_3.csv

可於直接於終端機中執行以下指令，並將參數改成你的參數，或是直接使用我們的預設值而不輸入參數。  

    python data_processing.py --data1 "your power data" --data2 "your operating reserve data" --data3 "your weather data" --data4 "your holiday data" --output "your output data"
### 輸出
輸出之[**training_data.csv**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/data/training_data_3.csv)格式如下表所示。

| Date| Supply Power| Load Power | Temperature | Holiday
|:---:|---:|---:|---:|---:
|20220223|33885|31318|21.74403735|0
|20220224|33609|31098|20.60402425|0
|20220225|33527|30121|15.63952502|0
|20220226|31259|27822|16.49920859|2
|20220227|29926|26196|19.43096822|2
|20220228|31464|27337|20.17672128|2



## 建立預測模型
利用上述整理好的[**training_data_3.csv**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/data/training_data_3.csv)於[**app_main.py**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/app_main.py)中進行模型訓練與預測。在[**app.py**](https://github.com/vf19961226/Electricity-Forecasting/blob/main/app.py)中將數據進行正規化後切割成訓練與測試兩組，使用長短期記憶（Long Short-Term Memory，LSTM）建立一預測模型，用以預測未來14天之電力備轉容量。

### 環境要求
| Name| Version
|:---:|---:
|Python|3.6.7
|Numpy|1.15.4
|Pandas|0.23.4
|matplotlib|3.0.2
|Keras|2.1.6

### 數據前處理
* 資料正規化   
```py
train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
```  
* 建立訓練集  
以過去x天 預測未來y天  
```py
def buildTrain(train,pastDay=x,futureDay=y)
```
* 分割數據   
X_Train為訓練數據，Ｙ_Train為label(備轉容量），並將10%數據做為驗證用途
```py
def splitData(X,Y,rate)
```
* 建立模型架構 
![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/LSTM_architecture_D15.png "LSTM_architecture")   
* 損失函數表現  
![GITHUB](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/figure/power_prediction_type_0.png "power_prediction_type_0.png")

### 命令參數

|Name|Input|Default
|:---:|---|---
|--data|訓練資料|./data/training_data.csv
|--predict_data_34|預測期間資料|./data/predict_dataset_34.csv
|--output|輸出預測結果|submission.csv

可於直接於終端機中執行以下指令，並將參數改成你的參數，或是直接使用我們的預設值而不輸入參數。  

    python app.py --data "your training data" --output "your output data"
    python app.py --data "your training data" --predict_data_34 "your predict data" --output "your output data"

### 預測結果
最終預測結果輸出為[**submission.csv**](https://github.com/yudream0214/Electricity_Forecasting_HW_1/blob/main/submission.csv)，其內容如下表所示。

| Date	| Operating Reserve(MW)
|---|:---:
|20220330|2955.505
|20220331|2990.3035
|20220401|3015.513
|20220402|3030.107
|20220403|3005.2974
|20220404|2970.9314
|20220405|2937.195
|20220406|2917.7432
|20220407|2925.5376
|20220408|2948.712
|20220409|2989.157
|20220410|2982.6519
|20220411|2940.2656
|20220412|2927.378
|20220413|2963.7002

