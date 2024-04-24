# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vQHsHbDExtE5BHjvwNTdWJEnYcXaXK6K
"""

import tensorflow as tf
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Flatten
from keras.regularizers import l2
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from google.colab import drive
drive.mount('/content/drive')

path_y = r"/content/drive/MyDrive/y_train.csv"
path_x = r"/content/drive/MyDrive/x_train.csv"
data_x = pd.read_csv(path_x)
dfx = pd.DataFrame(data_x)

data = pd.read_csv(path_y, delimiter=',')
df = pd.DataFrame(data)

names_cultur = ['rice', 'maize', 'chickpea', 'kindeybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'promegranate', 'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']
names = ['Nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']

for j in names:
    if type(dfx[j]) != float:
        dfx[j] = dfx[j].astype(float)


def replace_with_id(column, mapping):
    return [float(mapping[i]) for i in column]


label = {}
count1 = 0

for i in df['label']:
    if i not in label:
        label[i] = count1
        count1 += 1

df['label'] = replace_with_id(df['label'], label)

x = dfx[['Nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']].values
y = df[['label']].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = Sequential([
    Flatten(input_dim=7),
    Dense(2048, activation='sigmoid'),
    Dropout(0.2),
    Dense(2048, activation='sigmoid'),
    Dropout(0.2),
    Dense(1024, activation='sigmoid'),
    Dropout(0.2),
    Dense(512, activation='sigmoid'),
    Dropout(0.2),
    Dense(256, activation='sigmoid'),
    Dropout(0.1),
    Dense(1, activation='relu')
])

model.compile(optimizer=Adam(), loss='mse', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), batch_size=2)
model.save('model_v.1', save_format='h5')
loss, accuracy = model.evaluate(x_test, y_test, batch_size=128)
print(f"Accuracy: {accuracy*100}%\nLoss: {loss}")

import keras.models
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

model = keras.models.load_model('model_v.1')
result = model.predict(x_test)
print(
      f"Predict: {result[300]}\n"
      f"Test data: {y_test[300]}"
      )

print("predict:", names_cultur[int(result[300] - 1)])
print("real:", names_cultur[int(y_test[300] - 1)])

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras


accuracy1 = history.history['accuracy']
loss1 = history.history['loss']


history_df = pd.DataFrame({'accuracy': accuracy1, 'loss': loss1})

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(history_df.index, history_df['accuracy'], 'g', label='Точность')
plt.title('График зависимости точности нейросети')
plt.xlabel('Эпохи')
plt.ylabel('Точность')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history_df.index, history_df['loss'], 'r', label='Ошибка')
plt.title('График зависимости ошибки нейросети')
plt.xlabel('Эпохи')
plt.ylabel('Ошибка')
plt.legend()

plt.tight_layout()
plt.show()