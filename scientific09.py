# -*- coding: utf-8 -*-
"""Scientific09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A-n1gWeYnWROG9swcN8K7sOud8_6vQXZ

# ***Import Simple Essential libraries:***
"""

# Commented out IPython magic to ensure Python compatibility.
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
from scipy import optimize, stats

"""# ***Exe01:***
**2D minimization of a six-hump camelback function**

$$f(x,y) = \left(4-2.1x^2+\frac{x^4}{3} \right) x^2 +xy + (4y^2 -4)y^2$$

has multiple global and local minima.

- Find the global minima of this function
- How many global minima are there, and what is the function value at those points?
- What happens for an initial guess of $(x, y) = (0, 0)$?

Hints:

* Variables can be restricted to $-2 < x < 2$ and $-1 < y < 1$.
* Use `numpy.meshgrid()` and `pylab.imshow()` to find visually the regions.
* Use `scipy.optimize.minimize()`, optionally trying its optional arguments.
"""

#Define the function
def function(x,y): 
    return (4 - (2.1 * (x ** 2)) + (x ** 4) / 3) * (x ** 2) + x * y + (4 * (y ** 2) - 4) * (y ** 2)

fig, ax = plt.subplots(subplot_kw = {"projection": "3d"} , figsize= (10,10))
x = np.linspace(-2 , 2 , 100)
y = np.linspace(-1 , 1 , 100)
X, Y = np.meshgrid(x,y)
Output = function(X,Y)
ax.plot_surface(X , Y , Output , color = "purple")
ax.set_title("Six-Hump Camelback Function")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Output")
plt.figure()

print("We see that we have 3 global minima")

#Find the global minima
from scipy.optimize import minimize 
def f(x): 
    return (4 - (2.1 * (x[0] ** 2)) + (x[0] ** 4) / 3) * (x[0] ** 2) + x[0] * x[1] + (4* (x[1] ** 2) - 4) * (x[1] ** 2)
Result = minimize(f, (0.5, 0.75))
print("The global minima is:", Result.x)
print("The value of local minima:", f(Result.x))

#Find other global minima
#We have an initial guess based on the plot
Initial = [0, -0.7]
res = optimize.minimize(f , Initial)
Value = f(res["x"])
print("The value for initial guess:" , (res["x"], Value))

#Another guess
Initial1 = [0, 0.7]
res = optimize.minimize(f , Initial1)
Value1 = f(res["x"])
print("The value for initial guess:" , (res["x"], Value1))

#Initial Guess (0,0)
Initial2 = [0, 0]
res = optimize.minimize(f , Initial2)
Value2 = f(res["x"])
print("The value for initial guess:" , (res["x"], Value2))

"""# ***Exe02:***
**Non-linear ODE: the damped pendulum**

The equation of the motion that a pendulum makes with respect to the angle $\theta$ with the vertical is given by:

$$\frac{d^2\theta}{dt^2} = -\frac{1}{Q} \frac{d\theta}{dt} + \sin\theta + d \cos\Omega t$$

where $t$ is time, $Q$ is the damping factor, $d$ is the forcing amplitude, and $\Omega$ is the driving frequency of the forcing. 

This second order ODE needs to be written as two coupled first order ODEs defining a new variable $\omega \equiv d\theta/dt$:

$$\frac{d\theta}{dt} = \omega$$
$$\frac{d\omega}{dt} = -\frac{1}{Q}\,\omega + \sin\theta + d \cos\Omega t$$

Consider the initial conditions $\theta_0 = \omega_0 = 0$, and $Q = 2.0$, $d = 1.5$, and $\omega = 0.65$.

 - Solve the ODE with `odeint` over a pariod of 200 time steps
 - Create two plots, one of $\theta$ as a function of the time, and $\omega$ as a function of the time
 - **Optional**: determine if there is a set of parameters for which the motion is chaotic.
"""

from scipy.integrate import odeint 
def Pendulum(y , t , params):
        phi, omega = y
        Q, OMEGA , d= params
        Derivation = [omega , -1 / Q * phi + np.sin(phi) + d * np.cos(OMEGA * t)]
        return Derivation
d = 1.5
Q = 2
OMEGA = 0.65
params = [Q , OMEGA , d]
phi0 = 0
omega0 = 0
y0 = [phi0 , omega0]
t = np.linspace(0, 200, 5000)
solution = odeint(Pendulum, y0, t, args=(params,))
f, (ax1, ax2) = plt.subplots(1 , 2 , sharey = True , figsize = (20 , 6))
ax1.plot(t, solution[:, 0] , "g")
ax2.plot(t, solution[:, 1] , "r")

"""# ***Exe03:***
**FFT of a simple dataset**

Perform a periodicity analysis on the lynxs-hares population, i.e. determine what is the period of the population of these animals.

The dataset is the one dowloaded at the beginning of Lecture 06:

 - `!wget https://www.dropbox.com/s/ebe1cnyd2gm836a/populations.txt -P data/`
"""

#Get Data
!wget https://www.dropbox.com/s/ebe1cnyd2gm836a/populations.txt
df = np.loadtxt("populations.txt")

#Define the functions
from scipy import fftpack
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Peak(sample_freq, power):
    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    powes = power[pos_mask]
    peak_freq = freqs[powes.argmax()]
    return peak_freq
    
    
def Filter(sig_fft, sample_freq, peak_freq):
    high_freq_fft = sig_fft.copy()
    high_freq_fft[np.abs(sample_freq) > peak_freq] = 0
    filtered_sig = fftpack.ifft(high_freq_fft)
    real_filtered_signal = np.real(filtered_sig)
    return real_filtered_signal

#Data 
year = np.array([int(df[:,0][i]) for i in range(len(df[:,0]))])
hare = np.array([int(df[:,1][i]) for i in range(len(df[:,1]))])
lynx = np.array([int(df[:,2][i]) for i in range(len(df[:,2]))])
carrot = np.array([int(df[:,3][i]) for i in range(len(df[:,3]))])

time_step = year[2] - year[1]
hare_fft = fftpack.fft(hare)
lynx_fft = fftpack.fft(lynx)
carrot_fft = fftpack.fft(carrot)
hare_power = np.abs(hare_fft)
lynx_power = np.abs(lynx_fft)
carrot_power =np.abs(carrot_fft)
hare_freq = fftpack.fftfreq(hare.size, time_step)
lynx_freq = fftpack.fftfreq(lynx.size, time_step)
carrot_freq = fftpack.fftfreq(carrot.size, time_step)

#Plot the frequency and power of each animal
fig, ax = plt.subplots(figsize = (10 , 7))
ax.plot(hare_freq, hare_power, label = "hare" , color = "brown")
ax.plot(lynx_freq, lynx_power, label=  "lynx" , color = "black")
ax.plot(carrot_freq, carrot_power , label = "carrot" , color = "orange") 
ax.set_ylabel("power")
ax.legend()
plt.show()

#Now it is time to filter the signals
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30 , 10))

#Plotting hare
sig = hare 
real_filtered_signal = Filter(hare_fft , hare_freq , Peak(hare_freq , hare_power))
ax1.plot(year, real_filtered_signal , label = "Filtered Signal")
ax1.plot(year, sig , label = "Initial Signal" , color = "brown")
ax1.set_title("Hare filtered signal")
ax1.legend()

#Plotting lynx
sig = lynx
real_filtered_signal = Filter(lynx_fft , lynx_freq , Peak(lynx_freq , lynx_power))
ax2.plot(year, sig , label = "Initial Signal" , color = "black")
ax2.plot(year, real_filtered_signal , label = "Filtered Signal")
ax2.set_title("Lynx filtered signal")
ax2.legend()

#Plotting carrot
sig = carrot
real_filtered_signal = Filter(carrot_fft , carrot_freq , Peak(carrot_freq , carrot_power))
ax3.plot(year , sig , label= "Initial Signal" , color = "orange")
ax3.plot(year , real_filtered_signal , label = "Filtered Signal")
ax3.set_title("Carrot filtered signal")
ax3.legend()

"""# ***Exe04:***
**FFT of an image**

Write a filter that removes the periodic noise from the `moonlanding.png` image by using a 2-dimensional FFT.

* Import the image as a 2D numpy array using `plt.imread("images/moonlanding.png")`. Examine the image with `plt.imshow()`, which is heavily contaminated with periodic noise.
* Check the documentation of the `scipy.fftpack` package, and find the method that performs a 2D FFT. Plot the spectrum (Fourier transform of) the image. **Hint**: use `LogNorm` to plot the colors in log scale:
```Python
from matplotlib.colors import LogNorm
plt.imshow(image, norm=LogNorm(vmin=5))
```
* Inspect the spectrum, and try to locate the regions of the power spectrum that contain the signal and those which contain the periodic noise. Use array slicing to set the noise regions to zero.
* Apply the inverse Fourier transform to plot the resulting image.
"""

from google.colab import drive
drive.mount("/content/drive/")

#Import Libraries
from scipy.fftpack import fft2
from scipy.fftpack import ifft2
from matplotlib.colors import LogNorm
from matplotlib.pyplot import figure
import cv2 as cv

#Original pic
figure(figsize=(8, 6), dpi=100)
Picture = plt.imread("/content/drive/MyDrive/moonlanding.png")
#pic= cv.imread('/content/drive/MyDrive/moonlanding.png')
plt.imshow(Picture)
plt.show()

figure(figsize = (8, 6), dpi = 80)
pic_fft = fft2(Picture)
power = np.abs(pic_fft)

figure(figsize = (8, 6), dpi = 80)
pic_fft[power > 1000] = 0
plt.imshow(ifft2(pic_fft).real)