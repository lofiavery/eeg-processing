"""
Created on Sun May 13 08:51:15 2017
@author: Malte Güth
"""

# The first step in pre-processing your EEG data is to import your files into MNE. For most purposes the .fif format
# has ideal compatibility, but others work fine too. In the Neuropsychology Section and COCOAN we either work with
# Biosemi or BrainProducts EEG-systems. So odds are that your data are saved in the .bdf or .eeg format. 
# The following script will help you read in your data files once at a time or all in one go. Plus, you should get a 
# grasp of what you are dealing with, because higher-order statistics, for instance, are much easier understood if you 
# know what the data you work with looks like.

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
s_freq = 5000

# Finally, bring it all together with MNE's function for creating custoimzed EEG info files
info_custom = mne.create_info(channel_names, s_freq, channel_types, montage)
# You also my add a short description of the data set
info_custom['description'] = 'My experiment with simultaneous EEG-fMRI'

### Lab at the Department of Psychology
montage = mne.channels.read_montage(kind='biosemi64')
            
# Write a list of channel names
channel_names = ['Fp1','AF7','AF3','F1','F3','F5','F7','FT7','FC5','FC3','FC1','C1','C3','C5','T7','TP7','CP5','CP3','CP1',
                 'P1','P3','P5','P7','P9','PO7','PO3','O1','Iz','Oz','POz','Pz','CPz','Fpz','Fp2','AF8','AF4','AFz','Fz',
                 'F2','F4','F6','F8','FT8','FC6','FC4','FC2','FCz','Cz','C2','C4','C6','T8','TP8','CP6','CP4','CP2','P2','P4',
                 'P6','P8','P10','PO8','PO4','O2','EOG_blink','EOG_sacc']
                 
# Write a list of channel types (e.g., eeg, eog, ecg)
channel_types = ['eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	
                 'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',	'eeg',
                 'eog', 'eog']
                 
# Note the samlping rate of your recording (in your case most likely 1024 Hz)
s_freq = 1024

# Finally, bring it all together with MNE's function for creating custoimzed EEG info files
info_custom = mne.create_info(channel_names, s_freq, channel_types, montage)
# You also my add a short description of the data set
info_custom['description'] = 'My experiment with 64 EEG channels plus two EOG channels'


# After having written your customized info file, you can finally read in your data. Let's start with a single file.
# Write the path to your file.
data_path = './Sub1d.bdf'

# Read the raw EEG data. Note the naming convention you use for your triggers set in the EEG. The argument 'strip_to_integer'
# will remove all symbols that are no integers. Thus, it will convert 'S17' to '17'. The object 'raw' is an instance of raw
# EEG data.
raw = mne.io.read_raw_edf(data_path, montage=montage, event_id=None, 
                          event_id_func='strip_to_integer', preload=True, 
                          verbose=None, uint16_codec=None) 

# Replace the mne info structure with the customized one that has the correct labels, channel types and positions.
raw.info = info_custom

# If you just type in raw.info, your IPython console will give you all the header information of your file.
# Imagine your EEG data as it was during the recording, a collection of time points by channel in microvolt. Instead of
# several colorful graphs, you now have a matrix with rows and columns containing spatial data (electrodes) over time
# (sampling points) that can be translated into another temporal dimension (miliseconds) for plotting. These spatial data
# are scattered around a head shape that was specified with coordinates from the montage you have provided.
