from datetime import datetime
from typing import Any, Literal, Optional, Tuple

import pandas as pd
from pandas import DataFrame

from .config import THRESHOLDS


def get_min_max_dates(data: DataFrame) -> Tuple[Any, Any]:
    reg_date_col = "Дата регистрации"
    data[reg_date_col] = pd.to_datetime(
        data[reg_date_col], format="mixed", dayfirst=True, errors="coerce"
    )
    min_date, max_date = (data[reg_date_col].min(), data[reg_date_col].max())
    min_max = (str(min_date)[:10], str(max_date)[:10])
    return min_max


def reg_date_prob(
    input_date_str: str, min_max_dates: Tuple[Any, Any]
) -> float:
    input_date = datetime.strptime(str(input_date_str)[:10], "%Y-%m-%d").date()
    min_date, max_date = min_max_dates
    new_format = "%Y-%m-%d"
    min_date, max_date = (
        datetime.strptime(min_date, new_format).date(),
        datetime.strptime(max_date, new_format).date(),
    )

    total_days = (max_date - min_date).days
    input_days = (input_date - min_date).days
    normalized_value = input_days / total_days
    return normalized_value


def has_neg(value: str) -> float:
    if value != value:
        return None
    if value == "Имеется":
        return 1.0
    return 0.0


def check_float(number) -> Optional[float]:
    if number == number:
        return float(str(number).replace(",", "."))
    return None


def checks(value: Any) -> Optional[Any]:
    if value != value:
        return None
    return value


def hard_tax_to_prob(
    tax_value: Literal[
        "ОСН",
        "УСН 15%",
        "УСН 6%",
        "ПСН (только для ИП)",
        "АУСН",
        "НПД",
        "УСН 6% + ПСН",
        "УСН 15% + ПСН",
    ],
) -> float:
    if tax_value != tax_value:
        return None

    priority = {
        "ОСН": 0.6,
        "УСН 15%": 0.3,
        "УСН 6%": 0.2,
        "ПСН (только для ИП)": 0.2,
        "АУСН": 0.4,
        "НПД": 0.1,
        "УСН 6% + ПСН": 0.3,
        "УСН 15% + ПСН": 0.5,
    }
    return priority[tax_value]


def predict_risk(data: DataFrame, min_max_dates: Tuple[Any, Any]) -> float:
    """
    Основной подсчёт вероятностей ансаблей и передача в main
    """
    # метрика для вычисления итоговой вероятности указана в metrics.png
    res = [
        reg_date_prob(data["Дата регистрации"], min_max_dates),
        has_neg(data["Негативная информация"]),
        has_neg(data["Негатив относительно ГД"]),
        check_float(data["Мошенники"]),
        checks(data["Сервисы регистраторы"]),
        hard_tax_to_prob(data["Система налогообложения"]),
        None,  # чтобы метрика не обнуляла пользователя со всеми данными, иначе он 0% рисков
    ]

    inputs = sum(1 for x in res if x is not None)
    weights = (len(res) - inputs) / (len(res) - 1)
    filtered_data = [x for x in res if x is not None]
    total_sum = sum(filtered_data)

    metrics = total_sum * weights
    return metrics


def get_augmented_probas(data: DataFrame, save: bool = False):
    min_max_dates = get_min_max_dates(data)
    data["pred"] = data.apply(predict_risk, args=[min_max_dates], axis=1)

    phone_num_col = "Номер телефона"
    inn_col = "ИНН"
    data = data.dropna(subset=[inn_col, phone_num_col])
    data[phone_num_col] = (
        data[phone_num_col].astype(str).str.replace(".0", "", regex=False)
    )
    result_frame = data[[inn_col, phone_num_col, "pred"]]
    min_pred, max_pred = (
        result_frame["pred"].min(),
        result_frame["pred"].max(),
    )

    result_frame["pred"] = (result_frame["pred"] - min_pred) / (
        max_pred - min_pred
    )

    threshold_low, threshold_high = THRESHOLDS
    result_frame["target"] = result_frame["pred"].apply(
        lambda x: 0 if x < threshold_low else (1 if x < threshold_high else 2)
    )
    if save:
        result_frame.to_csv("./data/predicts.csv", index=False)


if __name__ == "__main__":
    base_data = pd.read_csv("./data/base_data.csv")
    get_augmented_probas(base_data, save=True)
