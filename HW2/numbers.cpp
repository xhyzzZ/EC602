// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <string>
#include <vector>
using std::string;
using std::vector;


bool is_happy(int x) {
    int num = 0;
    while (x != 1 && x != 4) {
        while (x) {
            num += (x % 10) * (x % 10);
            x /= 10;
        }
        x = num;
        num = 0;
    }
    return 1 == x;
}


double product_of_positives(vector<double> array) {
    double product = 1;
    for (int i = 0; i < array.size(); i++) {
        if (array.at(i) > 0) product *= array.at(i);
    }
    return product;
}

int product_of_positives(vector<int> array) {
    int product = 1;
    for (int i = 0; i < array.size(); i++) {
        if (array.at(i) > 0) product *= array.at(i);
    }
    return product;
}

vector<int> proper_divisors(int n) {
    vector<int> array;
    for (int i = 1; i < n; i++) {
        if (n % i == 0) array.push_back(i);
    }
    return array;
}

string add(string& num1, string& num2) {
    int i = num1.size() - 1, j = num2.size() - 1, carry = 0;
    if (i < j) return add(num2, num1);
    for (; (j >= 0 || carry) && i >= 0; carry /= 10) {
        if (j >= 0) {
            carry += num2.at(j--) - '0';
        }
        carry += num1.at(i) - '0';
        num1.at(i--) = carry % 10 + '0';
    }
    if (carry) return '1' + num1;
    return num1;
}
