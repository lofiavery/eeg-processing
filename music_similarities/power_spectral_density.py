"""
Created on Sat Aug 25 14:50:05 2018

@author: Malte Gueth
"""

import mne
from mne.time_frequency import psd_multitaper

# Load epoched data segments and compute power spectral density for all genres
# as alternative input for the rsa script
file = './epochs/sub-03-reordered-epo.fif'
epochs = mne.read_epochs(file)

picks = mne.pick_types(epochs.info, eeg=True)
tmin, tmax = 0, 1 # Pick time window within each epoch
fmin, fmax = 1, 60 # Pick frequency range

# Besides frequencies, the function returns an array of 320 epochs x 64 electrodes x 59 frequencies
psds, freqs = psd_multitaper(epochs, tmin=tmin, tmax=tmax,
                             fmin=fmin, fmax=fmax, picks=picks)
                             
