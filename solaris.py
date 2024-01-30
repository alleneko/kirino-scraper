import random
import time

import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


BUTTON = "button.btn.btn__main-content.add-js"
SHIPMENT = "div.shipment__block"

class Solaris:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.price = 0
		self.shipping = 0

	def get_page(self, url):
		self.url = "https://solarisjapan.com/products/" + url if "https://solarisjapan.com/products/" not in url.lower() else url
		self.driver.get(self.url)

	def get_buttons(self):
		buttons = self.driver.find_elements(By.CSS_SELECTOR, BUTTON)
		for button in buttons:
			if "brand new" in button.text.lower():
				self.price = button.text.split("$")[-1]
				self.format_buttons("new")
			elif "pre owned" in button.text.lower() and self.price == 0:
				self.price = button.text.split("$")[-1]
				self.format_buttons("used")
			elif "pre order" in button.text.lower() and self.price == 0:
				self.price = button.text.split("$")[-1]
				self.format_buttons("pre_order")

	def get_shipping(self):
		shipping = self.driver.find_elements(By.CSS_SELECTOR, SHIPMENT)
		for ship in shipping:
			if "express" in ship.text.lower():
				self.shipping = float(ship.text.split("$")[-1])

	def format_buttons(self, price):
		try:
			self.price = float(self.price)
		except Exception as e:
			self.price = 0

class SolarisSpreadSheet:
	def __init__(self, first_figure=1):
		self.path = "anime_figures.xlsx"
		self.book = openpyxl.load_workbook(self.path)
		self.book.active = self.book["SolarisJapan"]
		self.sheet = self.book.active
		self.last_figure = 1
		for figure in self.sheet["A"]:
			if figure.value:
				self.last_figure += 1
			else:
				break
		self.first_figure = first_figure
		self.browser = Solaris()

	def iterate_figures(self):
		for figure in range(self.first_figure, self.last_figure):
			if self.sheet["A"][figure].value:
				self.scrape_solaris(figure)
		self.book.close()

	def scrape_solaris(self, figure):
		self.browser.get_page(self.sheet["B"][figure].value)
		time.sleep(random.uniform(6, 12))
		self.browser.get_buttons()
		self.sheet["C"][figure].value = self.browser.price
		self.browser.get_shipping()
		self.sheet["F"][figure].value = self.browser.shipping
		self.book.save(self.path)
		time.sleep(random.uniform(25, 45))



