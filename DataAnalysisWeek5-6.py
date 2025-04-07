#!/usr/bin/env python
# coding: utf-8

# In[6]:


import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.stats import poisson
from scipy.stats import norm
import time
from IPython import display

data_indoor = pd.read_csv("csv files/indy_air_data_2.csv")
data_outdoor = pd.read_csv("csv files/road_data.csv")
data_indoor  = data_indoor.iloc[30:]
data_outdoor = data_outdoor.iloc[119:]
data_indoor  = data_indoor.reset_index()
data_outdoor  = data_outdoor.reset_index()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Particles >0.3um"])
plt.plot(data_outdoor["Particles >0.3um"])
plt.ylabel('Particles >0.3um"')
plt.xlabel('Time (seconds)')
plt.show()

fig2 = plt.figure(2, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"])
plt.plot(data_outdoor["Temperature: %0.1f C"])
plt.ylabel('Temperature')
plt.xlabel('Time (seconds)')
plt.show()

mean_indoor_particle = np.mean(data_indoor["Particles >0.3um"])
mean_outdoor_particle = np.mean(data_outdoor["Particles >0.3um"])
mean_indoor_temp = np.mean(data_indoor["Temperature: %0.1f C"])
mean_outdoor_temp = np.mean(data_outdoor["Temperature: %0.1f C"])

std_indoor_particle = np.std(data_indoor["Particles >0.3um"])
std_outdoor_particle = np.std(data_outdoor["Particles >0.3um"])
std_indoor_temp = np.std(data_indoor["Temperature: %0.1f C"])
std_outdoor_temp = np.std(data_outdoor["Temperature: %0.1f C"])

x = np.linspace(0, 300, 300)
y_indoor = norm.pdf(x, loc=mean_indoor_particle, scale=std_indoor_particle)
y_outdoor = norm.pdf(x, loc=mean_outdoor_particle, scale=std_outdoor_particle)

fig3 = plt.figure(3, figsize=(10,5))
plt.hist(data_indoor["Particles >0.3um"], density=True)
plt.hist(data_outdoor["Particles >0.3um"], density=True)
plt.plot(x, y_indoor, 'r-', label="Normal (indoor)")
plt.plot(x, y_outdoor, 'g-', label="Normal (outdoor)")

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_particle, std_indoor_particle))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_particle, std_outdoor_particle))

answer1_indoor = std_indoor_particle / np.sqrt(len(data_indoor))
answer1_outdoor = std_outdoor_particle / np.sqrt(len(data_outdoor))

print(answer1_indoor)
print(answer1_outdoor)

#distributions hard to tell


fig4 = plt.figure(4, figsize=(10,5))
plt.hist(data_indoor["Temperature: %0.1f C"])
plt.hist(data_outdoor["Temperature: %0.1f C"])

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_temp, std_indoor_temp))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_temp, std_outdoor_temp))

answer2_indoor = std_indoor_temp / np.sqrt(len(data_indoor))
answer2_outdoor = std_outdoor_temp / np.sqrt(len(data_outdoor))

print(answer2_indoor)
print(answer2_outdoor)

#Indoor follows a Gaussian distribution, outdoor does not due to too many temp fluxuations


# In[22]:


fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"], data_indoor["Humidity: %0.1f %%"])
plt.ylabel('Humidity')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Humidity - Indoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_outdoor["Temperature: %0.1f C"], data_outdoor["Humidity: %0.1f %%"], color='orange')
plt.ylabel('Humidity')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Humidity - Outdoor")
plt.show()

#clearly temperature and humidity are not correlated

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"], data_indoor["Gas: %d ohm"])
plt.ylabel('Gas')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Gas - Indoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_outdoor["Temperature: %0.1f C"], data_outdoor["Gas: %d ohm"], color='orange')
plt.ylabel('Gas')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Gas - Outdoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"], data_indoor["Pressure: %0.3f hPa"])
plt.ylabel('Pressure')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Pressure - Indoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_outdoor["Temperature: %0.1f C"], data_outdoor["Pressure: %0.3f hPa"], color='orange')
plt.ylabel('Pressure')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Pressure - Outdoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"], data_indoor["Altitude = %0.2f meters"])
plt.ylabel('Altitude')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Altitude - Indoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_outdoor["Temperature: %0.1f C"], data_outdoor["Altitude = %0.2f meters"], color='orange')
plt.ylabel('Altitude')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Altitude - Outdoor")
plt.show()

#you could make an argument that indoor temperature is correlated with Gas and Altitude and inversely related to Pressure
#because outdoor temperature is not gaussian there seems to be zero correlation with anything
#the hidden variable with these graphs is time, as it is assumed the temp and humidity data points were taken at the same time (which they were)


# In[21]:


fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor["Temperature: %0.1f C"], data_indoor["Particles >2.5um"])
plt.ylabel('Particles >2.5um')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Particles - Indoor")
plt.show()

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_outdoor["Temperature: %0.1f C"], data_outdoor["Particles >2.5um"], color='orange')
plt.ylabel('Particles >2.5um')
plt.xlabel('Temperature (degrees C)')
plt.title("Temperature vs Particles - Outdoor")
plt.show()


# In[28]:


data_indoor_shared = pd.read_csv("csv files/insidedata.csv")
data_outdoor_shared = pd.read_csv("csv files/outsidedata.csv")

fig1 = plt.figure(1, figsize=(10,5))
plt.plot(data_indoor_shared["Particles > 0.3um / 0.1L air:"])
plt.plot(data_outdoor_shared["Particles > 0.3um / 0.1L air:"])
plt.ylabel('Particles >0.3um"')
plt.xlabel('Time (seconds)')
plt.show()

fig2 = plt.figure(2, figsize=(10,5))
plt.plot(data_indoor_shared["Temperature"])
plt.plot(data_outdoor_shared["Temperature"])
plt.ylabel('Temperature')
plt.xlabel('Time (seconds)')
plt.show()

mean_indoor_particle_shared = np.mean(data_indoor_shared["Particles > 0.3um / 0.1L air:"])
mean_outdoor_particle_shared = np.mean(data_outdoor_shared["Particles > 0.3um / 0.1L air:"])
mean_indoor_temp_shared = np.mean(data_indoor_shared["Temperature"])
mean_outdoor_temp_shared = np.mean(data_outdoor_shared["Temperature"])

std_indoor_particle_shared = np.std(data_indoor_shared["Particles > 0.3um / 0.1L air:"])
std_outdoor_particle_shared = np.std(data_outdoor_shared["Particles > 0.3um / 0.1L air:"])
std_indoor_temp_shared = np.std(data_indoor_shared["Temperature"])
std_outdoor_temp_shared = np.std(data_outdoor_shared["Temperature"])

x = np.linspace(0, 300, 300)
y_indoor_shared = norm.pdf(x, loc=mean_indoor_particle_shared, scale=std_indoor_particle_shared)
y_outdoor_shared = norm.pdf(x, loc=mean_outdoor_particle_shared, scale=std_outdoor_particle_shared)

fig3 = plt.figure(3, figsize=(10,5))
plt.hist(data_indoor_shared["Particles > 0.3um / 0.1L air:"], density=True)
plt.hist(data_outdoor_shared["Particles > 0.3um / 0.1L air:"], density=True)
plt.plot(x, y_indoor_shared, 'r-', label="Normal (indoor)")
plt.plot(x, y_outdoor_shared, 'g-', label="Normal (outdoor)")

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_particle_shared, std_indoor_particle_shared))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_particle_shared, std_outdoor_particle_shared))

answer1_indoor_shared = std_indoor_particle_shared / np.sqrt(len(data_indoor_shared))
answer1_outdoor_shared = std_outdoor_particle_shared / np.sqrt(len(data_outdoor_shared))

print(answer1_indoor_shared)
print(answer1_outdoor_shared)



fig4 = plt.figure(4, figsize=(10,5))
plt.hist(data_indoor_shared["Temperature"])
plt.hist(data_outdoor_shared["Temperature"])

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_temp_shared, std_indoor_temp_shared))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_temp_shared, std_outdoor_temp_shared))

answer2_indoor_shared = std_indoor_temp_shared / np.sqrt(len(data_indoor_shared))
answer2_outdoor_shared = std_outdoor_temp_shared / np.sqrt(len(data_outdoor_shared))

print(answer2_indoor_shared)
print(answer2_outdoor_shared)

#Indoor follows a Gaussian distribution, outdoor does not due to too many temp fluxuations


# In[30]:


##############THEIRS

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_particle_shared, std_indoor_particle_shared))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_particle_shared, std_outdoor_particle_shared))

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_temp_shared, std_indoor_temp_shared))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_temp_shared, std_outdoor_temp_shared))

###########OURS

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_particle, std_indoor_particle))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_particle, std_outdoor_particle))

print("Indoor: mean = {:.2f}, std = {:.2f}".format(mean_indoor_temp, std_indoor_temp))
print("Outdoor: mean = {:.2f}, std = {:.2f}".format(mean_outdoor_temp, std_outdoor_temp))

###looks similar, means that the sensors used are precise and accurate


# In[ ]:




