# -*- coding: utf-8 -*-

import json
from glob import glob

import pke

def main():
	kp_extractor = pke.unsupervised.MultipartiteRank()

	for path in glob('../minutes/*'):
		with open(path, 'r') as r:
			doc = json.load(r)

		speakers = ['政府', '参考人'] + [speech['speaker'] for speech in doc['meetingRecord'][0]['speechRecord']]

		out = doc.copy()
		out['meetingRecord'][0]['speechRecord'] = []
		for speech in doc['meetingRecord'][0]['speechRecord']:
			kp_extractor.load_document(
				input=speech['speech'],
				language='ja',
				normalization=None,
				stoplist=speakers
				)
			kp_extractor.candidate_selection()
			kp_extractor.candidate_weighting()

			speech['keyphrase'] = kp_extractor.get_n_best(n=100),
			out['meetingRecord'][0]['speechRecord'].append(speech)

		with open(f'../keyphrases/{doc["meetingRecord"][0]["issueID"]}.json', 'w') as w:
			json.dump(out, w)
		

if __name__ == "__main__":
    main()
