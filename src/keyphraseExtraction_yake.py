# -*- coding: utf-8 -*-

import json
from glob import glob

import pke

from pprint import pprint

def main():
	kp_extractor = pke.unsupervised.YAKE()

	for path in glob('../minutes/*'):
		with open(path, 'r') as r:
			doc = json.load(r)

		speakers = ['政府', '参考人'] + [speech['speaker'] for speech in doc['meetingRecord'][0]['speechRecord']]

		kp = []
		for speech in doc['meetingRecord'][0]['speechRecord']:
			kp_extractor.load_document(
				input=speech['speech'],
				language='ja',
				normalization=None,
				stoplist=speakers
				)
			kp_extractor.candidate_selection()
			kp_extractor.candidate_weighting()

			kp += kp_extractor.get_n_best(n=100)

		pprint(kp)

if __name__ == "__main__":
    main()
