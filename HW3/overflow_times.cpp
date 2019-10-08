// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <cmath>
#include <cstdint>
#include <ctime>
#include <iostream>

int main() {
    clock_t start, end;
    uint16_t min = 1;
    // start timing
    start = clock();
    while (min > 0) {
        min++;
    }
    // time ends here
    end = clock();
    double microseconds = (double) (1.0e6) * (end - start) / CLOCKS_PER_SEC;
    double nanoseconds = (1.0e3) * microseconds * (pow(2.0, 8)) / (pow(2.0, 16));
    double seconds = microseconds / (1.0e6) * (pow(2, 32)) / (pow(2, 16));
    double years = microseconds / (1.0e6) * (pow(2, 32)) / (3600 * 24 * 365) * (pow(2, 64)) / (pow(2, 16)) / (pow(2, 32));

    std::cout << "estimated int8 time (nanoseconds):  "
              << nanoseconds << std::endl;
    std::cout << "measured int16 time (microseconds):  "
              << microseconds << std::endl;
    std::cout << "estimated int32 time (seconds):  "
              << seconds << std::endl;
    std::cout << "estimated int64 time (years):  "
              << years << std::endl;
}
