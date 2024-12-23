import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('W_base.csv')
# # квантили для разделения данных на три части. Для низких или высоких рисков.
# # У нас очень жадный алгоритм, который боится рисков
# q1 = df['pred'].quantile(0.2)
# q2 = df['pred'].quantile(0.4)

# # Создание класса, схожего с ЗСК, но с нашей метрикой
# df['target'] = df['pred'].apply(lambda x: 0 if x < q1 else (1 if x < q2 else 2))

# порог, похожий на квантили
threshold1 = 0.17
threshold2 = 0.35
df['target'] = df['pred'].apply(lambda x: 0 if x < threshold1 else (1 if x < threshold2 else 2))


df.to_csv('targets.csv', index=False)

plt.hist(df['pred'], bins=30, edgecolor='black', alpha=0.7)

plt.axvline(threshold1, color='r', linestyle='dashed', linewidth=1)
plt.axvline(threshold2, color='r', linestyle='dashed', linewidth=1)

plt.xlabel('Данные')
plt.ylabel('Значения P(A)')
plt.title('Распределение нашей псевдо вероятности')

plt.savefig('graph_proba.png')

plt.show()
