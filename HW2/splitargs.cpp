// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <iostream>
using std::cout;
using std::cerr;

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        if (i < 5) {
            cout << *(argv + i) << "\n";
        } else {
            cerr << *(argv + i) << "\n";
        }
    }
}

