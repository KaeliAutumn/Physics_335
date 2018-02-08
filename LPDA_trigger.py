#!/bin/python

from random import *
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

#constants
SNR = 5.0
num_events = 1000


#Effective Height Characteristics
h_eff=[]
with open('h_eff.txt') as f:
    h_eff = f.readlines()
h_eff = [x.strip() for x in h_eff]
h_eff=map(float,h_eff)

total_power=[0]*num_events
noise_power=[0]*num_events


#Impulse Characteristics
#impulse=[]
#with open('impulse.txt') as f:
#    impulse = f.readlines()
#impulse = [x.strip() for x in impulse]
#impulse = map(float,impulse)

#impulse_time=[]
#with open('impulse_time.txt') as f:
#    impulse_time = f.readlines()
#impulse_time = [x.strip() for x in impulse_time]
#impulse_time = map(float,impulse_time)

dt = 0.45
t = -13.5
mu=0.0
sigma = 0.057
impulse=[0]*len(h_eff)
for i in range(0,len(h_eff)):
    impulse[i]= 1.0/(sigma * np.sqrt(2.0 * np.pi)) * np.exp( - (t - mu)**2.0 / (2.0 * sigma**2.0))
    t=t+dt

#plt.figure(4)
#plt.plot(impulse)
noise_std=max(impulse)*dt/SNR
#print(noise_mean)

impulse_power =0
#Power sum impulse for SNR:
for x in range(0, len(impulse)):
    impulse_power=impulse_power+impulse[x]*impulse[x]*dt
print(impulse_power)

print('this is a test')
print(SNR)
print(math.pow(10.0,(SNR/10.0)))
noise_p=impulse_power/math.pow(10.0,(SNR/10.0))
#noise_std=np.sqrt(noise_p/len(impulse))
print(noise_p)
print(noise_std)
#


#loop over number of events
for k in range(1, num_events):

    #Noise Characteristics
    noise = np.random.normal(0.0,noise_std,len(impulse))

    #Create Signal
    signal=[0]*124
    for x in range(15,len(impulse)-15):
        signal[x]=impulse[x]+noise[x]

    #Convolute effective height and signal to get antenna response
    signal = np.array(signal)
    h_eff=np.array(h_eff)
    ant_response = fftconvolve(signal,h_eff,mode='full')

    #Plotting


    #plt.savefig('noise.jpg')

    #Power sum the signal
    power=[0]*len(ant_response)
    p_sum=0
    for i in range(0, len(ant_response)-1):
        power[i]=ant_response[i]*ant_response[i]
        p_sum=p_sum+power[i]*dt
    #print('sum is:')
    #print(p_sum)
    total_power[k]=p_sum

#print(total_power)

#plt.figure(1)
#plt.subplot(311)
#plt.plot(signal)
#plt.title('Impulse with noise, SNR 5')
#plt.xlabel('time (ns)')
#plt.ylabel('Signal (V)')

#plt.subplot(312)
#plt.plot(h_eff)
#plt.xlabel('h_eff for LPDA')
#plt.ylabel('h_eff (V)')

#plt.subplot(313)
#plt.plot(ant_response)



#plt.figure(2)
#plt.hist(total_power, bins=25)
#plt.xlabel('Total Power')
#plt.ylabel('Number of Entries')
#plt.title('Histogram of Power Sums, With Impulse')
#plt.savefig('powersum_impulse.jpg')


#NOW TRY NO SIGNAL

for k in range(1, num_events):

    #Noise Characteristics
#    noise_mean=max(impulse)/SNR
    noise = np.random.normal(0.0, noise_std,len(impulse))


    #Convolute effective height and signal to get antenna response
    noise = np.array(noise)
    h_eff=np.array(h_eff)
    ant_response = fftconvolve(noise,h_eff,mode='full')

    #Plotting
    #plt.figure(1)
    #plt.subplot(311)
    #plt.plot(signal)

    #plt.subplot(312)
    #plt.plot(h_eff)

    #plt.subplot(313)
    #plt.plot(ant_response)

    #plt.savefig('noise.jpg')

    #Power sum the signal
    power=[0]*len(ant_response)
    p_sum=0
    for i in range(0, len(ant_response)-1):
        power[i]=ant_response[i]*ant_response[i]
        p_sum=p_sum+power[i]*dt
    #print('sum is:')
    #print(p_sum)
    noise_power[k]=p_sum


#plt.figure(3)
#plt.hist(noise_power, bins=25)
#plt.xlabel('Total Power')
#plt.ylabel('Number of Entries')
#plt.title('Histogram of Power Sums, Noise Only')
#plt.savefig('powersum_noise.jpg')

bins=np.histogram(np.hstack((total_power,noise_power)), bins=40)[1]

plt.figure(5)
plt.hist(total_power,bins, alpha=0.5,label='impulse')
plt.hist(noise_power, bins, alpha=0.5, label='noise')
plt.legend(loc='upper right')
plt.savefig('power.jpg')
plt.show()
