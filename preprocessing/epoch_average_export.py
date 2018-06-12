"""
Created on Mon Jun 11 17:00:16 2018
@author: Malte Güth
"""

# With this script you can first epoch and then average your cleaned data. Epoching in EEG refers to the process of
# selecting important events from your experiment and creating little slices of data around these events.
# In principle, you cut out the small pieces of signal that ineterst you. This example will be performed with onsets
# of different music stimuli. The data set in question contained the presentation of six second music stimuli
# of different genres.

import mne

import glob
import os

import pandas as pd
import numpy as np

output_dir = 'your output directory for epochs'
data_path = 'your path to all your pre-processed files'     
for filename in glob.glob(os.path.join(data_path, '*.fif')):
    
    # Each time the loop goes through a new iteration, 
    # add a subject integer to the data path
    data_path = '/Volumes/INTENSO/DPX_EEG_fMRI/EEG/'

    # Read the raw EEG data that has been pre-processed, create an event file and down-sample the data for easier handling.
    raw = mne.io.read_raw_fif(data_path, events=None, event_id=None, preload=True)
    events = mne.find_events(raw, stim_channel='Stim', output='onset', min_duration=0.002)
    
    # The original samling rate has to be multiple of the new lower sampling rate. For 1024 Hz choose 256 Hz
    # and for 5000 Hz sample data down to 250 Hz.
    raw.resample(256, npad="auto") 
    
    # Define the stimulus labels for epoching by assigning numbers to labels. In the MNE event structure there are 
    # three columns: onsets in samples, previous_event_id  and event_id. By providing new id's you can ease epoching.
    event_id = {'music_onset': 1, 'heavy_metal': 2, 'modern_classic': 3}
    
    # Epoch the preprocessed data with a baseline of -2000 ms and 2500 ms after the stimulus onset,
    # and save the data as fif, for later uses of unaveraged epochs. Do not perform a baseline correction at this point,
    # since you might want to use different baselines for different analyses (i.e., time-frequency analysis).
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.5, tmax=1.0)
    epochs.save(output_dir + '%d-epo.fif' % (filename))
    
    # Average epoched data over conditions and apply baseline correction for Event-Related Potentials.
    evoked_music = epochs['music_onset'].average() # Derive ERPs locked on the onset of any music stimulus.
    evoked_cueA.apply_baseline(-0.25, 0) # Apply a baseline correction with a time window of -250 ms till the event onset.
    evoked_metal = epochs['heavy_metal'].average() # Derive ERPs locked specifically to the onset of heavy 
                                                    # metal music stimuli.
    evoked_metal.apply_baseline(-0.25, 0)
    evoked_classic = epochs['modern_classic'].average() # Derive ERPs locked specifically to the onset of modern 
                                                        # classic music stimuli.
    evoked_classic.apply_baseline(-0.25, 0)
    evoked.save(output_dir + '%d-ave.fif' % (filename))
    
# For higher-level analyses it is adivsable to export data frames with your averaged or epoched data, 
# especially if you intend to perform them in a different programming environment like R.

# In this example, I want to save all epochs for music onsets, convert them to pandas data frames after loading
# and append them to a larger data frame containing all epochs from all subjects. This data frame is then saved to a .csv.

for filename in glob.glob(os.path.join(output_dir, '*epo.fif')):
    index, scaling_time = ['epoch', 'time'], 1e3
    epochs = '/%d-epo.fif' % (filename)
    current_epochs = mne.read_epochs(epochs)
    df = current_epochs['music_onset'].to_data_frame(picks=None, scalings=None, scaling_time=scaling_time, index=index)  
    df_all_epochs = df_all_epochs.append(df)

df_all_epochs.to_csv('./eeg_epochs.csv')

# You can plot averaged results with topoplots at specific time points with the following.
ts_args = dict(gfp=True, zorder='std',
               ylim =dict(eeg=[-10,10]), unit=True)
topomap_args = dict(sensors=False, vmax=8, vmin=-8, average=0.025, contours=2)
music_example = evoked.plot_joint(title=None, times=[0, .1, .2, .3, .4, .5, .6, 1.],
                       ts_args=ts_args, topomap_args=topomap_args)
music_example.savefig('./music_gfp_stim_channel.pdf', bbox_inches='tight')


