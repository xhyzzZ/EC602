// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <iostream>
#include <cstdint>
#include <ctime>
#include <cmath>
int main() {
    clock_t start_clock, end_clock;
    uint16_t m = 1;
    // start timing
    start_clock = clock();
    while (m > 0) {
    	m++;
    }
    // time ends here
    end_clock = clock();
    double microseconds = (double)(1.0e6) * (end_clock - start_clock) / CLOCKS_PER_SEC;
    double nanoseconds = (1.0e3) * microseconds * (pow(2.0, 8)) / (pow(2.0, 16));
    double seconds = microseconds / (1.0e6) * (pow(2, 32)) / (pow(2, 16));
    double years = microseconds / (1.0e6) * (pow(2, 32)) / (pow(2, 16)) / (3600 * 24 * 365) * (pow(2, 64)) / (pow(2, 32));

    std::cout << "estimated int8 time (nanoseconds):  "
              << nanoseconds << std::endl;
    std::cout << "measured int16 time (microseconds):  "
              << microseconds << std::endl;
    std::cout << "estimated int32 time (seconds):  "
              << seconds << std::endl;
    std::cout << "estimated int64 time (years):  "
              << years << std::endl;
}