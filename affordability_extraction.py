from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import re

def get_products_from_category_selenium(category_url, headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(category_url)
    time.sleep(5)  # wait for JS to load

    products = []
    # Find product cards
    # Inspect: product cards may be divs with “ADD” or buttons
    cards = driver.find_elements(By.XPATH, "//div[contains(., 'ADD')]")
    for card in cards:
        text = card.text
        # name
        # Maybe first line or near top
        lines = text.split("\n")
        name = lines[0].strip()
        quantity = None
        # search quantity in the lines
        for ln in lines:
            m = re.search(r"(\d+(\.\d+)?)\s*(g|kg|ml|l|gm)", ln, re.IGNORECASE)
            if m:
                quantity = m.group(0)
                break
        price = None
        for ln in lines:
            if "₹" in ln:
                p = re.search(r"₹\s*([\d,]+(\.\d+)?)", ln)
                if p:
                    price = p.group(1).replace(",", "")
                    try:
                        price = float(price)
                    except:
                        price = None
                    break
        if name and price is not None:
            products.append({"name": name, "quantity": quantity, "price": price, "url": category_url})

    driver.quit()
    return products

if __name__ == "__main__":
    categories = [
        "https://blinkit.com/cn/baking-ingredients/cid/888/971",
        "https://blinkit.com/cn/spices/cid/175/xxx",  # replace with actual
        # etc
    ]
    all_products = []
    for cat in categories:
        prods = get_products_from_category_selenium(cat)
        print(f"{len(prods)} items from {cat}")
        all_products.extend(prods)
        time.sleep(3)
    # write to CSV like above
