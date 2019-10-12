// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <vector>

typedef vector<double> Poly;

// Add two polynomials, returning the result
Poly add_poly(const Poly &a, const Poly &b) {
	Poly res;
	int size = max(a.size(),b.size());

	if (a.size() == b.size()) {
		for (int i = 0; i < size; i++) {
			res.push_back(a.at(i) + b.at(i));
		}
	} else {
		for (int i = 0; i < size; i++) {
			if (i >= a.size())
				res.push_back(b.at(i));
			else if (i >= b.size())
				res.push_back(a.at(i));
			else res.push_back(a.at(i) + b.at(i));
		}
	}
	
	while(res.back() == 0.0) {
		res.pop_back();
		if (res.size() == 1) break;
	}
	return res;
}

// Multiply two polynomials, returning the result.
Poly multiply_poly(const Poly &a, const Poly &b) {
	int size = a.size() + b.size();
	Poly res(size - 1, 0);
	for (int i = 0; i < a.size(); i++) {
		for (int j = 0; j < b.size(); j++) {
			res.at(i + j) += (a.at(i) * b.at(j));
		}
	}
	while (res.back() == 0.0) {
		res.pop_back();
		if (res.size() == 1) break;
	}
	return res;
}