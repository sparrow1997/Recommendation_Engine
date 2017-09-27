import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split

data = pd.read_csv('../input/dataset_TSMC2014_NYC.csv')
data.head()

del data['venueId']
del data['venueCategoryId']
del data['latitude']
del data['longitude']
del data['timezoneOffset']
cont = data['venueCategory'].unique()
temp=[]
counter = 0
for c in cont:
    temp.append((c,counter))
    counter +=1
ar  = []
element = ""
for row in data['venueCategory']:
    element = row
    for word in temp:
        if word[0] == element :
            ar.append(word[1])
            
work,extra =train_test_split(data,test_size = 0.70) 
work

temp = np.array(work['utcTimestamp'])
time = []
for row in temp:
    str  = row
    t = [s for s in str.split(' ')]
    str = t[3]
    t = [s for s in str.split(':')]
    if(int(t[0])>12):
        time.append(1)
    else:
        time.append(0)
    
work['am_pm'] = time
del work['utcTimestamp']
work.reset_index(inplace =True)
del work['index']

del work['level_0']
dist = np.random.randint(50,size = work.shape[0])
work['dist'] = dist
rating = np.random.randint(10,size = work.shape[0])
work['rating'] = rating
work

data.head()