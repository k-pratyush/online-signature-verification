import pandas as pd
from statistics import mean
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv("data.csv")
del(df['Unnamed: 0'])
df.columns = ['FileName','X','Y','Pressure','Azumith','PenElevation']

#  All 5 parameters are saved into a list (colnames). All the fpg file names are saved into a list (filenames).
colnames = list(df.columns)
filenames = list(df['FileName'])

## To clean the data which are stored in the cells as strings of improper format & convert into a proper organized list 
## which can be used for time series analysis.

def clean(t):
  bad = ['.', '\n', '[',']'] 
  t = ''.join(i for i in t if not i in bad) 
  t = t.split(' ')
  t = list(filter(None, t)) 
  t = [float(i) for i in t]
  return(t)
  
df = df.set_index([colnames[0]])
for i in range(1,6):
  df[colnames[i]] = df[colnames[i]].map(clean)

UserNo =[]
SampleNo=[]
OP=[]
x_len = []
y_len = []
avg_ps = []
xy_ratio = []
pen_up =[]
DifPenEl = []
DifAz =[]
s_time = []
X_Speed = []
Y_Speed = []
for ind in df.index:
    UserNo.append(ind[:4])
    SampleNo.append(ind[5:7])
    if(ind[4] == 'f'):
        OP.append(0)
    else:
        OP.append(1) 
df['user'] = UserNo
df['sample'] =SampleNo
df['label']=OP

for i in range(5000):
    x_len.append(max(df.X[i])-min(df.X[i]))
    y_len.append(max(df.Y[i])-min(df.Y[i]))
    avg_ps.append(mean(df.Pressure[i]))
    xy_ratio.append((max(df.X[i])-min(df.X[i]))/(max(df.Y[i])-min(df.Y[i])))
    pen_up.append(df.Pressure[i].count(0))
    DifPenEl.append(len(set(df.PenElevation[i])))
    DifAz.append(len(set(df.Azumith[i])))
df['x_len'] = x_len
df['y_len'] = y_len
df['avg_ps'] = avg_ps
df['ratio'] = xy_ratio
df['dif_pen'] = DifPenEl
df['dif_az'] = DifAz
df['pen_up'] = pen_up

for i in range(5000):
    s_time.append(len(df.X[i])*(1/100))
df['sign_time'] = s_time
df.reset_index(inplace = True)

for i in range(5000):
    X_Speed.append((max(df.X[i])-min(df.X[i]))/df.sign_time[i])
    Y_Speed.append((max(df.Y[i])-min(df.Y[i]))/df.sign_time[i])
df['x_speed']=X_Speed
df['y_speed']=Y_Speed
df['x_speed']=[x/100 for x in df.x_speed]
df['y_speed']=[x/100 for x in df.y_speed]
x_size = [len(df.X[x]) for x in range(0,5000)]
df["x_size"] = x_size
#Vectorization
for i in range(0, len(df)):
    df['X'][i] = np.array(df['X'][i])
    df['Y'][i] = np.array(df['Y'][i])

W = 100
H = 100
for i in range(0, len(df)):
    df['X'][i] = ((df['X'][i] - min(df['X'][i])) / (max(df['X'][i] - min(df['X'][i])))) * W
    df['Y'][i] = ((df['Y'][i] - min(df['Y'][i])) / (max(df['Y'][i] - min(df['Y'][i])))) * H
    
def calculateDistance(x,y,xi,yi):
    return ((x - xi)**2 + (y - yi)**2)**(1/2)
temp = []
final = []
for i in range(0, len(df)):
    for j in range(0, len(df['X'][i]) - 1):
        temp.append(calculateDistance(df['X'][i][j], df['Y'][i][j], df['X'][i][j+1],[df['Y'][i][j+1]]))
    final.append(temp)
    temp = []
    print(i, ' done')
df['dist_list'] = final
for i in range(0, len(df)):
    df['dist_list'][i] = [item for sublist in final[i] for item in sublist]

# Length calculation for signatures
length_list = []
for i in range(0, len(df)):
    length_list.append(sum(df['dist_list'][i]))
df['total_length'] = length_list
df = df.loc[df.x_size > 6]
df.x_size.plot(kind = 'hist',bins = 100)
plt.xticks(rotation=90)
plt.show()

df.to_pickle("d.pkl")