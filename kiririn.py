from solaris import SolarisSpreadSheet
from ninoma import NinomaSpreadSheet


def solaris_scraper():
	solaris = SolarisSpreadSheet(first_figure=1)
	solaris.iterate_figures()

def ninoma_scraper():
	ninoma = NinomaSpreadSheet(first_figure=1)
	ninoma.iterate_figures()

solaris_scraper()
ninoma_scraper()
