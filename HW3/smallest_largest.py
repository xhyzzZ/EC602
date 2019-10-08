#!/usr/bin/python
# Copyright 2019 Haoyu Xu xhy@bu.edu
def largest_double():
	a = 2.0**1023
	b = 2 - 2**(-52)
	return a * b

def smallest_double():
	return 2.0**(-1022) * 2**(-52)
  
def largest_single():
	a = 2.0**127
	b = 2 - 2**(-23)
	return a * b

def smallest_single():
	return 2.0**(-126) * 2**(-23)


def main():
	print(largest_double())
	print(smallest_double())
	print(largest_single())
	print(smallest_single())

if __name__ == '__main__':
	main()