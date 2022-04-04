from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


service = Service("/Users/douglasherman/Desktop/chromedriver_2")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(by="id", value="cookie")

purchase_items = driver.find_elements(by="css selector", value="#store div")
purchase_item_ids = [item.get_attribute("id") for item in purchase_items]

timeout = time.time() + 5
five_mins = time.time() + 60*5

while True:
    cookie.click()

    if time.time() > timeout:

        all_item_prices = driver.find_elements(by="css selector", value="#store b")
        item_prices = []

        # convert the <b> texts in integer prices
        for price in all_item_prices:
            # convert item price elements to strings of text
            element_text = price.text
            # if not empty string, convert info to integer number of price
            if element_text != "":
                # split the text at the -, strip the whitespace, and replace the comma with empty string
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                # append result to item prices list
                item_prices.append(cost)

        # Dictionary of store items and prices
        upgrades = {}
        for i in range(len(item_prices)):
            upgrades[item_prices[i]] = purchase_item_ids[i]

        # getting current cookie count
        money_element = driver.find_element(by="id", value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

#         finding affordable upgrades
        affordable_upgrades = {}
        # grab the cost and item id from upgrades dictionary
        for cost, id in upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # buy most expensive upgrade...
        most_expensive_upgrade = max(affordable_upgrades)
        print(most_expensive_upgrade)
        upgrade_to_purchase_id = affordable_upgrades[most_expensive_upgrade]

        driver.find_element(by="id", value=upgrade_to_purchase_id).click()

#         Add 5 more seconds to timer to buy another upgrade
        timeout = time.time() + 5

    if time.time() > five_mins:
        cookies_per_second = driver.find_element(by="id", value="cps").text
        print(cookies_per_second)
        break


