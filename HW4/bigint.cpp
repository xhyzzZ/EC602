// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <string>

using namespace std;

typedef string BigInt;
BigInt multiply_int(const BigInt &a,const BigInt &b) {
	BigInt res(a.size() + b.size(), '0');
    
    for (int i = a.size() - 1; i >= 0; i--) {
        int carry = 0;
        for (int j = b.size() - 1; j >= 0; j--) {
            int tmp = (res.at(i + j + 1) - '0') + (a.at(i) - '0') * (b.at(j) - '0') + carry;
            res.at(i + j + 1) = tmp % 10 + '0';
            carry = tmp / 10;
        }
        res.at(i) += carry;
    }
    
    size_t start = res.find_first_not_of("0");
    if (string::npos != start) {
        return res.substr(start);
    }
    return "0";
}