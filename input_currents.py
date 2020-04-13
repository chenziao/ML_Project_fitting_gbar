import numpy as np

def rect(t,tstart,tstop,amp):
    """Rectangle current injection.
       Constant amplitude of amp from tstart to tstop.
       t: 1-d numpy array of timestamps of simulation steps.
    """
    I = np.zeros(t.shape)
    I[np.logical_and(t>=tstart,t<=tstop)] = amp
    return I

def ramp(t,tstart,tstop,amp_start,amp_stop):
    """Ramp current injection.
       Amplitude ramping up from amp_start at tstart to amp_stop at tstop.
       t: 1-d numpy array of timestamps of simulation steps.
    """
    I = np.zeros(t.shape)
    idx = np.logical_and(t>=tstart,t<=tstop)
    I[idx] = np.linspace(amp_start,amp_stop,idx.sum())
    return I

def zap(t,tstart,tstop,amp_start,amp_stop,fstart,fstop):
    """Zap current injection. Sinusoidally oscillating waveform, with 
       instantaneous frequency changing in time (i.e. chirp or ZAP waveform).
       Duration is from tstart to tstop.
       Amplitude changes linearly from amp_start to amp_stop over the duration.
       Frequency changes exponentially from fstart to fstop.
       t: 1-d numpy array of timestamps of simulation steps.
    """
    I = np.zeros(t.shape)
    idx = np.logical_and(t>=tstart,t<=tstop)
    n = idx.sum()
    I[idx] = np.linspace(amp_start,amp_stop,n)*np.sin(0.001*2*np.pi*np.geomspace(fstart,fstop/2,n)*(t[idx]-tstart))
    return I
