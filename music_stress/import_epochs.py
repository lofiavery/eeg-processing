"""
Created on Sat Jun 30 16:58:39 2018

@author: Malte Gueth
"""

import mne

# Import raw data as brainvision with path to the .vhdr file and set up paths

# Specify the path to your raw data. Please mind that .eeg, .vhdr, and .vmrk files need
# to be stored under the same directory for this command to work.
file = '/Volumes/INTENSO/music_stress/HOAF_EDA_Resp0002.vhdr'

# Use the 'read_raw_brainvision' function implemented in MNE to import the format
# utilized during your recordings with brain vision recorder.
raw = mne.io.read_raw_brainvision(file, preload=True)

# This is probably not necessary, since you should be able to treat your two data channel as
# eeg channels, but if you like, you could build a new info file that specifies your channels
# as miscellaneous channels. If you don't do this part, MNE should read your channels
# as one misc (GSR_MR_100), one eeg (Resp) and one stim (trigger channel).

# Here, you can specify channel names, types and sampling rate to build a new info file.
ch_labels = ['GSR_MR_100', 'Resp', 'Stim']
ch_types = ['misc', 'misc', 'stim']
sfreq = 250

# Put all of them together and maybe add a short description to the set.
info = mne.create_info(ch_labels, sfreq, ch_types)
raw.info['description'] = 'Music stress experiment in the MRI scanner with EDA and a respiratory channel'
raw.info['buffer_size_sec'] = 1

# Pre-processing should not be the most vital part of this analysis. Simple filtering
# should be enough. To this end, just pick a frequency cut-off in Hz. If you set h_freq to
# 'None', you only apply a high-pass filter, so only frequencies above the set threshold are kept.
# Conversly, if you only select a higher cut-off, a low-pass filter is applied and only
# frequencies below the threshold are kept.
picks = mne.pick_types(raw.info, misc=True)
raw.filter(l_freq = None, h_freq = None, picks=picks)

# Choose the channel containing your event codes, create a numpy array (here named 'events') with three
# columns of onsets in sampling points, previous channel values (here, always 0, because with this value
# the channel is cleared after it was used) and the event's code.
events = mne.find_events(raw, stim_channel='Stim')

# The ID for each event is a dictionary assignment of strings to an integer. Of course, you have
# more events than just these, but this serves only as an example.
event_id = {'Sync': 128, 'response_or_something': 1}

# To better check the distribution of events and ID's across time, you can visualize your
# channel with 'mne.viz.plot_events'. By default it plots events over sampling points.
# To make the plot a little more straightforward, you can enter your sampling rate, which
# in turn let's the function plot events over time in seconds. You can see that 'Sync' is by
# far the most common event, as it is regularly send while you record. This event is not of any
# use to you, so you might want to name other important events of your experiment.
events_plot = mne.viz.plot_events(events, sfreq, raw.first_samp)
events_plot.savefig('./event_channel.pdf', bbox='tight')

# If you enter the following, your raw data would be epoched. Epochs would be locked to
# 'Sync' and 'response', because these are the only ones I specified in 'event_id'.
# The temporal range of epochs is determined with the 'tmin' and 'tmax' parameters in seconds.
# 'baseline' refers to a baseline correction and picks limits epoching to the channels 
# selected as 'True' in the list of logicals 'picks'. Hence, respiratory responses and
# electrodermal responses would be epoched.
epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=-1, tmax=5,
                    baseline=None, picks=picks, preload=True)
epochs.save('./music_stress-epo.fif')

# If required, you can write the data of each epoch into a numpy array with the dimensions 
# epochs, channels, and sample points.
data = epochs['response_or_something'].get_data()
