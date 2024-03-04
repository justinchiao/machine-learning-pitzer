# -*- coding: utf-8 -*-
"""homework5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RAPBNH-GtRxs6AeD8bypq8QpjY0b8RIa

**Homework 5**

We begin by importing a few of the usual libraries, together with NYCflights13 dataset you looked at in Homework 1.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

flights=pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/nycflights13/flights.csv")

"""We now recall the speed vs distance dataframe that you created from the NYCflights13 dataset in Homework 1. (Here done as a single chain.)"""

flights=(
    flights[['tailnum','distance','air_time']][pd.notna(flights['air_time'])].
    assign(speed=lambda x:60*x.distance/x.air_time).
    groupby('tailnum').
    agg('mean').
    sort_values('distance',ascending=False)[32:]
)

plt.scatter(flights.distance,flights.speed)
plt.xlabel('Distance')
plt.ylabel('Speed')

"""**IMPORTANT:**
DO NOT CHANGE ```flights```!! If you need to add more columns for any reason, make a copy and call it something else.
"""

flights

"""Problem 1.

Create a linear model of speed vs distance that accurately predicts the speed of the planes with the lowest and highest distances.
"""

def linear_mod1(distance):
  min=flights.sort_values(by='distance').iloc[0]
  max=flights.sort_values(by='distance').iloc[-1]
  m=(max.speed-min.speed)/(max.distance-min.distance)
  pred=m*(distance-max.distance)+max.speed
  return pred

linear_mod1(flights.distance)

"""Run this code to visualize your model's predictions, as compared to the actual:"""

plt.scatter(flights.distance,flights.speed)
plt.plot(flights.distance,linear_mod1(flights.distance),'-r')
plt.xlabel('Distance')
plt.ylabel('Speed')

"""Problem 1b.

Calculate the RSS of ```linear_mod1```.
"""

RSS1=((flights.speed-linear_mod1(flights.distance))**2).sum()
RSS1

"""Problem 2.

Create a linear model of speed vs distance that minimizes the RSS.
"""

flights.head(5)

def linear_mod2(distance):
  features=flights[['distance']].assign(inter=np.ones(flights.shape[0])).to_numpy()
  target=flights.speed.to_numpy()
  coefficients=(np.linalg.inv(features.T@features))@(features.T@target)
  pred=(coefficients[0]*features.T[0])+(coefficients[1]*features.T[1])

  return pred

linear_mod2(flights.distance)

"""Run this code to visualize your model. Does it look better?"""

plt.scatter(flights.distance,flights.speed)
plt.plot(flights.distance,linear_mod2(flights.distance),'-r')
plt.xlabel('Distance')
plt.ylabel('Speed')

"""Problem 2b.

Calculate the RSS of ```linear_mod2```.
"""

RSS2=((flights.speed-linear_mod2(flights.distance))**2).sum()
RSS2

"""How does that compare to RSS1?

Problem 3.

Create a quadratic model of speed vs distance that minimizes the RSS.
"""

def quadratic_mod(distance):
  features=flights[['distance']].assign(sqr_dist=flights.distance**2).assign(inter=np.ones(flights.shape[0])).to_numpy()
  target=flights.speed.to_numpy()
  coefficients=(np.linalg.inv(features.T@features))@(features.T@target)
  pred=(coefficients[0]*features.T[0])+(coefficients[1]*features.T[1])+(coefficients[2]*features.T[2])
  return pred

quadratic_mod(flights.distance)

"""Now visualize it:"""

plt.scatter(flights.distance,flights.speed)
plt.plot(flights.distance,quadratic_mod(flights.distance),'-r')
plt.xlabel('Distance')
plt.ylabel('Speed')

"""Problem 3b.

Calculate the RSS of ```quadratic_mod```.
"""

RSSquad=((flights.speed-quadratic_mod(flights.distance))**2).sum()
RSSquad

"""How does that compare to RSS1 and RSS2?

Problem 4.

You may have noticed from your graph that the data looks a bit more logarithmic than polynomial. Use linear regression to define a model of the form
$$speed=a\ln{(distance)}+b.$$
Then, plot your model and calculate its RSS.
"""

def log_mod(distance):
  features=flights[['distance']].assign(sqr_dist=np.log(flights.distance)).assign(inter=np.ones(flights.shape[0])).drop(columns=['distance']).to_numpy()
  target=flights.speed.to_numpy()
  coefficients=(np.linalg.inv(features.T@features))@(features.T@target)
  pred=(coefficients[0]*features.T[0])+(coefficients[1]*features.T[1])#+(coefficients[2]*features.T[2])
  return pred

plt.scatter(flights.distance,flights.speed)
plt.plot(flights.distance,log_mod(flights.distance),'-r')
plt.xlabel('Distance')
plt.ylabel('Speed')

RSSlog=((flights.speed-log_mod(flights.distance))**2).sum()
RSSlog

print(RSS1,RSS2,RSSquad,RSSlog)

"""How does that compare to the RSS values for the previous models?"""