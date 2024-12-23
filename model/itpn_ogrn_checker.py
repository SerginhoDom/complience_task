import asyncio
from typing import Tuple, Optional

import requests
from bs4 import BeautifulSoup

from .itpn_checker import get_ogrn_by_itpn


async def check_vbr(ogrn: str) -> Optional[int]:
    response = requests.post(f"https://www.vbr.ru/kontragent/?ogrn={ogrn}")
    soup = BeautifulSoup(response.text, "html.parser")
    pos_score_span = soup.find(
        "div",
        class_="ReviewsSummary_item__Z52PK ReviewsSummary_positive__6_CWl",
    ).find("span", class_="ReviewsSummary_count__3IfMB")
    neg_score_span = soup.find(
        "div",
        class_="ReviewsSummary_item__Z52PK ReviewsSummary_negative__Jdvcv",
    ).find("span", class_="ReviewsSummary_count__3IfMB")
    if pos_score_span is not None and neg_score_span is not None:
        if int(neg_score_span.contents[0]):
                return 2
        elif int(pos_score_span.contents[0]) < 10:
            return 1
        else:
            return 0
    return None


async def check_vbankcenter(ogrn: str) -> Optional[int]:
    response = requests.get(f"https://vbankcenter.ru/contragent/{ogrn}")
    soup = BeautifulSoup(response.text, "html.parser")
    score = soup.select_one(
        ".absolute.left-0.text-center.w-full.top-6.font-bold.text-white.text-3xl"
    ).contents[0]

    if score is not None:
        if int(score) < 10:
            return 2
        elif int(score) < 50:
            return 1
        else:
            return 0
    return None


async def check_itpn_ogrn(itpn: str) -> Tuple[Optional[int], Optional[int]]:
    ogrn = await get_ogrn_by_itpn(itpn)
    vbr_res = await check_vbr(ogrn)
    vbank_res = await check_vbankcenter(ogrn)
    return (int(vbr_res), int(vbank_res))


if __name__ == "__main__":
    asyncio.run(check_vbankcenter("320774600480902"))
