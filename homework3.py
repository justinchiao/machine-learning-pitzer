# -*- coding: utf-8 -*-
"""homework3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KP7bB37UH5-jyUY1QJ-pkxnPfc6Onaoc

**Homework 3**

This assignment is a continuation of homework 2. Make sure you complete that first!.

We begin with the usual imports.
"""

import numpy as np
import pandas as pd

"""Now load the iris dataset."""

iris=pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv",index_col=0)

"""In the code block below copy your code from homework 2 that defines the function `KNN`, together with all of the helper functions."""

"""Define `data` to be a DataFrame containing the `Petal.Length` and `Petal.Width` of the flowers in the iris dataset. Define `target` to be a Pandas Series containing the `Species` column."""

data=iris[['Petal.Length','Petal.Width']]
data =data.rename(columns={'Petal.Length':'petal_length','Petal.Width':'petal_width'})
target= iris['Species']

"""Define a function `sq_distances` with inputs `data` (a DataFrame of known Petal Lengths and Petal Widths), `length` and `width` (the Petal Length and Petal Width of an unknown flower). The function should return a Pandas series of squared distances from the unknown point to each point in `data`. Use Pandas and/or Numpy operations. DO NOT USE A FOR LOOP."""

def sq_distances(data,length,width):
  #Your code here
  data['sq_distance']=((data.petal_length-length)**2)+((data.petal_width-width)**2)
  return data.sq_distance

"""Define a function `SpeciesOfKNeighbors` that gives the Species of the k nearest neighbors from the point with given Petal Length and Petal Width to the points in `data`. (The list of species for each point in `data` is contained in the Series `target`.)"""

def SpeciesOfNeighbors(data,target,length,width,k):
  #Your code here
  sq_dist_row=sq_distances(data,length,width).sort_values(ascending=True).head(k).index
  return target[sq_dist_row]

"""Create a function `prediction` that takes a Pandas Series of labels, and returns the label that appears the most often. (Hint: The Pandas Series function `value_counts()` will be useful here."""

def prediction(labels):
  #Your code here
  return labels.value_counts().sort_values(ascending=False).index[0]

"""Create a function `KNN` which takes a DataFrame `data` of known Petal Lengths and Petal Widths, a Series `target` containing their species, a hyperparameter `k`, and the `length` and `width` of the petal of an unknown flower. Your function should return the most common species among the k nearest neighbors of the unknown flower."""

def KNN(data,target,length,width,k):
  #Your code here
  return prediction(SpeciesOfNeighbors(data,target,length,width,k))

"""The iris dataset contains 150 observations. We'd like to set aside 20% of these for testing the accuracy of our model(s). In the code block below, we create a Numpy array `test_indices` with a random sample of 20% of the numbers from 0 to 149. Then, we create a boolean Numpy array with a value of True for each index listed in `test_indices`, and False for the other values. Finally, we create a boolean Numpy array `train_mask` with the negation of each entry in `test_mask`. Spend some time examining the commands in the code block to make sure you understand them."""

np.random.seed(6) #controls randomness. Do not change!
size=len(data)  #size of original dataset (should be 150 for iris)
test_frac=0.2 #fraction of dataset to set aside for testing
test_size=int(size*test_frac) #desired size of test dataset
test_indices=np.random.choice(np.arange(size),test_size) #random sample of indices from iris
test_mask=np.zeros(size,dtype=bool) #numpy array of False values
test_mask[test_indices]=True #change values at desired indices to True
train_mask=~test_mask #True->False, False->True

"""Define `test_data` to be a DataFrame containing the `Petal.Length` and `Petal.Width` of the rows specified by `test_mask`. Define `test_target` to be a Pandas Series containing the `Species` of those rows. Define `train_data` and `train_target` similarly."""

train_data=data.loc[train_mask,['petal_length','petal_width']]
train_target=target[train_mask]
test_data=data.loc[test_mask,['petal_length','petal_width']]
test_target=target[test_mask]

"""Define a function called `predict_labels` whose inputs are `train_data`, `train_target`, `test_data` and `k`. Your function should output a Series of labels (one for each entry in `test_data`) that are predicted by your KNN function, based on the k-closest points in train_data.

*Hints.* There are many ways to do this. Here are two possibilities:
1. Use the Pandas command `apply` and a lambda function. (strongly preferred)
2. Use a "for loop", collect your answers in a list, and then convert to a Pandas Series object.
"""

def predict_labels(train_data,train_target,test_data,k):
  #Your code here
  return test_data.apply(lambda x: KNN(train_data,train_target,x.petal_length, x.petal_width,k), axis=1)
predict_labels(train_data,train_target,test_data,5)

"""Define a function called `accuracy` whose inputs are `train_data`, `train_target`, `test_data`, `test_target` and `k`. Your function should return the accuracy: the fraction of times your `predict_labels` function returned the correct answer."""

def accuracy(train_data,train_target,test_data,test_target,k):
  #Your code here
  boo=predict_labels(train_data,train_target,test_data,k)==test_target
  return (boo[boo==True].count())/boo.count()

"""Our goal is to visualize the accuracy of our KNN algorithm for various values of k, so we may pick the best one. Reasonable values of k start at 3, and may go as high as 20 (depending on the application). For each such value of k, compute the accuracy and assemble these in a 1D Numpy array."""

k_values=np.arange(3,21) #possible values for k
accuracies=np.array([accuracy(train_data,train_target,test_data,test_target,k) for k in k_values if k <= k_values[-1]])
accuracies

"""Run the following code block to visualize:"""

import matplotlib.pyplot as plt
plt.plot(k_values,accuracies)

"""The optimal value of k will be the first odd number appearing at a maximum (think about why). What is it?"""

k=9