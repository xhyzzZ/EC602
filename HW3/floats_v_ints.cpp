// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <cfloat>
#include <cmath>
#include <cstdint>
#include <iostream>

using namespace std;

int main() {
	int n, m;
	long double Rs, Rm, Ri;

	n = 16, m = 10;
	Rm = (pow(2, n - 1) * (2 - pow(2, -m))) / INT16_MAX;
	Rs = 1 / pow(2, -14);
	Ri = INT16_MAX/pow(2,11);
	cout << "16 : Ri = " << Ri << " Rm = " << Rm << " Rs = " << Rs << endl;

	n = 32, m = 23;
	Rm = FLT_MAX / INT32_MAX;
	Rs = 1 / FLT_MIN;
	Ri = INT32_MAX / pow(2, 24);
	cout << "32 : Ri = " << Ri << " Rm = " << Rm << " Rs = " << Rs << endl;

	n = 64, m = 52;
	Rm = DBL_MAX / INT64_MAX;
	Rs = 1 / DBL_MIN;
	Ri = INT64_MAX / pow(2, 53);
	cout << "64 : Ri = " << Ri << " Rm = " << Rm << " Rs = " << Rs << endl;
}
