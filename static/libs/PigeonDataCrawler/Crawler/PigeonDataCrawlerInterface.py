#!PigeonDataCrawler/bin/python
from flask import Flask, jsonify, request
import json
from PigeonGodOneCrawler import PigeonGodOneCrawler
from LingDungCrawler import LingDungCrawler

app = Flask(__name__)

@app.route('/data/PigeonGodOne', methods=['POST'])
def getPigeonGodOneData():
    union = request.json['union']
    date = request.json['date']
    pigeonGodOneCrawler = PigeonGodOneCrawler()
    dateCollection = pigeonGodOneCrawler.getWebsitePeriodData(union, date)
    return dateCollection
    
@app.route('/data/LingDung', methods=['POST'])
def getLingDungData():
    union = request.json['union']
    date = request.json['date']
    lingDungCrawler = LingDungCrawler()
    dateCollection = lingDungCrawler.getWebsitePeriodData(union, date)
    return dateCollection

if __name__ == '__main__':
	app.run(debug=True)