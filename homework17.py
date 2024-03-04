# -*- coding: utf-8 -*-
"""homework17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NIRiw72x6VTb1g-xByKR4vCZdeuhda9Y

**Homework 17**

Here are all the imports you will need for this assigment:
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.optimizers import Adam

"""To begin we make up some sequential data and visualize it:"""

t=np.arange(1000)/10
data=np.sin(t)+np.sin(0.7*t+0.1)

plt.scatter(t,data)

"""Now, we break up `data` into sequences of length 10.  For each such seqence, we define a target `y` which is the next data value."""

X=[]
y=[]
for i in range(1000-11):
  X.append(data[i:i+10])
  y.append(data[i+10])

X=np.array(X)
y=np.array(y)

X.shape, y.shape

"""To see what we have just created, look at X[1] (a data sequence of length 10), and y[1], the value we would like to predict:"""

X[1], y[1]

"""To feed the sequences into a recurrent neural network, we have to get the input shape correct. This is required to be (num_sequences, sequence_length, num_features). Since each element of each sequence is just a single number (rather than a vector of numbers), the number of features is 1. So we reshape as follows:"""

X=X.reshape(989,10,1)

"""Do an 80/20 train/test split to obtain Xtrain, Xtest, ytrain and ytest."""

Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,train_size=0.8)

"""Now define the model! You only need three layers: an Input layer, an RNN layer, and a Dense layer. You can try different numbers of RNN units, different activation functions, dropout levels, etc.  """

model=Sequential()
model.add(InputLayer((10,1))) #Input shape is (sequence_length,num_features)
model.add(SimpleRNN(15,activation='relu'))
model.add(Dense(1))

"""Now, take a look at your model. Make sure you understand the number of parameters in each layer!"""

model.summary()

"""Compile your model. What's the right loss function to use for this kind of task?"""

model.compile(optimizer=Adam(learning_rate=0.01),loss='mean_squared_error')

"""Fit your model to the training data. You should play with the number of epochs."""

model.fit(Xtrain,ytrain,batch_size=50,epochs=100)

"""Evaluate the loss on the test data. Your goal is to have created a model with a loss that is consistently under 0.05 for the test data."""

loss=model.evaluate(Xtest,ytest)
loss

"""Another way to see how good your model is would be to plot the predicted values (in red) based on each subsequence against the actual values (in blue). Run this code block to see that:"""

plt.scatter(t[11:],y)
plt.scatter(t[11:],model.predict(X),c='r')