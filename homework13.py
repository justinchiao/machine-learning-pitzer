# -*- coding: utf-8 -*-
"""homework13.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GffH5aVu6_AcQreeeig1vt7y7_rjUbo2

**Homework 13**

For this assignment, we'll bring back some of the helper functions that we built throughout the semester:
"""

import numpy as np

class Scaler():
  def __init__(self,z):
    self.min=np.min(z,axis=0)
    self.max=np.max(z,axis=0)

  def scale(self,x):

    return (x-self.min)/(self.max-self.min+0.000001)

  def unscale(self,x):
    return x*(self.max-self.min+0.000001)+self.min

def OneHot(y):
  classes=np.max(y)+1
  Y=np.zeros((len(y),classes))
  i=np.arange(len(y))
  Y[i,y[i]]=1
  return Y

def MSE(pred,y):
  return np.mean((pred-y)**2)

def Accuracy(pred,y):
  '''Assumes pred is an array of probabilities, and y is a one-hot encoded target column'''
  class_preds=np.argmax(pred,axis=1) #predicted classes from probabilities
  class_target=np.argmax(y,axis=1) #target classes from OneHot encoding
  return np.mean(class_preds==class_target)

"""Our task now is to add `backprop` and `update` methods to the three classes you worked on in homework 12: `Linear()`, `Softmax()`, and `Model()`. There are no parameters to update and nothing to do with the gradients for the `Softmax` layer, so that is done for you:"""

class Softmax():
  '''Implement Softmax as final layer for prediction only'''
  def predict(self,input):
    return np.exp(input)/np.sum(np.exp(input),axis=1)[:,np.newaxis]
    #the end part [:,np.newaxis] was added just to get the shape right for later use

  def backprop(self,grad):
    #We ignore this layer in backpropogation
    return grad

  def update(self,lr):
    #Nothing to update
    pass

"""
For the `Linear` class, the `backprop` method will compute the gradient with respect to each parameter in that layer, given the gradients in the *next* layer. The method should output those gradients, for use in the *previous* layer.

The `update` method of the `Linear` class should change the weights and biases, based on previously computed gradients and some learning rate."""

class Linear():
  '''Fully connected linear layer class'''
  def __init__(self, input_size, output_size):
    np.random.seed(input_size) #control randomness! Remove for real use
    self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
    self.biases = np.zeros(output_size)

  def predict(self,input):
    self.input=input
    return self.input@self.weights+self.biases

  def backprop(self,grad):
    self.grad=grad
    return self.grad@self.weights.T

  def update(self,lr):
    wt_grad = self.input.T@self.grad
    bias_grad = np.sum(self.grad, axis=0)
    self.weights -= lr * wt_grad / len(self.input)
    self.biases -= lr * bias_grad / len(self.input)

"""Finally, add `backprop` and `update` methods to the `Model` class. The `backprop` method should pass the gradient of each layer (starting from the last) to the input of the `backprop` method for the previous layer. The `update` method should just call the `update` methods for each layer.

Note that I have also included a `train` method that is very similar to what we have seen before, to implement batch gradient descent for the network. Make sure you read and understand that code!
"""

class Model():
  def __init__(self,layerlist):
    self.layerlist=layerlist

  def add(self,layer):
    self.layerlist+=[layer]

  def predict(self,input):
    for layer in self.layerlist:
      input=layer.predict(input)
    return input

  def backprop(self,grad):
    for layer in reversed(self.layerlist): #every layer reverse order
      grad=layer.backprop(grad) #calls backprop for each layer in grad

  def update(self,lr):
    for layer in self.layerlist: #every layer in NN
            layer.update(lr) #each layer updated with lr

    #directly mods the weightd and biases-- don't need return

  def train(self,X,y,epochs,batch_size,lr,loss_fn):
    n=len(X)
    indices=np.arange(n)
    for i in range(epochs):
      np.random.seed(i)
      np.random.shuffle(indices)
      X_shuffle=X[indices]
      y_shuffle=y[indices]
      num_batches=n//batch_size
      for j in range(num_batches):
        X_batch=X_shuffle[j*batch_size:(j+1)*batch_size]
        y_batch=y_shuffle[j*batch_size:(j+1)*batch_size]
        pred=self.predict(X_batch)
        lossgrad=pred-y_batch
        #for regression, make sure shape of y_batch is (n,1)
        #for Softmax classification, make sure y_batch is OneHot encoded
        self.backprop(lossgrad)
        self.update(lr)
      if n%batch_size!=0: #Check if there is a smaller leftover batch
        X_batch=X_shuffle[num_batches*batch_size:]
        y_batch=y_shuffle[num_batches*batch_size:]
        pred=self.predict(X_batch)
        lossgrad=pred-y_batch
        self.backprop(lossgrad)
        self.update(lr)
      if i%1==0: #Change this line to update reporting more/less frequently
        print("epoch: ",i,", loss: ",loss_fn(self.predict(X),y))

"""Let's test your code on the good old iris dataset!

Run this code block to import the dataset and define the feature matrix:
"""

import pandas as pd
iris=pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv',index_col=0)

X=np.array(iris.iloc[:,:4]) #All four flower trait features

"""Next, we convert the target column (Species) to numerical values, and do a one-hot encoding:"""

flowerdict={'setosa':0,'versicolor':1,'virginica':2}
target=iris['Species'].apply(lambda x:flowerdict[x])
target=np.array(target)
y=OneHot(target)

"""Define the model:"""

NN=Model([])
NN.add(Linear(4,4))
NN.add(Linear(4,3))
NN.add(Softmax())

"""Now, if your code works, we can train the model, and report the accuracy as it improves:"""

NN.train(X,y,500,50,0.01,Accuracy)

"""Now try a regression task. First we'll import a toy dataset:"""

mtcars=pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv',index_col=0)
mtcars.head()

"""1. Make the first column (mpg) the target array, `y`. Make sure `y` is a numpy array of shape (32,1).
2.  Make the feature matrix `X` the remaining columns. Make sure `X` is a numpy array of shape (32,10)
3. Scale both X and y to obtain X_scaled and y_scaled.
4. Define a neural network called `mtNN` with two linear layers. The first layer should have 10 inputs and 10 outputs. The second layer should have 10 inputs and 1 output.
5. Train your neural network on X_scaled and y_scaled. Use 500 epochs, a batch size of 5, a learning rate of 0.01, and the `MSE` function to report loss during training.
"""

y=np.array([mtcars.reset_index().mpg]).T
X=np.array(mtcars.reset_index().drop(columns=['rownames','mpg']))

y_scaler=Scaler(y)
x_scaler=Scaler(X)
y_scaled=y_scaler.scale(y)
X_scaled=x_scaler.scale(X)


mtNN=Model([])
mtNN.add(Linear(10,10))
mtNN.add(Linear(10,1))

mtNN.train(X_scaled,y_scaled,500,5,0.01,MSE)