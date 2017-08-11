#coding=utf-8

from PigeonDataCrawler import PigeonDataCrawler
import requests
import sys
import json
import math
from bs4 import BeautifulSoup

class PigeonGodOneCrawler(PigeonDataCrawler):
	websiteLink = 'http://www.topigeon.com.tw/qry_sms_list.asp'
	outputFileName = 'PigeonGodOneCrawlerFile.html'
	encodeType = 'BIG5'
	showColumn = 1000
	ensure_ascii = True
	
	def __init__(self):
		super(PigeonGodOneCrawler, self).__init__(self.websiteLink, self.outputFileName, self.encodeType, self.showColumn, self.ensure_ascii)

	def getHtmlContent(self, union, date):
		params = {'s1': union, 's2': date, 's5': self.showColumn}
		requestsCookieJar = requests.cookies.RequestsCookieJar()
		requestsCookieJar.set('qry_sms_list_sysid', union, domain='www.topigeon.com.tw', path='/')
		res = requests.get(self.websiteLink, params=params, cookies=requestsCookieJar)
		htmlContent = res.text
		
		finalPage = self.getCurrentPage(res.text, self.showColumn)
		currentPage = 2
		while (currentPage <= finalPage):
		   params['Page'] = str(currentPage)
		   res = requests.get(self.websiteLink, params=params, cookies=requestsCookieJar)
		   htmlContent += res.text
		   currentPage += 1
		
		return htmlContent;
		
	def getCurrentPage(self, htmlContent, showColumn):
		soup = BeautifulSoup(htmlContent, 'html.parser')
		totalPigeonNum = soup.select("font:nth-of-type(7)")[0].get_text()
		return int(math.ceil(float(totalPigeonNum)/showColumn))	
		
	def getDataCollectionByDate(self, res, date, showColumn):
		htmlContent = res.encode("utf-8")
		dateCollection = {}
		soup = BeautifulSoup(htmlContent, 'html.parser')
		for tr in soup.find_all('tr', attrs={"id": "TableTitleLink"}):
			count = 1
			collection = {}
			groupKey = {'date': date}
			for td in tr.find_all('td', limit=7):
				content = td.get_text()
				if count == 1:
					collection.update({'totalRank': content})
				elif count == 2:
					collection.update({'selfRank': content})
				elif count == 3:
					groupKey.update({'pigeonryID': content})
				elif count == 4:
					groupKey.update({'pigeonID': content})
				elif count == 5:
					collection.update({'arriveTime': content})
				elif count == 6:
					collection.update({'eastLongitude': content})
				elif count == 7:
					collection.update({'northLatitude': content})

				count = count + 1
				
			dateCollection = super(PigeonGodOneCrawler, self).pushIntoDateCollection(dateCollection, collection, groupKey)
		
		return dateCollection;
