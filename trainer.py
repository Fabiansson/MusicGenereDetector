# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras import models
from keras import layers

data = pd.read_csv('./data/features_with_var_parentlabels.csv')

# Dropping unnecessary columns
data = data.drop(['filename'], axis=1)

# create genre list
genre_list = data.iloc[:, -1]
encoder = LabelEncoder()
y = encoder.fit_transform(genre_list)

# normalizing the dataset
scaler = StandardScaler()
X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype=float))

# split in training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# creating a model
model = models.Sequential()
model.add(layers.Dense(512, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(8, activation='softmax'))

# learning process
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# train
history = model.fit(X_train,
                    y_train,
                    validation_data=(X_test, y_test),
                    epochs=100,
                    batch_size=128)

print(model.summary())
model.save('music_genre_detector_model')

# evaluate
test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=128)
print('Test Accuracy: ', test_acc)
