import numpy as np

def neg_inf_prob(data):
    # Можно улучшить ввод чтобы был выбор либо то либо нет
    if data != data:
        return None
    if data == 'Имеется':
        return 1
    return 0