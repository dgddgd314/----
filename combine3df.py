import pandas as pd

df1 = pd.DataFrame({'A' : [1,2,3],
                    'B' : [4,5,6],
                    'C' : [7,8,9]})
df2 = pd.DataFrame({'A' : [1,1,1],
                    'B' : [1,1,1],
                    'C' : [1,1,1]})
df3 = pd.DataFrame({'A' : [7,7,7],
                    'B' : [7,7,7],
                    'C' : [7,7,7]})
df = pd.DataFrame(0,columns=df1.columns, index = range(df1.shape[0]))
dfcolor = pd.DataFrame(0,columns=df1.columns, index = range(df1.shape[0]))

for i in range (df1.shape[0]):
    for j in range (df1.shape[1]):
        data = pd.Series([df1.loc[i][j], df2.loc[i][j], df3.loc[i][j]])
        df.loc[i][j] = data.max()
        dfcolor.loc[i][j] = data.idxmax()

print(df)
print(dfcolor)