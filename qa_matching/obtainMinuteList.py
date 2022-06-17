# -*- coding: utf-8 -*-

import requests
import psycopg2 as psql

def main():
	query = '''
	prefix lawlod_diss_prop: <https://history.lawlod.net/discussion/property/>
	prefix lawlod_prop: <https://history.lawlod.net/property/> 

	SELECT distinct ?s ?o
	WHERE {
		?s lawlod_diss_prop:history/lawlod_diss_prop:discussion/lawlod_diss_prop:minuteLink ?o ;
		lawlod_prop:promulgateDate ?date .
		FILTER (?date > "1946-11-01"^^xsd:dateTime)
	}
	'''

	res = requests.get('https://history.lawlod.net/sparql', params={
		'defaul_graph': 'https://history.lawlod.net',
		'format': 'json',
		'query': query,
	})

	con = psql.connect(dbname='hourei_disc_minute', user='taka-coma', host='192.168.111.200')
	cur = con.cursor()

	for r in res.json()['results']['bindings']:
		lawid = r['s']['value']
		min_link = r['o']['value']
		min_link = min_link[:min_link.find('&spkNum')]

		cur.execute('''
			insert into law_minute
			values (%s, %s)
		''', (lawid, min_link))

	con.commit()
	cur.close()
	con.close()
	

if __name__ == "__main__":
    main()
