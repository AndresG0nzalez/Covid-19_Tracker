#!/usr/bin/python3

import requests
import json
import mysql.connector
import collections

zip_code_data = collections.namedtuple('zip_code_data', 'cases city county')

def dbconnect():
	db = mysql.connector.connect(
		host='localhost',
		user='puser',
		# password='A6p)td#7xZT8u3w,'
		password='securepw',
		database='cop4710'
	)

	return db

def populate_county(db, cr):
	j = json.loads(requests.get(county_json_url).text)

	for i in j['features']:
		name = i['attributes']['County_1'];
		cases = i['attributes']['CasesAll'];
		new_cases = i['attributes']['NewPos'];
		deaths = i['attributes']['Deaths'];
		age_0_4 = i['attributes']['C_Age_0_4'];
		age_5_14 = i['attributes']['C_Age_5_14'];
		age_15_24 = i['attributes']['C_Age_15_24'];
		age_25_34 = i['attributes']['C_Age_25_34'];
		age_35_44 = i['attributes']['C_Age_35_44'];
		age_45_54 = i['attributes']['C_Age_45_54'];
		age_5_14 = i['attributes']['C_Age_5_14'];
		age_55_64 = i['attributes']['C_Age_55_64'];
		age_65_74 = i['attributes']['C_Age_65_74'];
		age_75_84 = i['attributes']['C_Age_75_84'];
		age_85_plus = i['attributes']['C_Age_85plus'];
		age_median = i['attributes']['C_AgeMedian'];
		men = i['attributes']['C_Men'];
		women = i['attributes']['C_Women'];
		white = i['attributes']['C_RaceWhite'];
		black = i['attributes']['C_RaceBlack'];
		hispanic_y = i['attributes']['C_HispanicYES'];
		hispanic_n = i['attributes']['C_HispanicNO'];

		sql = 'INSERT INTO County (county_name, cases, age_0_4, age_15_24, age_25_34, age_35_44, age_45_54, age_5_14, age_55_64, age_65_74, age_75_84, age_85_plus, age_median, new_cases, deaths, men, women, race_white, race_black, race_hispanic_yes, race_hispanic_no) VALUES (' + '%s,' * 20 + '%s)'
		val = (name, cases, age_0_4, age_15_24, age_25_34, age_35_44, age_45_54, age_5_14, age_55_64, age_65_74, age_75_84, age_85_plus, age_median, new_cases, deaths, men, women, white, black, hispanic_y, hispanic_n)
		cr.execute(sql, val)
		db.commit();

def populate_city_zip(db, cr):
	j = json.loads(requests.get(zip_json_url).text)
	cities = {}
	
	for i in j['features']:
		city = i['attributes']['POName']
		county = i['attributes']['COUNTYNAME']

		if city != None and city != 'NONE':
			cities[city] = county

	for city in cities:
		val = (city, cities[city])
		sql = 'INSERT INTO City (name, county) VALUES (%s, %s)'
		cr.execute(sql, val)
		continue
	db.commit()


	zips = {}
	for i in j['features']:
		zip_code = i['attributes']['ZIP']
		cases = i['attributes']['Cases_1']
		city = i['attributes']['POName']
		county = i['attributes']['COUNTYNAME']

		if city == 'NONE':
			city = None

		if county == 'NONE':
			county = None

		if cases == '<5':
			cases = '0'

		data = zip_code_data(cases=cases, city=city, county=county)

		if zip_code not in zips:
			zips[zip_code] = data	
		elif data.cases > zips[zip_code].cases:
			zips[zip_code] = data
				
	sql = 'INSERT INTO zip_code (zip_code, num_cases, city, county) VALUES (%s, %s, %s, %s)'
	for z in zips:
		d = zips[z]
		val = (z, d.cases, d.city, d.county)
		cr.execute(sql, val)
	db.commit()

def main():
	db = dbconnect()
	cr = db.cursor()

	cr.execute('DELETE FROM zip_code WHERE 1=1')
	cr.execute('DELETE FROM City WHERE 1=1')
	cr.execute('DELETE FROM County WHERE 1=1')


	populate_county(db, cr)
	populate_city_zip(db, cr)
		


county_json_url = 'https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Cases/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token='

zip_json_url = 'https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_Cases_Zips_COVID19/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=ZIP%2C+COUNTYNAME%2C+POName%2C+Cases_1&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token='
if __name__ == "__main__":
    main()
