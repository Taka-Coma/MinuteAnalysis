# -*- coding: utf-8 -*-

import json
from glob import glob

import pke
import numpy as np
from copy import deepcopy

def main():
	kp_extractor = pke.unsupervised.MultipartiteRank()

	for path in glob('../minutes/*'):
		with open(path, 'r') as r:
			doc = json.load(r)

		speakers = ['政府', '参考人'] + [speech['speaker'] for speech in doc['meetingRecord'][0]['speechRecord']]

		kps = []

		out = deepcopy(doc)
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

			speech['keyphrase'] = [k for k, conf in kp_extractor.get_n_best(n=100)]
			out['meetingRecord'][0]['speechRecord'].append(speech)

			kps += speech['keyphrase']

		kps = list(set(kps))
		kp_mat = np.zeros((len(out['meetingRecord'][0]['speechRecord']), len(kps)))

		for i, speech in enumerate(out['meetingRecord'][0]['speechRecord']):
			kps_in_speech = speech['keyphrase']

			inds = [(i, kps.index(kp)) for kp in kps_in_speech]
			np.put(kp_mat, inds, [1])

		print(kp_mat)

		return

		with open(f'../keyphrases/{doc["meetingRecord"][0]["issueID"]}.json', 'w') as w:
			json.dump(out, w)
		

if __name__ == "__main__":
    main()
