"""
Created on Fri Jun 29 18:40:23 2018

@author: maltegueth
"""

# Epoching of events in the EEG can be difficult. If you're only interested
# in the onset of a sensory stimulus, it's straightforward. Just pick
# the timings of the stimulus onset and you're done. In simple choice reaction
# experiments you might want to discard all epochs that contain incorrect
# responses or just a specific set of respones. In more complex cases you
# might be interested in a sequence of events you havn't thought of, while you
# were programming the experiment and, thus, did not specify a trigger code
# fot this specific event. This script demonstrates epoching for very different
# purposes, ranging from easy to complex.

# As an example, I'll be using the Dot Pattern Expectancy task used in the lab
# of the Neuropsychology Section (Marburg), in which there are always two successive
# stimuli - a cue and a probe. The cue gives an indication of what type of probe
# is going to appear with one cue being highly predictive and the other one ambiguous. 
# Depending on the fit of cue and probe (each consisting of dot patterns), 
# there are two possible responses (left and right button). Reactions have to be
# given as soon as the probe appears. So in principle there is a hint that is more
# or less helpful and a target that requires on of two different responses.

# Set up paths and load raw data
import mne

path = 'your raw data path'
file = 'sub01-raw.fif'

raw = mne.read_raw(path + file, preload=True)
picks = mne.pick_types(raw.info, eeg=True)

# Read the events from the raw data file.
events = mne.find_events(raw)

# Let's start with an easy case. Epochs locked to the cue onset are easy.
# There are only two stimuli with the names 'A' and 'B' with distinct event triggers.
# So we just have to make a dictionary with assignments of integers in the stimulus
# channel to the respective labels.
event_id = {'A': 70, 'B': 71} 

# Epoch the raw data with the event and event_id information.
epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=-0.2, tmax=1,
                    baseline=(0, None), picks=picks, preload=True)

# Now we have an interval of -200 ms and 1000 ms around the cue onsets. These
# are labelled 'A' and 'B' and can simply be accessed and worked with by writing:
epochs['A']
epochs['B']

# However, 'B' actually refers to a set of dot patterns which are all equal to
# the subject, because they don't look like 'A'. Hence, multiple codes (71-75)
# were used for 'B'. There are two ways of integrating this into your script.

# 1) You can separatly epoch the different patterns of 'B' by using '/' after an
# identical part of the label.
event_id = {'A': 70, 'B/1': 71, 'B/2': 72, 'B/3': 73, 'B/4': 74, 'B/5': 75}
epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=-0.2, tmax=1,
                    baseline=(0, None), picks=picks, preload=True)

# If you now epoch the data with these assignments, the same code can be applied
# to refer to the all epochs locked to cue 'B'.
epochs['A']
epochs['B']

# 2) The second solution utilizes mne.merge_events(). This function requires
# an mne event numpy array, a list of codes that you want to merge, and another
# code you wish to adapt for each code in the list. So if we pick all codes
# for 'B' and replace them with, for instance, 71, all 'B' epochs are 
# represented by 71.
mne.merge_events(events, [71, 72, 73, 74, 75], 71, replace_events=True)

# As described above, there are also probes in the paradigm. These elicit
# a large P3, which is sensitive to expectancy violations, because subjects 
# needed to adapt their behavior if an ambiguous cue was followed by an
# unexpected probe (Y) instead of the more frequent probe (X). There are
# four different types which should all be epoched: AX, BX, AY, and BY.
# In order to so, we need to epoch a sequence of events. An additional 
# difficulty is that 'Y' is represented the same way 'B' is. There is multiple
# codes for 'Y' (77-81).

# The most starightforward solution, in my opinion, is to re-write
# the event array with a for loop and assign new codes. This can be 
# written shorter, but for clarity's sake I'll be more detailed.
# The new assignment of event_ids shall be: {AX: 1, BX: 2, AY: 3, BY: 4}.

# Create a 1D array with all codes.
new_events = events[:,2]

# Create a intermediary variable for noting the cue code and set it to 0.
# temp_cue will be used to store information about the first stimulus
# in our sequence, which is 'A' (1) or 'B' (2).
temp_cue = 0

# Build a for loop with multiple if conditions to find the sequences. The loop should
# iterate through all elements of the event column. Then, with each iteration of the loop
# we will look through all event codes, search for a cue code, set the temp_cue to a
# specific value if a cue is found, continue by searching for the next probe, re-code the
# probe according to the value of temp_cue, set the temp_cue back to zero, and get
# to the next element in the event array.
for i in range(new_events.size):
    
    # The first if statement codes the cue. If an 'A' is found and the temp_cue is 0.
    # set the temp_cue to 1 (i.e., we found an A).
    if (new_events[i] == 70 and temp_cue == 0):
        temp_cue = 1
    # Otherwise, if any of the codes for 'B' is found and the temp_cue is 0, set the
    # temp_cue to 2.
    elif (new_events[i] == 71 and temp_cue == 0):
        temp_cue = 2
    elif (new_events[i] == 72 and temp_cue == 0):
        temp_cue = 2
    elif (new_events[i] == 73 and temp_cue == 0):
        temp_cue = 2
    elif (new_events[i] == 74 and temp_cue == 0):
        temp_cue = 2
    elif (new_events[i] == 75 and temp_cue == 0):
        temp_cue = 2
    
    # After we coded the cue-section of the sequence, we move on to the probe.
    if temp_cue == 1:
        # If the temp_cue has already been set through the first if condition, is set 1,
        # and a code for 'X' is found, change the value in row i, which corresponds to the
        # current probe value to a new value that specifically codes 'AX'.
        if new_events[i] == 76:
            new_events[i] = 1
            # Don't forget to set the temp_cue back to 0.
            temp_cue = 0
        # Now do the same for 'AY' with one statement for each code of 'Y'.
        elif new_events[i] == 77:
            new_events[i] = 3
            temp_cue = 0
        elif new_events[i] == 78:
            new_events[i] = 3
            temp_cue = 0
        elif new_events[i] == 79:
            new_events[i] = 3
            temp_cue = 0
        elif new_events[i] == 80:
            new_events[i] = 3
            temp_cue = 0
        elif new_events[i] == 81:
            new_events[i] = 3
            temp_cue = 0
    elif temp_cue == 2:
        if new_events[i] == 76:
            new_events[i] = 2
            temp_cue = 0
        elif new_events[i] == 77:
            new_events[i] = 4
            temp_cue = 0
        elif new_events[i] == 78:
            new_events[i] = 4
            temp_cue = 0
        elif new_events[i] == 79:
            new_events[i] = 4
            temp_cue = 0
        elif new_events[i] == 80:
            new_events[i] = 4
            temp_cue = 0
        elif new_events[i] == 81:
            new_events[i] = 4
            temp_cue = 0
