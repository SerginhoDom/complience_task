import pandas as pd
from model import predict_risk

data = pd.read_csv('data/base_data.csv')

data['pred'] = data.apply(predict_risk, axis=1)

# Удаление NaN
data = data.dropna(subset=["ИНН", "Номер телефона"])

data["Номер телефона"] = data["Номер телефона"].astype(str).str.replace('.0', '', regex=False)

result_df = data[["ИНН", "Номер телефона", "pred"]]

result_df.to_csv('probs.csv', index=False)
