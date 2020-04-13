"""
@author: ziao
"""

import matplotlib.pyplot as plt
import numpy as np
from neuron import h
import celltemplate as ct
import input_currents as ic

el = -60 # mV. Reversal potential of leak channel
dt = 0.025 # ms. Simulation time step size
tstop = 1600 # ms. Total simulatin time
t = np.arange(0,tstop,dt) # array of time steps

h.load_file('stdrun.hoc')
h.v_init= el # set initial membrane potential
h.tstop = tstop # how long to run the simulation in ms
h.dt = dt # time step (resolution) of the simulation in ms

# create a cell using the template and assign gbar (maximum conductance) for each channel
cell = ct.squidCell(el=el)
cell.gl = 0.0002
cell.gna = 0.12
cell.gk = 0.036

# record time steps
t_vec = h.Vector()
t_vec.record(h._ref_t)

# current injection
I_start = 200.0  # start time in ms
I_stop = 1400.0  # stop time in ms
I_amp = 50.0     # amplitude in nA
f_start = 1      # initial frequenzy in Hz
f_stop = 300     # final frequenzy in Hz
noise_amp = 10.0 # gaussian noise amplitude nA

#inj_ideal = ic.rect(t,I_start,I_stop,I_amp)
#inj_ideal = ic.ramp(t,I_start,I_stop,0,I_amp)
inj_ideal = ic.zap(t,I_start,I_stop,I_amp,I_amp,f_start,f_stop) # ideal current injection before adding noise
cell.current_inject(inj_ideal,noise=noise_amp,noise_start=I_start,noise_stop=I_stop) # with noise
#cell.current_inject(inj_ideal) # without noise

# run simulation
h.run()

# plot results
plt.figure(figsize=(8,6))
plt.subplot(311)
plt.plot(t_vec,cell.v,'b')
plt.xlim(0,tstop)
plt.legend(['Vm'])
plt.ylabel('mV')
plt.subplot(312)
plt.plot(t,inj_ideal,'m')
plt.xlim(0,tstop)
plt.legend(['desired I_inj'])
plt.ylabel('nA')
plt.subplot(313)
plt.plot(t_vec,cell.i,'r')
plt.xlim(0,tstop)
plt.legend(['actual I_inj'])
plt.xlabel('time (ms)')
plt.ylabel('nA')
plt.show()

