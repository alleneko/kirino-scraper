from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

BUTTON = "button.btn.btn__main-content.add-js"
SHIPMENT = "div.shipment__block"

class Solaris:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.prices = {
			"new": 0,
			"used": 0,
			"pre_order": 0
		}

	def get_page(self, url):
		self.url = "https://solarisjapan.com/products/" + url if "https://solarisjapan.com/products/" not in url.lower() else url
		self.driver.get(self.url)

	def get_buttons(self):
		buttons = self.driver.find_elements(By.CSS_SELECTOR, BUTTON)
		for button in buttons:
			if "brand new" in button.text.lower():
				self.prices["new"] = button.text.split("$")[-1]
				self.format_buttons("new")
			elif "pre owned" in button.text.lower():
				self.prices["used"] = button.text.split("$")[-1]
				self.format_buttons("used")
			elif "pre order" in button.text.lower():
				self.prices["pre_order"] = button.text.split("$")[-1]
				self.format_buttons("pre_order")

	def get_shipping(self):
		shipping = self.driver.find_elements(By.CSS_SELECTOR, SHIPMENT)
		for ship in shipping:
			if "express" in ship.text.lower():
				self.shipping = float(ship.text.split("$")[-1])

	def format_buttons(self, price):
		try:
			self.prices[price] = float(self.prices[price])
		except Exception as e:
			self.prices[price] = 0

