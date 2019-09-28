#!/usr/bin/python
# Copyright © 2019 Haoyu Xu xhy@bu.edu

Table = "{:<6} {:<22} {:<22} {:<22}"
print(Table.format('Bytes', 'Largest Unsigned Int', 'Minimum Signed Int', 'Maximum Signed Int'))

for x in range(1, 9):
	bits = 8 * x
	size = 2 ** bits - 1
	imax = 2 ** (bits - 1) - 1
	imin = imax - size
	print(Table.format(x, size, imin, imax))