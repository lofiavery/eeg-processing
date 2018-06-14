"""
Created on Sun May 13 08:51:15 2018
@author: Malte Güth
"""

# The first step in pre-processing your EEG data is to import your files into MNE. For most purposes the .fif format
# has ideal compatibility, but others work fine too. In the Neuropsychology Section and COCOAN we either work with
# Biosemi or BrainProducts EEG-systems. So odds are that your data are saved in the .bdf or .eeg format. 
# The following script will help you read in your data files once at a time or all in one go. Plus, you should get a 
# grasp of what you are dealing with, because higher-order statistics, for instance, are much easier understood if you 
# know what the data you work with look like.

# First, you build the digital montage of your eeg system. That means you have to know how many channels you used, what
# labels they had and according to which basic montage they were distributed across the scalp.
# It's also possible to specifiy a path to a montage file you alreday build in the formats ‘.elc’, ‘.txt’, ‘.csd’, ‘.elp’,
# ‘.hpts’, ‘.sfp’, ‘.loc’, ‘.locs’ and ‘.eloc’ or .bvef.

# The first command we need is 'import'. Most of what you will write for your thesis is not actually newly programmed code
# in Python. For the majority of your thesis you are using packages or libraries of pre-defined functions. In order to
# utilize them in a script, you first have to import the library in a session.

# Import the basic utilities in MNE
import mne

# Create new objects or lists that will contain your montage's electrode positions, channel names, types and sampling rate.
# The latter refers to the amount of data points you recorded per second (in Herz).
# 'standard_1005' would work for the 31-channel (plus ECG) montage we have at the scanner, while 'biosemi64' is for 
# the 64-channel system used in the lab in the Department of Psychology. Choose your montage accordingly and skip 
# the other one. Notice that we are calling mne, then set a dot ('.') and add more specifications which function to use.


### MRI-compatible system at the scanner
montage = mne.channels.read_montage(kind='standard_1005')

# Write a list of channel names
channel_names = ['Fp1',	'Fp2',	'F3',	'F4',	'C3',	'C4',	'P3',	'P4',	
                 'O1',	'O2',	'F7',	'F8',	'T7',	'T8',	'P7',	'P8',	
                 'Fz',	'Cz',	'Pz',	'Oz',	'FC1',	'FC2',	'CP1',	'CP2',	
                 'FC5',	'FC6',	'CP5',	'CP6',	'TP9',	'TP10', 'POz', 'ECG']
                 
# Write a list of channel types (e.g., eeg, eog, ecg)
channel_types = ['eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg', 'eeg', 'ecg']

# Note the samlping rate of your recording (in your case most likely 5000 Hz)
sfreq = 5000

# Finally, bring it all together with MNE's function for creating custoimzed EEG info files
info_custom = mne.create_info(channel_names, sfreq, channel_types, montage)
# You also my add a short description of the data set
info_custom['description'] = 'My experiment with simultaneous EEG-fMRI'

### Lab at the Department of Psychology
montage = mne.channels.read_montage(kind='biosemi64')
            
# Write a list of channel names
channel_names = ['Fp1','AF7','AF3','F1','F3','F5','F7','FT7','FC5','FC3','FC1','C1','C3','C5','T7',
                 'TP7','CP5','CP3','CP1','P1','P3','P5','P7','P9','PO7','PO3','O1','Iz','Oz','POz',
                 'Pz','CPz','Fpz','Fp2','AF8','AF4','AFz','Fz','F2','F4','F6','F8','FT8','FC6','FC4',
                 'FC2','FCz','Cz','C2','C4','C6','T8','TP8','CP6','CP4','CP2','P2','P4',
                 'P6','P8','P10','PO8','PO4','O2','EXG1','EXG2','Stim']
                 
# Write a list of channel types (e.g., eeg, eog, ecg)
channel_types = ['eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',
                 'eog',	'eog', 'stim']
                 
# Note the samlping rate of your recording (in your case most likely 1024 Hz)
sfreq = 1024

# Finally, bring it all together with MNE's function for creating custoimzed EEG info files
info_custom = mne.create_info(channel_names, sfreq, channel_types, montage)
# You also my add a short description of the data set
info_custom['description'] = 'My experiment with 64 EEG channels plus two EOG channels'


# After having written your customized info file, you can finally read in your data. Let's start with a single file.
# Write the path to your file. In case of .eeg files, make sure you have stored the identically named .vmrk (markers) and 
# .vhdr (headers) files under the same path, since the .eeg file contains the raw values and references the other two.
data_path = './Sub1.eeg'

# ... or look for the bdf file
data_path = './Sub1.bdf'

# Read the raw EEG data. Note the naming convention you use for your triggers set in the EEG. The object 'raw' is an 
# instance of raw EEG data. The argument 'preload' enables us to directly load the file into memory and eases quick data
# manipulation. For Biosemi data files, stimulus codes are stored in an additional empty channel that only contains bits 
# 1-16. We need to know the stimulus channel and specify it while importing data, look for events with 'mne.find_events'
# when data is imported or provide event information by separately importing a customized event file. The lists of
# 'eog' and 'exclude' is a list of external channels I wrote in the config file we use in the lab. You will notice a lot of
# unnecessary empty channels that were meant for other experiments also utilizing this config file. Just ignore all but the
# first two EXG channels (EOG channels).
raw = mne.io.read_raw_edf(data_path, montage=montage, preload=True, stim_channel=-1,
                          eog=[u'EXG1', u'EXG2'] exclude=[u'EXG3', u'EXG4', u'EXG5', u'EXG6', u'EXG7', u'EXG8']) 

# Replace the mne info structure with the customized one that has the correct labels, channel types and positions.
raw.info = info_custom

# If you just type in raw.info, your IPython console will give you all the header information of your file. For instance,
# if you type 'raw.ch_names', the console returns the list of channel labels you specified earlier. Similarly you can grab
# hold of any information that is stored in raw. 
raw.ch_names

# Next, define the type of data you have provided in 'picks'
picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=True,
                       stim=True)

# Now look for events with 'mne.find_events' in your raw file's stimulus channel with the events' onsets, only including
# events that have a duration of at least .002 seconds.
events = mne.find_events(raw, output='onset', min_duration=0.002)

# ... or
events = mne.find_events(raw, stim_channel='Stim', output='onset', 
                         min_duration=0.002)

# For initial plotting, do some very basic data cleaning (filter, new reference) with a band-pass filter (high-pass=0.5 Hz
# and low-pass=30Hz). Of course, the choice of reference depends on your analyses, what you intend to study and what system
# you are using. As a new reference and a general recommendation, I suggest an average reference for the 64-channel system 
# from the lab in the Department of Psychology and a mastoid reference (TP9 and TP10) for the 32-channel system 
# from the lab in the clinic.
raw.filter(0.1, 30., n_jobs=1, fir_design='firwin') 

raw.set_eeg_reference(ref_channels=['TP9','TP10']) 

# ... or
raw.set_eeg_reference(ref_channels='average') 

# Imagine your EEG data as it was during the recording, a collection of time points by channel in microvolt. Instead of
# several colorful graphs, you now have a numpy array with rows and columns containing spatial data (electrodes) over time
# (sampling points) that can be translated into another temporal scale (miliseconds) for plotting. These spatial data
# are scattered around a head shape that was specified with coordinates from the montage you have provided. A more
# detailed description of specifically the MNE raw data structure can be found here: 
# https://martinos.org/mne/dev/auto_tutorials/plot_object_raw.html

# You can have a look at your raw data and browse through it. However, for browsing you will probably have to switch to
# the terminal and use mne_browse_raw. This will open an interactive window where you can just scroll through the raw data.
raw.plot()

# If you want to have a look at the data in raw numbers, you can extract data from raw objects. The start and stop
# arguments have to be given as samples. You can also extract time points for data samples by setting the 
# return_times argument to True.
raw.get_data(picks=picks, start=0, stop=None, return_times=False)

# If you want to save a file you have been working on, use the .save function for instances of raw or epochs. Mind
# the respective naming conventions for these file types in MNE ('-raw.fif', '-epo.fif', '-ave.fif', '-eve.fif', etc).
raw.save('Sub1-raw.fif', picks=picks, overwrite=True)
