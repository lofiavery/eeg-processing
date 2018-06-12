"""
Created on Mon Jun 11 15:23:02 2018
@author: Malte Güth
"""

# This script performs basic steps of data cleaning in EEG including filtering, re-referencing and ICA. The script is
# separated in two parts. In the first, each step is performed on an individual subject level and the second shows how
# to design pre-preprocessing more efficiently by looping through multiple subjects.
# Note that the data import is dealt with in the data_import.py script. In this script, I presume that you have already
# read the instructions from this file.

import mne
from mne.preprocessing import ICA

# Read the raw EEG data. I'm excluding the EOG, as this type of data cleaning does not necessitate EOG channels
# I'm outlining this approach, as it is more flexible and works for both labs.
data_path='./Sub1.bdf'
raw = mne.io.read_raw_edf(data_path, montage=chanlocs, preload=True, stim_channel=-1,
                          exclude=[u'EXG1', u'EXG2', u'EXG3', u'EXG4', u'EXG5', u'EXG6', u'EXG7', u'EXG8']) 

picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False,
                       stim=True)

# Filter and rereference the data to reduce noise and remove artefact frequencies
raw.filter(0.5, 30., n_jobs=1, fir_design='firwin') 
raw.set_eeg_reference(ref_channels='average', projection=False) 

# With just filtering and rereferencing the signal to a better offline reference data are not free from artefacts.
# In order to perform fine-tuning for your EEG data and remove the tougher artefacts, we utilize Independent Component
# Analysis (ICA). For a detailed explanation of what ICA is and how it works, please see the recommended lietarture
# José or me provided. In short, ICA is like a factor analysis for your data. It assumes that there are underlying sources
# to your continuous mixed signal, causing signal variation. In other words, currents at the scalp are created by neuronal
# sources and mix according to an unknwon mixing process in the EEG, which is why oscillating signals are recorded as 
# summed potentials at each electrode. With ICA, the continuous signal is unmixed into likely signal components.
# Each components represents a signal contribution to the continuous signal, has its own frequency spectrum, scalp
# distributions, underlying dipoles and distribution across time. Hence, we can identify those signal components likely
# reflecting event-related data and artefacts (i.e., muscle or eye movement).

# First, we specify ICA parameters.
# In unmixing the signal, we have to specify how many components we want to extract for the signal decomposition.
# Note that ICA is a type of signal reduction. We have several thousand data points over n electrodes and reduce them 
# to a decompositon of latent factors (components). It is not advisable/possible to draw more components than electrodes,
# since these are our original dimensions. Thus, decomposing the signal into, for instance, 64 components with 64 electrodes
# would result in rank defficiency in your data. Furthermore, components are decomposed in accordance to their contribution
# to the overall variance in the data. Each new component accounts for a smaller portion of the data.
n_components = 25 

# The first couple of components will very likely reflect eye movement. These are very distinct, as eye movements create
# consistent signal changes in form of large amplitudes at slow frequency. Consistent signal sources are moreeasily identified.
# 25 components are enough for you to find the relevant sources you want to exclude when back-projecting the unmixed data to
# continuous data.

# Next, you have to specify the ICA algorithm you wish to use. Without going any deeper into differences between algorithms,
# I recommend you choose the 'extended-infomax' algorithm implemented in MNE for (in my experience) very robust results.
method = 'extended-infomax'

# Finally, you can pick a decimation rate for your ICA. This basically entails that you can save time by reducing
# computational effort and precision of the results by only selecting each nth time slice of data. 'decim' represents the
# utilized increment. Please be careful, because higher increments save time but decrease the derived statistics' accuracy.
decim = 3 

# Additionally, you can specify data rejection parameters with the 'reject' argument to avoid the distortion 
# of ica components by large artifacts (i.e., upper body movement, slight head shaking). For EEG, reject has to be
# something along the lines of dict(eeg=100e-6) depending on your threshold of amplitude distortion.
reject = None

ica = ICA(n_components=n_components, method=method)
ica.fit(raw, picks=picks, decim=decim, reject=reject)

# You can now plot ICA component topographies to get an idea of the decomposition.
ica.plot_components()
# This function will give you a list of components, but not their distinct properties. To plot frequency power across
# the sepctrum and other characteristics of a component, use the command below with picks as a list fo component numbers.
ica.plot_properties(raw, picks=[])

# In order to remove components, you have to specify component numbers when back-projecting the decomposition
# to a continuous raw signal. Then, the specified components' signal contribution will be excluded from the data.
ica.apply(raw, exclude=[])


# For the second part, the type of loop you build to read data and save it, depends on your creativity and how your naming
# convention for data sets looks like. Here are two examples that work fine for me.

# With N=13 participants named 'Sub' + their numerical index, this loop will successively perform the pre-processing 
# until ICA and save ICA decompositons.
for x in range(1, 14):
    
    # Each time the loop goes through a new iteration, 
    # add a subject integer to the data path.
    data_path = './Sub%d.set' % (x) 
    
    # Read the raw EEG data.
    raw = mne.io.read_raw_edf(data_path, montage=montage, preload=True, stim_channel=-1,
                              eog=[u'EXG1', u'EXG2'] exclude=[u'EXG3', u'EXG4', u'EXG5', u'EXG6', u'EXG7', u'EXG8']) 
    picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=True, stim=True)
    raw.filter(0.5, 30., n_jobs=1, fir_design='firwin') 
    raw.set_eeg_reference(ref_channels='average') 
    ica.fit(raw, picks=picks, decim=decim, reject=reject)
    ica.save('./Sub%d-ica.fif.gz' % (x))
    
    
# ... perhaps even easier is this version with glob and os, as it simply reads all files under the given path
# with a specified suffix in the filename.

import glob
import os

data_path = 'your path to all your raw files'     
for filename in glob.glob(os.path.join(data_path, '*.bdf')):
    raw = mne.io.read_raw_edf(data_path, montage=montage, preload=True, stim_channel=-1,
                              eog=[u'EXG1', u'EXG2'] exclude=[u'EXG3', u'EXG4', u'EXG5', u'EXG6', u'EXG7', u'EXG8']) 
    picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=True, stim=True)
    raw.filter(0.5, 30., n_jobs=1, fir_design='firwin') 
    raw.set_eeg_reference(ref_channels='average') 
    ica.fit(raw, picks=picks, decim=decim, reject=reject)
    ica.save('./%d-ica.fif.gz' % (filename))
    
# Concerning ICA component rejection, I will upload further scripts showing an advanced method of identifying 
# artefact components. For a start, I recommend that you do this manually by checking the component properties of
# each subject yourself. This is also very useful in learning more about how EEG signal is composed and what
# to expect from artefact and event-related signal.
