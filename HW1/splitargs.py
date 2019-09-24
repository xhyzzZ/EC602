# Copyright 2019 Haoyu Xu xhy@bu.edu

import sys

if len(sys.argv) <= 5:
	# send first x arguments through stdout (where x is 1-4)
	for i in range(1, len(sys.argv)):
		print(sys.argv[i]);
else:
	# send first 4 arguments through stdout
	for i in range(1, 5):
		print(sys.argv[i]);
	# the remaining through stderr
	for i in range(5, len(sys.argv)):
		sys.stderr.write(sys.argv[i] + '\n');