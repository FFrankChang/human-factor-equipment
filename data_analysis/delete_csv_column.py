import pandas as pd

df = pd.read_csv('./data/MaBing_combined.csv')

df.drop(df.columns[1], axis=1, inplace=True)

df = df.iloc[:, :-4]
df.to_csv('./data/MaBing_combined_2.csv', index=False)
