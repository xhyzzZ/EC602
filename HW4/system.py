#!/usr/bin/python
# Copyright 2019 Haoyu Xu xhy@bu.edu
import numpy as np

part_a = input().strip().split(' ')
part_b = input().strip().split(' ')
part_a = [float(x) for x in part_a]
part_b = [float(x) for x in part_b]
if all(item == 0 for item in np.convolve(part_a, part_b)):
	print(0)
else:
	for item in np.convolve(part_a, part_b):
		print(item, end = " ")