# -*- coding: utf-8 -*-

import json
from glob import glob

import pke
import numpy as np
from copy import deepcopy

import pickle


def main():
	kp_extractor = pke.unsupervised.MultipartiteRank()

	for path in glob('../minutes/*'):
		with open(path, 'r') as r:
			doc = json.load(r)

		speakers = ['政府', '参考人', '委員長', 'ところ', 'とおり', 'お願い'] + [speech['speaker'] for speech in doc['meetingRecord'][0]['speechRecord']]

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

			speech['keyphrase'] = [k.replace(' ', '') for k, conf in kp_extractor.get_n_best(n=100)]
			tmp = []
			for k, conf in kp_extractor.get_n_best(n=100):
				tmp.append(k.replace(' ', ''))
				for sub_k in k.split(' '):
					tmp.append(sub_k)
			speech['keyphrase_full'] = list(set(tmp))
			out['meetingRecord'][0]['speechRecord'].append(speech)

			kps += speech['keyphrase']

		kps = list(set(kps))
		kp_mat = np.zeros((len(out['meetingRecord'][0]['speechRecord']), len(kps)))

		for i, speech in enumerate(out['meetingRecord'][0]['speechRecord']):
			kps_in_speech = speech['keyphrase']

			for kp in kps_in_speech:
				kp_mat[i, kps.index(kp)] = 1

		with open(f'../keyphrases/{doc["meetingRecord"][0]["issueID"]}.json', 'w') as w:
			json.dump(out, w)

		with open(f'../keyphrases/{doc["meetingRecord"][0]["issueID"]}_mat.pkl', 'wb') as w:
			pickle.dump(kp_mat, w)
		

if __name__ == "__main__":
    main()
