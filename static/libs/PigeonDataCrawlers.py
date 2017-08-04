#coding=utf-8

import requests
import sys
import json
from bs4 import BeautifulSoup

def getWebsitePeriodData(union, date):
	res = getHtmlContent(union, date)
	htmlContent = res.text.encode("utf-8")
	dateCollection = getDataCollectionByDate(htmlContent, date)	
	dateCollection = json.dumps(dateCollection, ensure_ascii=True)
	
	#writeHtmlFile(dateCollection, 'BIG5')
	#print(dateCollection)

	return dateCollection;

def getHtmlContent(union, date):
	url = 'http://www.topigeon.com.tw/qry_sms_list.asp'
	params = {'s1': union, 's2': date, 's5': '99999'}
	jar = requests.cookies.RequestsCookieJar()
	jar.set('qry_sms_list_sysid', union, domain='www.topigeon.com.tw', path='/')

	res = requests.get(url, params=params, cookies=jar)
	
	return res;
	
def getDataCollectionByDate(htmlContent, date):
	dateCollection = {}
	soup = BeautifulSoup(htmlContent, 'html.parser')
	for tr in soup.find_all('tr', attrs={"id": "TableTitleLink"}):
		count = 1
		collection = {}
		groupKey = {'date': date}
		for td in tr.find_all('td', limit=7):
			content = td.get_text().encode("utf-8")
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
			
		dateCollection = pushIntodateCollection(dateCollection, collection, groupKey)
	
	return dateCollection;
	
def pushIntodateCollection(dateCollection, collection, groupKey):
	date = groupKey['date']
	pigeonryID = groupKey['pigeonryID']
	pigeonID = groupKey['pigeonID']

	#group by date
	if dateCollection.get(date) is None :
		dateCollection[date] = {}

	#group by pigeonryID
	if dateCollection.get(date).get(pigeonryID) is None :
		dateCollection[date][pigeonryID] = {}
	
	#group by pigeonID	
	if dateCollection.get(date).get(pigeonryID).get(pigeonID) is None :
		dateCollection[date][pigeonryID][pigeonID] = {}
			
	dateCollection[date][pigeonryID][pigeonID].update(collection)
	
	return dateCollection;	
	
def writeHtmlFile(htmlContent, encodeType):
	name = open('test.html', "w")
	htmlContent = htmlContent.encode(encodeType)
	name.write(htmlContent)
	name.close()
	
	return ;
	
getWebsitePeriodData('1606', '2017/07/30')