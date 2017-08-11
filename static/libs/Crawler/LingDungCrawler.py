#coding=utf-8

from PigeonDataCrawler import PigeonDataCrawler
import requests
import sys
import json
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LingDungCrawler(PigeonDataCrawler):
	websiteLink = 'http://61.219.217.105/msg/message_results_fast.asp'
	outputFileName = 'LingDungCrawlerFile.html'
	encodeType = 'BIG5'
	showColumn = 1500
	ensure_ascii = False
	
	def __init__(self):
		super(LingDungCrawler, self).__init__(self.websiteLink, self.outputFileName, self.encodeType, self.showColumn, self.ensure_ascii)

	def getHtmlContent(self, union, date):
		driver = webdriver.Chrome(executable_path=r'C:\Python27\Scripts\chromedriver.exe')
		completeWebsiteLink = self.websiteLink + '?Udate=' + date + '&Ucgp=' + union
		driver.get(completeWebsiteLink)
		driver.add_cookie({
		  'domain': '61.219.217.105',
		  'name': 'MessageUcgp',
		  'value': union,
		  'path': '/msg',
		  'expires': None
		})
		
		driver.add_cookie({
		  'domain': '61.219.217.105',
		  'name': 'mPageS',
		  'value': self.showColumn,
		  'path': '/msg',
		  'expires': None
		})
		
		driver.get(completeWebsiteLink)
		
		driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))		
		driver.get(completeWebsiteLink)
		res = driver.page_source
		nextPage = self.getCurrentPage(res, self.showColumn) - 1
		while (nextPage > 0):
		   completeWebsiteLinkAppendPage = completeWebsiteLink + '&Page=' + str(nextPage)
		   driver.get(completeWebsiteLinkAppendPage)
		   res = driver.page_source + res
		   nextPage -= 1
		   
		driver.close()
		return res;	
		
	def getCurrentPage(self, htmlContent, showColumn):
		soup = BeautifulSoup(htmlContent, 'html.parser')
		totalPigeonNum = soup.select("font:nth-of-type(3)")[0].get_text()
		return int(math.ceil(float(totalPigeonNum)/showColumn))

		
	def getDataCollectionByDate(self, htmlContent, date, showColumn):
		showColumn = showColumn + 1
		htmlContent = htmlContent.encode('utf-8')
		dateCollection = {}
		soup = BeautifulSoup(htmlContent, 'html.parser')
		trWalker = 0
		for tr in soup.select('body > div:nth-of-type(1) > table > tbody > tr > td > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr > td > table tr'):
			trWalker = trWalker + 1
			count = 1
			if trWalker % showColumn == 1:
				continue
				
			collection = {}
			groupKey = {'date': date}
			for td in tr.find_all('td', limit=9):
				content = td.get_text()
				if count == 1:
					collection.update({'totalRank': content})
				elif count == 2:
					collection.update({'selfRank': content})
				elif count == 4:
					groupKey.update({'pigeonryID': content})
				elif count == 5:
					groupKey.update({'pigeonID': content})
				elif count == 7:
					collection.update({'arriveTime': content})
				elif count == 8:
					collection.update({'eastLongitude': content})
				elif count == 9:
					collection.update({'northLatitude': content})
					
				count = count + 1

			dateCollection = super(LingDungCrawler, self).pushIntoDateCollection(dateCollection, collection, groupKey)

		#print(dateCollection)			
		return dateCollection;
