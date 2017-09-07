#coding=utf-8

import requests
import sys
import json
from bs4 import BeautifulSoup

class PigeonDataCrawler(object):

	def __init__(self, websiteLink, outputFileName, encodeType, showColumn, ensure_ascii):
		self.websiteLink = websiteLink
		self.outputFileName = outputFileName
		self.encodeType = encodeType
		self.showColumn = showColumn
		self.ensure_ascii = ensure_ascii
		
	def getWebsitePeriodData(self, union, date):
		htmlContent = self.getHtmlContent(union, date)
		dateCollection = self.getDataCollectionByDate(htmlContent, date, self.showColumn)	
		dateCollection = json.dumps(dateCollection, ensure_ascii = self.ensure_ascii)
		
		#self.writeHtmlFile(htmlContent, self.encodeType)
		#print(dateCollection)

		return dateCollection;	
		
	def writeHtmlFile(self, htmlContent, encodeType):
		name = open(self.outputFileName, "w")
		htmlContent = htmlContent.encode(encodeType)
		name.write(htmlContent)
		name.close()
