# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed, Dropout
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--data",default="./data/training_data_3.csv",help="Input your training data.")
parser.add_argument("--predict_data_all",default="./data/predict_dataset_all.csv",help="Input your predict data range.")
parser.add_argument("--predict_data_34",default="./data/predict_dataset_34.csv",help="Input your predict data range.")
parser.add_argument("--output",default="submission_34_type_2.csv",help="Output your predict data.")
args=parser.parse_args()

"""
#匯入資料集
train_data = pd.read_csv(args.data)
#讀取前20條data
train_data.head(20)

def readTrain():
    train = pd.read_csv(args.data)
    return train

#正規化
def normalize(train):
    train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
    return train_norm

#建立訓練data
def buildTrain(train,pastDay=30,futureDay=8):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
        X_train.append(np.array(train.iloc[i:i+pastDay]))
        Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Supply Power"])
        -np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Load Power"]))
    return np.array(X_train), np.array(Y_train)

#分割data
def splitData(X,Y,rate):
    X_train = X[int(X.shape[0]*rate):]
    Y_train = Y[int(Y.shape[0]*rate):]
    X_val = X[:int(X.shape[0]*rate)]
    Y_val = Y[:int(Y.shape[0]*rate)]
    return X_train, Y_train, X_val, Y_val

# read SPY.csv
train = readTrain()

# Normalization
train_norm = normalize(train)

# build Data, use last 30 days to predict next 5 days
X_train, Y_train = buildTrain(train_norm, 30, 8)

# split training data and validation data
X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

def buildManyToManyModel(shape, mode_type):
    
    if mode_type == 0: # unit= 4 
        model = Sequential()
        model.add(LSTM(4, input_length=shape[1], input_dim=shape[2], return_sequences=True))
        # output shape: (7, 1)
        model.add(TimeDistributed(Dense(1)))
        model.compile(loss="mse", optimizer="Adam")
        model.summary()
        
    elif mode_type == 1: # unit to bigger 20 
        model = Sequential()
        model.add(LSTM(20, input_length=shape[1], input_dim=shape[2], return_sequences=True))
        # output shape: (7, 1)
        model.add(TimeDistributed(Dense(1)))
        model.compile(loss="mse", optimizer="Adam")
        model.summary()
        
    elif mode_type == 2:  # unit to bigger 100
        model = Sequential()
        model.add(LSTM(100, input_length=shape[1], input_dim=shape[2], return_sequences=True))
        # output shape: (7, 1)
        model.add(TimeDistributed(Dense(1)))
        model.compile(loss="mse", optimizer="Adam")
        model.summary()
    
    return model

train = readTrain()

train_norm = normalize(train)
# change the last day and next day 
X_train, Y_train = buildTrain(train_norm,15, 15)

X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

model = buildManyToManyModel(X_train.shape, 2)
callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")

Y_train=np.reshape(Y_train,(Y_train.shape[0],Y_train.shape[1],1))
Y_val=np.reshape(Y_val,(Y_val.shape[0],Y_val.shape[1],1))
history=model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])

fig = plt.figure()
plt.plot(history.history['loss'],label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(loc='upper right')
fig.savefig("./figure/power_prediction_type_2.png")

model.save('./power_prediction_type_2.h5')
"""
from tensorflow.keras.models import load_model
model = load_model('./power_prediction_type_2.h5') 

#predict_data = pd.read_csv(args.data)
predict_data = pd.read_csv(args.predict_data_34)

#正規化
def normalize(train):
    train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
    return train_norm

#建立訓練data
def buildTrain(train,pastDay=8,futureDay=8):
    X_predict = []
    for i in range(predict_data.shape[0]-futureDay-pastDay):
        X_predict.append(np.array(train.iloc[i:i+pastDay]))
    return np.array(X_predict)



# Normalization
predict_norm = normalize(predict_data)

# build Data, use last 30 days to predict next 5 days
X_predict = buildTrain(predict_norm, 15, 15)
print(X_predict.shape)
print(X_predict)

predict = model.predict(X_predict)
predict_reshape=np.reshape(predict,(predict.shape[0],predict.shape[1]))
sub=predict_reshape[-1]
dfs= pd.DataFrame(sub)
denorm = dfs.apply(lambda x: x*(np.max(predict_data['Supply Power']-predict_data['Load Power'])
                    -np.min(predict_data['Supply Power']-predict_data['Load Power']))
                    +np.mean(predict_data['Supply Power']-predict_data['Load Power']))
            
df_SP = dfs.apply(lambda x: x*(np.max(predict_data['Supply Power'])-np.min(predict_data['Supply Power']))+np.mean(predict_data['Supply Power']))
df_LP = dfs.apply(lambda x: x*(np.max(predict_data['Load Power'])-np.min(predict_data['Load Power']))+np.mean(predict_data['Load Power']))
            
            
dfs_print = denorm
#print(dfs_print)
#dfs_print.drop([0],inplace=True)
new1=dfs_print.rename({0:20220330, 1:20220331, 2:20220401,3:20220402,4:20220403,
                       5:20220404,6:20220405,7:20220406,8:20220407,9:20220408,
                       10:20220409,11:20220410,12:20220411,13:20220412, 14:20220413},axis='index')
print(new1)
new1.to_csv(args.output)
