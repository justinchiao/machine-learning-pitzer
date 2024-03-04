# -*- coding: utf-8 -*-
"""homework9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zcw6MuaC4jk5Wy1dlWfEtokXRte8uR1t

**Homework 9**

We begin with the imports you will need, together with the functions defined in previous assignments.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def TrainTestSplit(X,y,p,seed=1):
  '''Splits feature matrix X and target array y into train and test sets
  p is the fraction going to train'''
  np.random.seed(seed) #controls randomness
  size=len(y)
  train_size=int(p*size)
  train_mask=np.zeros(size,dtype=bool)
  train_indices=np.random.choice(size, train_size, replace=False)
  train_mask[train_indices]=True
  test_mask=~train_mask
  X_train=X[train_mask]
  X_test=X[test_mask]
  y_train=y[train_mask]
  y_test=y[test_mask]
  return X_train,X_test,y_train,y_test

def PolyFeatures(x,d):
  X=np.zeros((len(x),d+1))
  for i in range(d+1):
    X[:,i]=x**i
  return X

def AddOnes(X):
  return np.concatenate((X,np.ones((len(X),1))),axis=1)

class Scaler:
  def __init__(self,z):
    self.min=np.min(z,axis=0)
    self.max=np.max(z,axis=0)

  def scale(self,x):
    return (x-self.min)/(self.max-self.min)

  def unscale(self,x):
    return x*(self.max-self.min)+self.min

def train(X,y,max_iter,lr):
  '''MSE minimization by Gradient Descent'''
  X=np.array(X) #Just in case X is a DataFrame
  y=np.array(y) #Just in case y is a Series
  n=len(X)
  coeff=np.ones(X.shape[1]) #Initialize all coeff to be 1 (something to play with?)
  for i in range(max_iter):
    resid=X@coeff-y
    gradient=((X.T)@resid)/n #Lot's of lin alg here. Try to unpack it!
    coeff=coeff-lr*gradient #Gradient Descent step.
  return coeff

def SGD(X,y,epochs,batch_size,lr):
  '''Stochastic Gradient Descent'''
  X=np.array(X) #Just in case X is a DataFrame
  y=np.array(y) #Just in case y is a Series
  n=len(X)
  coeff=np.ones(X.shape[1]) #Initialize all coeff to be 1 (something to play with?)
  indices=np.arange(len(X))
  for i in range(epochs):
    np.random.seed(i) #Just so everyone gets the same answer!
    np.random.shuffle(indices)
    X_shuffle=X[indices]
    y_shuffle=y[indices]
    num_batches=n//batch_size
    for j in range(num_batches):
      X_batch=X_shuffle[j*batch_size:(j+1)*batch_size]
      y_batch=y_shuffle[j*batch_size:(j+1)*batch_size]
      resid=X_batch@coeff-y_batch
      gradient=((X_batch.T)@resid)/len(X_batch) #Unpack this lin alg!
      coeff=coeff-lr*gradient #Gradient Descent step.
    if n%batch_size!=0: #Check if there is a smaller leftover batch
      X_batch=X_shuffle[num_batches*batch_size:] #last batch
      y_batch=y_shuffle[num_batches*batch_size:] #last batch
      resid=X_batch@coeff-y_batch
      gradient=((X_batch.T)@resid)/len(X_batch)
      coeff=coeff-lr*gradient
  return coeff

def predict(X,coeff): #If X was scaled, then this will return scaled predictions
  return X@coeff

def MSE(pred,y):
  return np.sum((pred-y)**2)/len(y)

"""In this assignment you will modify the SGD function to allow for L1 (Lasso) and L2 (Ridge) regularization."""

def SGD(X,y,epochs,batch_size,lr,alpha=0,beta=0):
  '''Stochastic Gradient Descent With L1 and L2 regularization'''
  #alpha=amount of L1 (Lasso) regularization
  #beta=amount of L2 (Ridge) regularization
  X=np.array(X) #Just in case X is a DataFrame
  y=np.array(y) #Just in case y is a Series
  n=len(X)
  coeff=np.ones(X.shape[1]) #Initialize all coeff to be 1 (something to play with?)
  indices=np.arange(len(X))
  for i in range(epochs):
    np.random.seed(i) #Just so everyone gets the same answer!
    np.random.shuffle(indices)
    X_shuffle=X[indices]
    y_shuffle=y[indices]
    num_batches=n//batch_size
    for j in range(num_batches):
      X_batch=X_shuffle[j*batch_size:(j+1)*batch_size]
      y_batch=y_shuffle[j*batch_size:(j+1)*batch_size]
      resid=X_batch@coeff-y_batch
      gradient=lr*((X_batch.T)@resid)/len(X_batch) + alpha*(2*(coeff>0)-1) + beta*coeff #modify this line
      coeff=coeff-gradient #Gradient Descent step.
    if n%batch_size!=0: #Check if there is a smaller leftover batch
      X_batch=X_shuffle[num_batches*batch_size:] #last batch
      y_batch=y_shuffle[num_batches*batch_size:] #last batch
      resid=X_batch@coeff-y_batch
      gradient=lr*((X_batch.T)@resid)/len(X_batch) + alpha*(2*(coeff>0)-1) + beta*coeff #modify this line
      coeff=coeff-gradient
  return coeff

"""Let's make up some data to play with:"""

np.random.seed(4)
x=np.arange(2,15)
randoms=np.random.rand(13)
y=2*x+3+10*randoms
plt.scatter(x,y)

"""Now let's do a train/test split and fit an 8th degree polynomial model to the train set via SGD."""

x_train,x_test,y_train,y_test=TrainTestSplit(x,y,0.75)
xscaler=Scaler(x_train)
yscaler=Scaler(y_train)
x_train_scaled=xscaler.scale(x_train)
X_train_scaled=PolyFeatures(x_train_scaled,8)
y_train_scaled=yscaler.scale(y_train)
coeff=SGD(X_train_scaled,y_train_scaled,100000,13,0.1)
pred_scaled=predict(X_train_scaled,coeff) #Generate predictions for the training set
pred=yscaler.unscale(pred_scaled)
MSE(pred,y_train) #MSE for the training set. Should be very low!!

"""To see the overfitting, let's run predictions on lots of values of x."""

x_plot=np.arange(2,15,.01) # 1,300 values of x between 2 and 15
x_plot_scaled=xscaler.scale(x_plot)
X_plot_scaled=PolyFeatures(x_plot_scaled,8)
plot_pred_scaled=predict(X_plot_scaled,coeff) #Generate predictions for plotting
plot_pred=yscaler.unscale(plot_pred_scaled)
plt.scatter(x_train,y_train) #plot train set
plt.scatter(x_test,y_test,color='r') #plot test set
plt.plot(x_plot,plot_pred,'-r') #plot 1300 values and their predictions, and draw smooth curve

"""Now we check the MSE for the test set. As you might expect from the overfitting, this is much higher!"""

x_test_scaled=xscaler.scale(x_test)
X_test_scaled=PolyFeatures(x_test_scaled,8)
pred_scaled=predict(X_test_scaled,coeff) #generate predictions for the test set
pred=yscaler.unscale(pred_scaled)
MSE(pred,y_test) #MSE for the test set

"""Now let's do it again and add a little L2 regularization by setting beta=0.01 in the SGD function:"""

coeff=SGD(X_train_scaled,y_train_scaled,100000,13,0.1,beta=0.01)
pred_scaled=predict(X_test_scaled,coeff) #generate predictions for the test set
pred=yscaler.unscale(pred_scaled)
MSE_with_L2=MSE(pred,y_test) #MSE for the test set
MSE_with_L2

"""If your SGD function works, the MSE should be about 5. That's much better!!

---
*Assignment*

You will now explore the classic California housing dataset. Import it here:
"""

from sklearn.datasets import fetch_california_housing
ca=fetch_california_housing(as_frame=True).frame
ca.head(3)

ca.shape

"""Our goal is to find a model which predicts the MedHouseVal variable as accurately as possible. In the process of exploring this question, we will decide which of features are most important for prediction.

To start, you'll need to create a feature matrix X containing all of the columns besides MedHouseVal, and a target vector y containing the entries in MedHouseVal.
"""

X=np.array(ca.drop(columns='MedHouseVal'))
y=np.array(ca.MedHouseVal)

y

X

"""Now, do the following:
1. 80/20 Train-Test split
2. Scale the training feature matrix and training target array.
3. Add a column of ones.
4. Find the coefficients of a linear model using SGD with 1000 epochs, batch sizes of 5000, and a learning rate of 0.01. (For now, don't use any regularization.)
"""

X.shape

#YOUR CODE HERE
X_train,X_test,y_train,y_test=TrainTestSplit(X,y,.8)

# MedInc_scaler=Scaler(X_train[:,0])
# HouseAge_scaler=Scaler(X_train[:,1])
# AveRooms_scaler=Scaler(X_train[:,2])
# AveBedrms_scaler=Scaler(X_train[:,3])
# Population_scaler=Scaler(X_train[:,4])
# AveOccup_scaler=Scaler(X_train[:,5])
# Latitude_scaler=Scaler(X_train[:,6])
# Longitude_scaler=Scaler(X_train[:,7])
# X_train_scaled=np.c_[np.array(MedInc_scaler.scale(X_train[:,0])),
#                      np.array(HouseAge_scaler.scale(X_train[:,1])),
#                      np.array(AveRooms_scaler.scale(X_train[:,2])),
#                      np.array(AveBedrms_scaler.scale(X_train[:,3])),
#                      np.array(Population_scaler.scale(X_train[:,4])),
#                      np.array(AveOccup_scaler.scale(X_train[:,5])),
#                      np.array(Latitude_scaler.scale(X_train[:,6])),
#                      np.array(Longitude_scaler.scale(X_train[:,7])),
#                      X_train[:,8]]

xscaler=Scaler(X_train)
yscaler=Scaler(y_train)
X_train_scaled=AddOnes(xscaler.scale(X_train))
y_train_scaled=yscaler.scale(y_train)
coeff=SGD(X_train_scaled,y_train_scaled,1000,5000,0.01)
coeff

"""Coefficients that are very close to zero indicate that the corresponding columns are an insignificant factor in making predictions with this model. How many coefficients are greater than -0.1 and less than 0.1?


"""

num_small_coeffs_no_regularization=0

"""Calculate the MSE for the test set."""

X_test=AddOnes(xscaler.scale(X_test))
pred=predict(X_test,coeff)
pred_unscaled=yscaler.unscale(pred)
MSE_no_reg=MSE(pred_unscaled,y_test)
MSE_no_reg

"""To refine this model more, we can use a little L1 regularization to see which columns are *really* important (feature selection). Find another set of coefficients using SGD with the same number of epochs, batch size, and learning rate, but this time include a little L1 regularization by lettting alpha=10e-5 (i.e. 0.0001)."""

coeff_with_L1=SGD(X_train_scaled,y_train_scaled,1000,5000,0.01, alpha=0.0001)
coeff_with_L1

"""Now how many coefficients are now insignificant?"""

num_small_coeffs_with_regularization=3

"""Which columns of the original ca DataFrame do these correspond to? (Ignore the added column of ones, if that turns out to be insignificant.)"""

insig_columns=ca.columns[[6,7]] #Insert indices of "insignificant" columns
insig_columns

"""Now, do the following:
1. Drop the "insignificant" columns from the ca dataframe.
2. Do a new train-test split.
3. Scale the training feature matrix and training target (you'll need to define new Scaler objects).
4. Add a column of ones, *only if you found that column to be significant for prediction!*
5. Create a linear model with the same epochs, batch size, and learning rate as before (no regularization).
6. Determine the MSE on the test set.

You should find the MSE is about the same as before, indicating that the dropped columns really were unimportant for prediction.
"""

new_X=np.array(ca.drop(columns=insig_columns).drop(columns='MedHouseVal'))

X_train,X_test,y_train,y_test=TrainTestSplit(new_X,y,.8)
xscaler=Scaler(X_train)
yscaler=Scaler(y_train)
X_train_scaled=xscaler.scale(X_train)
y_train_scaled=yscaler.scale(y_train)
coeff=SGD(X_train_scaled,y_train_scaled,1000,5000,0.01)

X_test=xscaler.scale(X_test)
pred=predict(X_test,coeff)
pred_unscaled=yscaler.unscale(pred)

new_MSE=MSE(pred_unscaled,y_test)
new_MSE