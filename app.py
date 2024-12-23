import asyncio
import streamlit as st
import pandas as pd

from xmas_hack.phonenum_checker import check_phone_number
from xmas_hack.itpn_ogrn_checker import check_itpn_ogrn


def render_color_boxes(colors: tuple[str, str, str]):
    good, norm, bad = st.columns(3)
    with good:
        st.write(
            f"""
            <div style="background-color: {colors[0]}; padding: 10px; border: px green; border-radius: 5px;">
                <h3 style="color: black;">Тип риска 0</h3>
                <p>Низкий уровень риска</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Fill the second column with yellow background and border
    with norm:
        st.write(
            f"""
            <div style="background-color: {colors[1]}; padding: 10px; border: 2px yellow; border-radius: 5px;">
                <h3 style="color: black;">Тип риска 1</h3>
                <p>Средний уровень риска</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Fill the third column with red background and border
    with bad:
        st.write(
            f"""
            <div style="background-color: {colors[2]}; padding: 10px; border: 2px red; border-radius: 5px;">
                <h3 style="color: black;">Тип риска 2</h3>
                <p>Высокий уровень риска</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    return ()


predicts = pd.read_csv("./data/predicts.csv")

st.write("# Комплаенс-система для Банка")

st.sidebar.write("## Данные клиента")
phone_number = (
    st.sidebar.text_input("Номер телефона", placeholder="71234567890") or None
)
itpn_slash_ogrn = st.sidebar.text_input("ИНН/ОГРН/ОГРНИП") or None

data = pd.DataFrame(
    {
        "Номер телефона": [phone_number],
        "ИНН/ОГРН/ОГРНИП": [itpn_slash_ogrn],
    }
)

st.write("## Краткий профайлинг прогноза")

with st.container(border=True):
    predicts["pred_rounded"] = predicts["pred"].round(1)
    pred_distribution = predicts["pred_rounded"].value_counts()
    st.bar_chart(
        pred_distribution,
        x_label="Спрогнозированное значение",
        y_label="Кол-во точек данных со значением",
        use_container_width=True,
    )

prediction_value = None
with st.sidebar:
    predict_button = st.sidebar.button("Предсказать риск", type="primary")
    if predict_button and (phone_number is None and itpn_slash_ogrn is None):
        st.sidebar.error("Недостаточно данных")
    elif phone_number is not None and itpn_slash_ogrn is None:
        prediction_value = (
            sum(asyncio.run(check_phone_number(phone_number))) // 2
        )
        st.sidebar.success(f"Уровень риска: {prediction_value}")
    elif phone_number is None and itpn_slash_ogrn is not None:
        prediction_value = (
            sum(asyncio.run(check_itpn_ogrn(itpn_slash_ogrn))) // 2
        )
        st.sidebar.success(f"Уровень риска: {prediction_value}")
    elif predict_button and (
        phone_number is not None and itpn_slash_ogrn is not None
    ):
        prediction_value = predicts[
            (predicts["Номер телефона"] == int(phone_number))
            & (predicts["ИНН"] == int(itpn_slash_ogrn))
        ]["target"].to_list()[0]
        st.sidebar.success(f"Уровень риска: {prediction_value}")


if "prediction_value" in locals():
    st.write("## Метка по уровню риска")

    match prediction_value:
        case 0:
            render_color_boxes(("#00FF00", "#bab560", "#FF4B4B"))
        case 1:
            render_color_boxes(("#2A4A3C", "#FFFF00", "#FF4B4B"))
        case 2:
            render_color_boxes(("#2A4A3C", "#bab560", "#EB0404"))

    st.write(f"Уровень риска: {prediction_value}")
