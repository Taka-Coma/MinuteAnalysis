# -*- coding: utf-8 -*-

import psycopg2 as psql
import re
import requests
import json

def main():
	con = psql.connect(dbname='hourei_disc_minute', user='taka-coma', host='192.168.111.200')
	cur = con.cursor()

	cur.execute('''
		select distinct minute_link
		from law_minute
		except
		select distinct minute_link
		from minute_id
	''')

	rows = [row for row in cur.fetchall()]

	minid_pattern = re.compile('minId=([0-9A-Z]+)\&?')

	for row in rows:
		matches = minid_pattern.findall(row[0])

		minid = matches[0]

		url = f"https://kokkai.ndl.go.jp/api/meeting"
		params = {
			"issueID": minid,
			"recordPacking": "json"
		}
		fname = f'../minutes/{minid}.json'

		res = requests.get(url, params=params).json()
		if res['numberOfRecords'] == 0:
			continue

		with open(fname, 'w') as w:
			json.dump(res, w)

		cur.execute('''
			insert into minute_id
			values (%s, %s)
		''', (row[0], minid))
		con.commit()

	cur.close()
	con.close()

if __name__ == "__main__":
    main()
