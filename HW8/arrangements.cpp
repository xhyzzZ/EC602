// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "timer.h"

using std::vector;
using std::string;
using std::cout;
using std::sort;

class Arrangements {
 private:
  bool flag;
  string names;
  string names1;
  static vector<double> fib;
  static vector<double> dinner;
  static string reverse(string names, int start, int end) {
    string rev;
    for (int i = end; i >= start; i--)
      rev.push_back(names.at(i));
    return rev;
  }

 public:
  Arrangements() {
    flag = false;
    for (char i = 'a'; i <= 'z'; i++) names += i;
    for (char i = 'A'; i <= 'Z'; i++) names += i;
  }

  explicit Arrangements(string thenames) {
    flag = false;
    names = thenames;
  }

  vector<string> panel_shuffles(int n) {
    if (n > names.size())
      throw n;

    string guest;
    if (!flag)
      guest = names;
    else if (flag)
      guest = names1;
    if (n == 1)
      return {string(1, guest.at(0))};
    string temp = string(1, guest.at(1));
    temp.push_back(guest.at(0));
    vector<vector<string>> res =  {{string(1, guest.at(0))},
      {guest.substr(0, 2), temp}
    };

    for (int i = 2; i < n; i++) {
      vector<string> nextCombinations;
      for (int j = 0; j < res.at(i - 1).size(); j++)
        nextCombinations.push_back(res.at(i - 1).at(j)
                                   + string(1, guest.at(i)));
      for (int j = 0; j < res.at(i - 2).size(); j++)
        nextCombinations.push_back(res.at(i - 2).at(j)
                                   + reverse(guest, i - 1, i));
      res.push_back(nextCombinations);
    }

    return res.back();
  }

  vector<string> dinner_shuffles(int n) {
    if (n > names.size())
      throw n;

    vector<string> res = panel_shuffles(n);
    if (n <= 2)
      return res;

    res.push_back(names.substr(1, n - 1) + string(1, names.at(0)));
    res.push_back(string(1, names.at(n - 1)) + names.substr(0, n - 1));

    flag = true;
    names1 = names.substr(1, n - 2);
    vector<string> v = panel_shuffles(n - 2);
    flag = false;

    for (const auto & i : v)
      res.push_back(string(1, names.at(n - 1)) + i + string(1, names.at(0)));

    return res;
  }

  double panel_count(int n) {
    if (n > names.size())
      throw n;
    return fib.at(n);
  }

  double dinner_count(int n) {
    if (n > names.size())
      throw n;
    return dinner.at(n);
  }

  vector<double> getFibs() {
    return fib;
  }
};

vector<double> setFibs() {
  vector<double> fib;
  double a = 1, b = 1, c;
  fib.push_back(a);
  fib.push_back(b);
  for (int i = 2; i <= 100; i++) {
    c = a + b;
    a = b;
    b = c;
    fib.push_back(c);
  }
  return fib;
}

vector<double> setDinner() {
// Formula: F(n) + F(n - 2) + 2
  Arrangements arrange;
  vector<double> dinner = {1, 1, 2};
  vector<double> fib = arrange.getFibs();
  for (int i = 3; i <= 100; i++)
    dinner.push_back(fib.at(i) + fib.at(i - 2) + 2);
  return dinner;
}

vector<double> Arrangements::fib = setFibs();

vector<double> Arrangements::dinner = setDinner();

// Methods and constructors defined here:

// TESTING: leave this line and below as is.

void show_result(vector<string> v) {
    sort(v.begin(), v.end());
    for (auto c : v)
        cout << c << "\n";
    cout << "\n";
}

void show_partial_result(string testname, vector<string> res, int n) {
    if (res.empty()) return;

    sort(res.begin(), res.end());

    std::vector<uint64_t> locs{0, res.size() / 3,
                               2 * res.size() / 3, res.size() - 1};
    std::cout << "\n" << testname << " " << n << "\n";
    for (auto i : locs) {
        std::cout << " res.at(" << i
                  << ") = " << res.at(i) << "\n";
    }
}


const int COUNTLIM = 100;
const int COUNTLIM_SMALL = 30;

void standard_tests();
void interactive_main();

int main(int argc, char const ** argv) {
    if (argc > 1 and (string(*(argv + 1)) == string("int")))
        interactive_main();
    else
        standard_tests();
}

void standard_tests() {
    int n;

    cout.precision(15);

    // Basic test
    Arrangements standard;

    cout << "\nPanel Shuffles for 4 panelists.\n";
    show_result(standard.panel_shuffles(4));

    cout << "\nDinner Shuffles for 4 guests.\n";
    show_result(standard.dinner_shuffles(4));

    // Test other names
    Arrangements numbers("123456789");
    Arrangements symbols("!@#$%^&*()_+");

    std::array<Arrangements*, 3> v{&standard, &numbers, &symbols};

    cout << "\nPanel Shuffles for 6 panelists, 3 sets of names.\n";
    for (auto arr : v)
        show_result(arr->panel_shuffles(6));

    cout << "\nDinner Shuffles for 6 guests, 3 sets of names.\n";
    for (auto arr : v)
        show_result(arr->dinner_shuffles(6));

    // Count tests
    Arrangements large(string(COUNTLIM, 'a'));

    Timer t_pc("panel count", true);
    n = 1;
    cout << "\nPanel Shuffle Count Table (0.1 seconds)\n";
    cout << "     N  panel(N)\n";

    while (n < COUNTLIM and t_pc.time() < 0.1) {
        t_pc.start();
        double pc = large.panel_count(n);
        t_pc.stop();
        cout << std::setw(6) << n << " "
             << std::setw(6) << pc << "\n";
        n++;
    }


    Timer t_dc("dinner count", true);
    n = 1;
    cout << "\nDinner Shuffle Count Table (0.1 seconds)\n";
    cout << "     N  dinner(N)\n";

    while (n < COUNTLIM and t_dc.time() < 0.1) {
        t_dc.start();
        double dc = large.dinner_count(n);
        t_dc.stop();
        cout << std::setw(6) << n << " "
             << std::setw(6) << dc << "\n";
        n++;
    }

    Timer t_panel("panel", true);
    n = 4;
    cout << "\nHow many panel shuffles can be created in 0.5 seconds?\n";

    while (t_panel.time() < 0.5)  {
        double last = t_panel.time();
        t_panel.start();
        vector<string> res = standard.panel_shuffles(n);
        t_panel.stop();
        show_partial_result("panel", res, n);
        cout << "time " << t_panel.time() - last << "\n";
        n++;
    }

    int largest_panel = n - 1;

    Timer t_dinner("dinner timing", true);
    n = 4;
    cout << "\nHow many dinner shuffles can be created in 0.5 seconds?\n";

    while (t_dinner.time() < 0.5)  {
        double last = t_dinner.time();
        t_dinner.start();
        vector<string> res = standard.dinner_shuffles(n);
        t_dinner.stop();
        show_partial_result("dinner", res, n);
        cout << "time " << t_dinner.time() - last << "\n";
        n++;
    }
    cout << "\nLargest panel shuffles performed: "
         << largest_panel << "\n";
    cout << "\nLargest dinner shuffles performed: " << n - 1 << "\n";

    // Error checking
    Arrangements small("abcd");
    cout << "\nError Handling Tests\n";

    try {
        small.panel_count(5);
    } catch (int n) {
        cout << n;
    }
    try {
        small.panel_shuffles(6);
    } catch (int n) {
        cout << n;
    }
    try {
        small.dinner_count(7);
    } catch (int n) {
        cout << n;
    }
    try {
        small.dinner_shuffles(89);
    } catch (int n) {
        cout << n;
    }
    try {
        large.dinner_shuffles(122);
    } catch (int n) {
        cout << n;
    }
    try {
        numbers.dinner_shuffles(9);
    } catch (int n) {
        cout << n;
    }
    try {
        numbers.dinner_shuffles(10);
    } catch (int n) {
        cout << n;
    }
    cout << "\n";
}


void interactive_main() {
    std::string asktype, symbols;
    int number;
    cout << "Type quit to exit.\n";
    cout << "Commands:\npc names n\nps names n\ndc names n\nds names n\n";
    cout.precision(15);

    while (true) {
        std::cin >> asktype;
        if (asktype == "quit") break;
        std::cin >> symbols;
        Arrangements h(symbols);
        std::cin >> number;
        if (asktype == "pc") {
            std::cout << "panel_count(" << number <<  ") = ";
            std::cout << h.panel_count(number) << "\n";
        } else if (asktype == "ps") {
            std::cout << "panel_shuffles(" << number <<  ") = ";
            for (auto e : h.panel_shuffles(number) )
                std::cout << e << " ";
            std::cout << "\n";
        } else if (asktype == "dc") {
            std::cout << "dinner_count(" << number << ") = ";
            std::cout << h.dinner_count(number) << "\n";
        } else if (asktype == "ds") {
            std::cout << "dinner_shuffles(" << number <<  ") = ";
            for (auto e : h.dinner_shuffles(number))
                std::cout << e << " ";
            std::cout << "\n";
        }
    }
}