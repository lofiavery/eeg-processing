"""
Created on Mon Jun 11 21:01:45 2018
@author: Malte Güth
"""

# After pre-processing data and creating relevant epochs, this script shows how to compute single trial time-frequency
# analysis with a pre-defined wavelet. Please mind that wavelet parameters should suit your data and your analysis.
# This is merely an example of a wavelet José and I often use for our experiments.

import mne

import numpy as np
import matplotlib.pyplot as plt

# Start by loading all relevant epochs and concatenating them. Again, I will use the example of passive music listening.
path = 'path to your epochs'     
for filename in glob.glob(os.path.join(path, '*-epo.fif')):
    epochs = mne.io.read_epochs_fif(filename, events=None, event_id=None, montage=chanlocs, eog=(), verbose=None, 
                                    uint16_codec=None)
    evoked = epochs.average()
    if filename == './Sub1.fif': # At this point, I usually pick the first data set in the directory I want to load.
        list_music = []
        list_music.append(evoked) # Append the evoked responses in a list, so that you can also plot evoked
                                  # responses next to the time-frequency results.
        all_epochs = epochs
    else:
        list_music.append(evoked)
        all_epochs = mne.concatenate_epochs([all_epochs, epochs])
        
# Define wavelet parameters.

decim = 3
freqs = np.logspace(*np.log10([1, 50]), num=50)
cycles = np.logspace(np.log10(3), np.log10(10), 30)/(2*np.pi*freqs)

# Compute time-frequency results with a Morlet wavelet.
tfr_epochs = mne.time_frequency.tfr_morlet(all_epochs['music_onset', freqs, n_cycles=cycles, use_fft=True,
                                           decim=decim, average=True, return_itc=False, n_jobs=1)
epochs_power_music = tfr_epochs.data

# To check event-related changes across all electrodes, plot results as a topolplot. Be careful with baseline
# corrections, so you don't perform them twice.
tfr_epochs.plot_topo(baseline=(-1.5,-0.5), mode='logratio', font_color='k')

# Check results at a specific electrode you picked.
tfr_epochs.plot([46], baseline=(-1.5, -0.5), mode='logratio', 
                title='Total power at ' + tfr_epochs_a.ch_names[46])
