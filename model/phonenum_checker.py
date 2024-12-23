from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page


async def check_tlfbase(phone_number: str) -> Optional[int]:
    response = requests.post(f"https://tlfbase.ru/phone={phone_number}")
    soup = BeautifulSoup(response.text, "html.parser")
    reliability = soup.find("div", class_="security on").get("id")
    match reliability:
        case "red_security":
            return 2
        case "yellow_security":
            return 1
        case "green_security":
            return 0
    return None


async def check_moshelovka(page: Page, phone_number: int) -> Optional[int]:
    await page.goto("https://moshelovka.onf.ru/blacklist/")

    await page.locator(".sword").fill(phone_number)
    await page.locator(".ssubmit").click()

    await page.wait_for_selector(".bl_res", state="visible")
    res_no_text_visible = page.locator(".res_no_text").is_visible()
    if not await res_no_text_visible:
        return 2
    else:
        return 1


async def check_phone_number(phone_number: str) -> Optional[Dict[str, int]]:
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            stats = (
                await check_tlfbase(phone_number),
                await check_moshelovka(page, phone_number),
            )
            return stats
        except Exception as e:
            print("Error ocurred:", e)
        finally:
            await browser.close()
