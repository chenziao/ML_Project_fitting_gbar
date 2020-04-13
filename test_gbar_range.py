"""
@author: ziao
"""

import matplotlib.pyplot as plt
import numpy as np
from neuron import h
import celltemplate as ct
import input_currents as ic

el = -60 # mV
dt = 0.025 # ms
tstop = 1600 # ms
t = np.arange(0,tstop,dt)

h.load_file('stdrun.hoc')
h.v_init= el
h.tstop = tstop
h.dt = dt

cell = ct.squidCell(el=el)

t_vec = h.Vector()
t_vec.record(h._ref_t)


I_start = 200.0  # start time in ms
I_stop = 1400.0  # stop time in ms
I_amp = 50.0     # amplitude in nA
f_start = 1      # initial frequenzy in Hz
f_stop = 300     # final frequenzy in Hz
noise_amp = 10.0 # gaussian noise amplitude nA

inj_ideal = ic.zap(t,I_start,I_stop,I_amp,I_amp,f_start,f_stop)
#cell.current_inject(inj_ideal,noise=noise_amp,noise_start=I_start,noise_stop=I_stop) # noise exists in the same duration of current injection
cell.current_inject(inj_ideal,noise=noise_amp) # noise exists throughout the simulation


# Example: Run 8 cases with min/max gbar of each channel
g_n = np.array(['gl','gna','gk'])  # channel names
g_range = np.array([[0.0002,0.0004],[0.04,0.12],[0.035,0.060]]) # Lower/Upper bound for each channel
idx = np.array(np.unravel_index(np.arange(8),(2,2,2))) # index for selecting gbar
V = np.zeros([2,2,2,t.shape[0]+1]) # array to store results from 8 cases

for i in range(8):
    for j in range(3):
        setattr(cell,g_n[j],g_range[j,idx[j,i]]) # set gbar for each channel
    h.run() # run simulation
    V[tuple(list(idx[:,i])+[Ellipsis])] = cell.v.as_numpy() # store results as numpy array


LU = np.array(['L','H']) # denote lower & Upper bound.
plt.figure(figsize=(8,12))
for i in range(8):
    plt.subplot(4,2,i+1)
    plt.plot(t_vec,V[tuple(list(idx[:,i])+[Ellipsis])])
    plt.xlim(0,tstop)
    plt.title(','.join(g_n.tolist())+':'+','.join(LU[idx[:,i]].tolist()))

