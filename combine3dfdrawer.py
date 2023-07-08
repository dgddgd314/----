import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np 

df1 = pd.read_csv(r"C:\Users\82103\Desktop\과제연구\elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATTpertt)_1.csv")
df2 = pd.read_csv(r"C:\Users\82103\Desktop\과제연구\elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATTpertt)_2.csv")
df3 = pd.read_csv(r"C:\Users\82103\Desktop\과제연구\elevatorAlgorithm SCAN([5~50], [0.2~15.0], ATTpertt)_3.csv")
df = pd.DataFrame(columns=df1.columns, index = range(df1.shape[0]))
dfcolor = pd.DataFrame(columns=df1.columns, index = range(df1.shape[0]))
count = pd.Series([0,0,0])

for i in range (df1.shape[0]):
    for j in range (df1.shape[1]):
        data = pd.Series([df1.loc[i][j], df2.loc[i][j], df3.loc[i][j]])
        df.loc[i][j] = max(list(data))
        dfcolor.loc[i][j] = data.idxmax()

#print("df", df)
#print("dfcolor", dfcolor)

X = []
for i in range(df.shape[0]):
    for j in range(df.shape[1]-1):
        X.append(df.loc[i][0])
Y = list(df.columns.tolist()[1:]) * (df.shape[0])
Y = (list)(np.array(Y).astype(int))
Z = []
for i in range(df.shape[0]):
    for j in range(1,df.shape[1]):
        Z.append(df.loc[i][j])

color = []
for i in range(dfcolor.shape[0]):
    for j in range(1,dfcolor.shape[1]):
        color.append(dfcolor.loc[i][j])
        count[dfcolor.loc[i][j]] += 1;
"""
print(X[:10])
print(Y[:10])
print(Z[:10])
print(color[:10])
"""
fig = plt.figure()
ax = plt.axes(projection='3d')

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["skyblue","blue"])
# Create the 3D scatter plot
ax.scatter3D(X, Y, Z, c=color, cmap = cmap)

# Add labels and title
ax.set_xlabel('person/RTT')
ax.set_ylabel('MAX Floor Number')

ax.set_xlim(0,15)
ax.set_ylim(0,50)
ax.set_title('ATT/(ATT+AWT)')

# Display the plot
plt.show()

print(count)
