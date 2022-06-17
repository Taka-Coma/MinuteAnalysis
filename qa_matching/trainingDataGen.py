# -*- coding: utf-8 -*-

import json
import re

def main():
	#data = loadMinute('../minutes/119804319X00920190508.json')
	data = loadMinute('../minutes/119814319X01220190516.json')

	nameOfHouse = data['meetingRecord'][0]['nameOfHouse']

	heading = None
	for speech in data['meetingRecord'][0]['speechRecord'][1:]:
		txt = speech['speech']

		sents = [sent.strip() for sent in txt.split('\r\n')]
		print(sents)
		print('===')

def loadMinute(path):
	with open(path, 'r') as r:
		out = json.load(r)
	return out

if __name__ == "__main__":
    main()
