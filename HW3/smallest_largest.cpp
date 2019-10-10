// Copyright 2019 Haoyu Xu xhy@bu.edu
double largest_double() {
	double res;
	long int *pointer = (long int*) &res;
	*pointer = 0x7fefffffffffffff;

	return res;
}

double smallest_double() {
	double res;
	long int *pointer = (long int*) &res;
	*pointer = 0x1;

	return res;
}
  
float largest_single() {
	float res;
	int *pointer = (int*) &res;
	*pointer = 0x7f7fffff;

	return res;
}

float smallest_single() {
	float res;
	int *pointer = (int*) &res;
	*pointer = 0x00000001;

	return res;
}