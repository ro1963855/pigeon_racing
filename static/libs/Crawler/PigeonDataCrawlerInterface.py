from PigeonGodOneCrawler import PigeonGodOneCrawler
from LingDungCrawler import LingDungCrawler

def getPigeonGodOneData(union, date):
	pigeonGodOneCrawler = PigeonGodOneCrawler()
	dateCollection = pigeonGodOneCrawler.getWebsitePeriodData(union, date)
	return dateCollection
	
def getLingDungData(union, date):
	lingDungCrawler = LingDungCrawler()
	dateCollection = lingDungCrawler.getWebsitePeriodData(union, date)
	return dateCollection
	
#print(getPigeonGodOneData('1606', '2017/08/10'))
#print(getLingDungData('24', '2017/8/10'))