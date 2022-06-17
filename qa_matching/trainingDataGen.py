# -*- coding: utf-8 -*-

import json
import re
from glob import glob
import csv

def main():
	header = ('sentence', 'next_sentence', 'annotation')
	for path in glob('../minutes/*.json'):
		data = loadMinute(path)

		minid = path[path.rfind('/')+1:-5]

		out = [header]
		for speech in data['meetingRecord'][0]['speechRecord'][1:]:
			txt = speech['speech']

			sents = [sent.strip() for sent in txt.split('\r\n')]
			for i in range(1, len(sents)):
				pair = (sents[i-1], sents[i]) 

				out.append(pair)

			out.append(('===',))

		with open(f'./training_data/{minid}.csv', 'w') as w:
			writer = csv.writer(w)
			writer.writerows(out)

def loadMinute(path):
	with open(path, 'r') as r:
		out = json.load(r)
	return out

if __name__ == "__main__":
    main()
