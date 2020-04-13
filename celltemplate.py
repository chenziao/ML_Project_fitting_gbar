"""
@author: ziao
"""

from neuron import h

class squidCell():
    def __init__(self, el=-60):
        self.soma = h.Section(name='soma')
        self.soma.nseg = 1
        self.soma.diam = 500 # um
        self.soma.L = 500    # um
        self.soma.cm = 1     # uF
        self.soma.insert('leak')
        self.soma.insert('na')
        self.soma.insert('k')
        self.soma.nao = 79.8
        self.soma.ki = 69.35
        self.soma.el_leak = el # mV
        self.gl = 0.0003 # leak channel S/cm2
        self.gna = 0.12  # Sodium channel S/cm2
        self.gk = 0.036  # Potassium channel S/cm2
        self.stim = h.IClamp(self.soma(0.5)) # current injection object
        self.stim.delay = 0
        self.stim.dur = h.tstop
        self.rand = h.Random() # random number generator
        self.inj = h.Vector()  # current inject vector
        self.i = h.Vector()    # current injection record
        self.i.record(self.stim._ref_i)
        self.v = h.Vector()    # membrane voltage record
        self.v.record(self.soma(0.5)._ref_v)
    
    @property
    def gl(self):
        return self.__gl
    
    @gl.setter
    def gl(self, x):
        self.__gl = x
        self.soma.glbar_leak = x
    
    @property
    def gna(self):
        return self.__gna
    
    @gna.setter
    def gna(self, x):
        self.__gna = x
        self.soma.gnabar_na = x
    
    @property
    def gk(self):
        return self.__gk
    
    @gk.setter
    def gk(self, x):
        self.__gk = x
        self.soma.gkbar_k = x
    
    def current_inject(self,I_inj,noise=0,noise_start=None,noise_stop=None):
        """Set up current injection to the cell.
           I_inj: a 1-d numpy array or a list of current injection amplitude 
                  in each time step.
           noise: standard deviation of 0-mean gaussian noise.
           noise_start,noise_stop: start and stop time of noise.
                  If not specified, set on throughout the simulation.
        """
        dt = h.dt
        self.inj.from_python(I_inj)
        if noise>0:
            self.rand.normal(0,noise**2)
            if noise_start is None: noise_start=0
            if noise_stop is None: noise_stop=h.tstop-dt
            self.inj.addrand(self.rand,noise_start/dt,noise_stop/dt)
        self.inj.play(self.stim._ref_amp,dt)
