import os
import glob

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

import mne

# Create a classifier
clf = make_pipeline(StandardScaler(),
                    LogisticRegression(C=1, solver='lbfgs'))

# Load cleaned raw data and start epoching them as required
path = './rawdata/'  
for file in glob.glob(os.path.join(path, '*ICA-raw.fif')):

    filepath, filename = os.path.split(file)
    filename, ext = os.path.splitext(filename)
    
    raw = mne.io.read_raw_fif(file, preload=True) 
    picks = mne.pick_types(raw.info, eeg=True)
        
    events = mne.find_events(raw)
    
    # Recode genres that were sorted alphabetically to the desired integer assignments,
    # as noted in the event_id dict
    new_events = events[:,2]
    
    for i in range(new_events.size):
        
        if (new_events[i] == 1):
            new_events[i] = 1
        elif (new_events[i] == 2):
              new_events[i] = 6
        elif (new_events[i] == 3):
              new_events[i] = 7
        elif (new_events[i] == 4):
              new_events[i] = 11
        elif (new_events[i] == 5):
              new_events[i] = 12
        elif (new_events[i] == 6):
              new_events[i] = 13
        elif (new_events[i] == 7):
              new_events[i] = 16
        elif (new_events[i] == 8):
              new_events[i] = 3
        elif (new_events[i] == 9):
              new_events[i] = 17
        elif (new_events[i] == 10):
              new_events[i] = 8
        elif (new_events[i] == 11):
              new_events[i] = 5
        elif (new_events[i] == 12):
              new_events[i] = 2
        elif (new_events[i] == 13):
              new_events[i] = 18
        elif (new_events[i] == 14):
              new_events[i] = 9
        elif (new_events[i] == 15):
              new_events[i] = 19
        elif (new_events[i] == 16):
              new_events[i] = 4
        elif (new_events[i] == 17):
              new_events[i] = 10
        elif (new_events[i] == 18):
              new_events[i] = 20
        elif (new_events[i] == 19):
              new_events[i] = 14
        elif (new_events[i] == 20):
              new_events[i] = 15

    events[:,2] = new_events
    event_id = {'alternative': 1, 'punk': 2, 'heavymetal': 3,
                'rocknroll': 4, 'psychedelic': 5, 'baroque': 6,
                'classic': 7, 'modernclassic': 8, 'renaissance': 9,
                'romantic': 10, 'deephouse': 11, 'drumandbass': 12,
                'dubstep': 13, 'techno': 14, 'trance': 15, 'funk': 16,
                'hiphop': 17, 'reggae': 18, 'rnb': 19, 'soul': 20
                } 
    
    # Epoch the data with 500 ms before the music onset and 6000 ms after it
    epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=-0.5, tmax=6,
                        baseline=(-0.5, 0), picks=picks, preload=True)        
    epochs.resample(256) 
    
    # Save the epochs with re-assigned trigger codes
    epochs.save('./epochs/' + filename[:-8] + '-reordered-epo.fif')

    # Crop the epochs to time windows you want to analyze separately
    X = epochs.copy().crop(0, 0.5).get_data().mean(axis=2)
    #X = epochs.copy().crop(2, 2.5).get_data().mean(axis=2)
    #X = epochs.copy().crop(4, 4.5).get_data().mean(axis=2)

    y = epochs.events[:, 2]

    classes = set(y)
    cv = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)


    # Compute confusion matrix for each cross-validation fold
    y_pred = np.zeros((len(y), len(classes)))
    for train, test in cv.split(X, y):
        # Fit
        clf.fit(X[train], y[train])
        # Probabilistic prediction (necessary for ROC-AUC scoring metric)
        y_pred[test] = clf.predict_proba(X[test])

    confusion = np.zeros((len(classes), len(classes)))
    for ii, train_class in enumerate(classes):
        for jj in range(ii, len(classes)):
            confusion[ii, jj] = roc_auc_score(y == train_class, y_pred[:, jj])
            confusion[jj, ii] = confusion[ii, jj]
            
    # Add all confusion matrices for all subjects together and average them
    if file == './rawdata/sub-02-ICA-raw.fif':
        all_confusion = confusion
    else:
        all_confusion = np.append(all_confusion, confusion, axis=0)
        
mean_confusion = all_confusion.mean(0)
labels = {'alternative': 0, 'punk': 1, 'heavymetal': 2,
          'rocknroll': 3, 'psychedelic': 4, 'baroque': 5,
          'classic': 6, 'modernclassic': 7, 'renaissance': 8,
          'romantic': 9, 'deephouse': 10, 'drumandbass': 11,
          'dubstep': 12, 'techno': 13, 'trance': 14, 'funk': 15,
          'hiphop': 16, 'reggae': 17, 'rnb': 18, 'soul': 19
         } 

fig, ax = plt.subplots(1)
im = ax.matshow(mean_confusion, cmap='RdBu_r', clim=[0.3, 0.7])
ax.set_yticks(range(len(classes)))
ax.set_yticklabels(labels)
ax.set_xticks(range(len(classes)))
ax.set_xticklabels(labels, rotation=70, ha='left')
plt.colorbar(im)
plt.tight_layout()
plt.show()
