import pandas as pd

df = pd.read_csv('probs.csv')

min_pred = df['pred'].min()
max_pred = df['pred'].max()

df['pred'] = (df['pred'] - min_pred) / (max_pred - min_pred)

df.to_csv('W_base.csv', index=False)