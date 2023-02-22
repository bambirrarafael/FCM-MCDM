import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import layers


mnist = tf.keras.datasets.mnist
data = pd.read_excel('D:\Programas\Doutorado\FCM-MCDM\dados\exemplo_artigo_petr.xlsx')

model = keras.Sequential()
model.add(keras.Input(shape=(3, 1)))
model.add(layers.SimpleRNN(9, activation='sigmoid'))
model.add(layers.Dense(6, activation='sigmoid'))
adam = keras.optimizers.Adam(learning_rate=0.01)

hist = model.fit(data[['var_1', 'var_2', 'var_3']], data[['c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6']], epochs=100, verbose=1)


print()

