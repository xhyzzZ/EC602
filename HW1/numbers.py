# Copyright 2019 Haoyu Xu xhy@bu.edu

def is_happy(x):
	seen = set()
	while x not in seen:
		seen.add(x)
		x = sum([int(y) ** 2 for y in str(x)])
	return x == 1


def product_of_positives(seq):
	product = 1
	for i in range(0, len(seq)):
		if seq[i] > 0:
			product *= seq[i]
	return product

def proper_divisors(n):
	empty_tuple = ()
	for i in range(1, n):
		if (n % i == 0):
			empty_tuple += (i, )
	return empty_tuple

def main():
	# your test code here.
	print(is_happy(19))
	print(proper_divisors(30))
	pass

if __name__ == '__main__':
	main()