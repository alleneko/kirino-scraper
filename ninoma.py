import random
import time

import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Ninoma:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.price = 0

	def get_page(self, url):
		self.url = "https://ninoma.com/products/" + url if "https://ninoma.com/products/" not in url.lower() else url
		self.driver.get(self.url)

	def switch_currency(self):
		switcher = self.driver.find_element(By.CSS_SELECTOR, ".doubly-nice-select.currency-switcher.right")
		switcher.click()
		time.sleep(2)

		currency = self.driver.find_element("xpath", '//*[@data-value="USD"]')
		currency.click()

	def get_price(self):
		price = self.driver.find_element(By.CSS_SELECTOR, ".price__current ").text
		stripper = price.strip()
		get_rid_of_usd = stripper.split(" ")[0]

		add_to_cart = self.driver.find_element(By.CSS_SELECTOR, "span.atc-button--text").text

		self.price = float(get_rid_of_usd.replace("$", ""))  if "add to cart" in add_to_cart.lower() else 0
		print(self.price)

class NinomaSpreadSheet:
	def __init__(self, first_figure=1):
		self.path = "anime_figures.xlsx"
		self.book = openpyxl.load_workbook(self.path)
		self.book.active = self.book["Ninoma"]
		self.sheet = self.book.active
		self.last_figure = 1
		for figure in self.sheet["A"]:
			if figure.value:
				self.last_figure += 1
			else:
				break
		self.first_figure = first_figure
		self.browser = Ninoma()

	def iterate_figures(self):
		for figure in range(self.first_figure, self.last_figure):
			if self.sheet["A"][figure].value:
				self.scrape_ninoma(figure)
			else:
				break
		self.book.close()

	def scrape_ninoma(self, figure):
		self.browser.get_page(self.sheet["B"][figure].value)
		time.sleep(random.uniform(5, 12))
		self.browser.switch_currency()
		time.sleep(random.uniform(1, 3))
		self.browser.get_price()
		self.sheet["C"][figure].value = self.browser.price
		self.sheet["D"][figure].value = 60
		self.book.save(self.path)
		time.sleep(random.uniform(25, 45))


# url = "akaza-akari-kyun-chara-yuru-yuri-banpresto-41593"

# ninoma = Ninoma()
# ninoma.get_page(url)
# sleep(5)
# ninoma.switch_currency()
# sleep(2)
# ninoma.get_price()

# sleep(20)