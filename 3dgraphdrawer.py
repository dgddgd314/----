import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np 

# Data for x-axis, y-axis, and z-axis

df = pd.read_csv(r"C:\Users\82103\Desktop\과제연구\elevatorAlgorithm SCAN([5~50], [0.2~15.0], tpmpermove).csv")

# Create the figure and axis

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

fig = plt.figure()
ax = plt.axes(projection='3d')

# Create the 3D scatter plot

ax.scatter3D(X, Y, Z, c=Z, cmap='plasma')

# Add labels and title
ax.set_xlabel('person/RTT')
ax.set_ylabel('MAX Floor Number')

ax.set_xlim(0,15)
ax.set_ylim(0,50)
ax.set_title('Average Person Riding, tick = 3')

# Display the plot
plt.show()
print(max(Z), min(Z))