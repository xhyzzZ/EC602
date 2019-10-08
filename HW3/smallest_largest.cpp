// Copyright 2019 Haoyu Xu xhy@bu.edu
double largest_double() {
	double a = 2;
	int x = 2;
	for (int i = 0; i < 1023; i++) {
		a *= x;
	}
	double b = 2;
	double y = 0.5;
	for (int i = 0; i < 52; i++) {
		b *= y;
	}
	
	return a * (2 - b) - 1;
}

double smallest_double() {

}
  
float largest_single() {

}

float smallest_single() {

}