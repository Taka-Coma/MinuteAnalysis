# -*- coding: utf-8 -*-

import pickle
from glob import glob

from pprint import pprint

def main():
	for path in glob('../keyphrases/*_mat.pkl'):
		with open(path, 'rb') as r:
			mat = pickle.load(r)

		common = mat.dot(mat.T)
		xs, ys = common.nonzero()

		sim_list = {x: [] for x in set(xs)}
		for x, y in zip(xs, ys):
			if x == y:
				continue
			sim_list[x].append((y, common[x, y]))

		pprint(sim_list)

if __name__ == "__main__":
    main()
