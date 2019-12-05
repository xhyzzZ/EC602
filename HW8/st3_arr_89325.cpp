// Copyright 2019 Haoyu Xu xhy@bu.edu
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "timer.h"

using std::vector;
using std::string;
using std::cout;
using std::sort;
using std::swap;
using std::map;

class Arrangements {
 private:
  // your private data
  string names;
  map<int64_t, double> mymap;
  map<int64_t, double> dinner_map;

 public:
  Arrangements() {
    this->names = "";
    for (char i = 'a'; i <= 'z'; i++) names += i;
    for (char i = 'A'; i <= 'Z'; i++) names += i;
  }
  explicit Arrangements(string thenames) { this->names = thenames; }

  vector<string> panel_rec(string str) {
    vector<string> v;

    if (str.length() == 1) {
      v.push_back(str);
    } else if (str.length() == 2) {
      v.push_back(str);
      string newstr = "";
      for (int64_t i = str.length() - 1; i >= 0; i--) newstr += str.at(i);
      v.push_back(newstr);
    } else {
      string newstr = "";
      for (int64_t i = 1; i < str.length(); i++) newstr += str.at(i);
      vector<string> v1 = panel_rec(newstr);
      for (int64_t i = 0; i < v1.size(); i++) {
        string s = "";
        s += str.at(0);
        s += v1.at(i);
        v.push_back(s);
      }
      newstr = "";
      for (int64_t i = 2; i < str.length(); i++) newstr += str.at(i);
      vector<string> v2 = panel_rec(newstr);
      for (int64_t i = 0; i < v2.size(); i++) {
        string s = "";
        s += str.at(1);
        s += str.at(0);
        s += v2.at(i);
        v.push_back(s);
      }
    }

    return v;
  }

  void permute(vector<string> res, string str, int l, int r) {
    if (l == r) {
        res.push_back(str);
    } else {
        for (int i = l; i <= r; i++) {
            swap(str.at(l), str.at(i));
            permute(res, str, l + 1, r);
            swap(str.at(l), str.at(i));
        }
    }
  }

  vector<string> panel_shuffles(int64_t n) {
    string str = "";
    for (int64_t i = 0; i < n; i++) str += names.at(i);
    return panel_rec(str);
  }

  vector<string> dinner_shuffles(int64_t n) {
    // string str = "";
    // for (int64_t i = 0; i < n; i++) str += names.at(i);
    // vector<string> v;
    // if (n == 1) {
    //   v.push_back(str);
    // } else if (n == 2) {
    //   v.push_back(str);
    //   string newstr = "";
    //   for (int64_t i = str.length() - 1; i >= 0; i--) newstr += str.at(i);
    //   v.push_back(newstr);
    // } else {
    //   vector<string> v1 = panel_shuffles(n);
    //   for (int64_t i = 0; i < v1.size(); i++) {
    //     v.push_back(v1.at(i));
    //   }
    //   string s = "";
    //   for (int64_t i = 1; i < str.length(); i++) {
    //     s += str.at(i);
    //   }
    //   s += str.at(0);
    //   v.push_back(s);
    //   s = "";
    //   s += str.at(str.length() - 1);
    //   for (int64_t i = 0; i < str.length() - 1; i++) {
    //     s += str.at(i);
    //   }
    //   v.push_back(s);
    //   s = "";
    //   for (int64_t i = 1; i < str.length() - 1; i++) s += str.at(i);
    //   v1 = panel_rec(s);
    //   for (int64_t i = 0; i < v1.size(); i++) {
    //     string x = "";
    //     x += str.at(str.length() - 1);
    //     x += v1.at(i);
    //     x += str.at(0);
    //     v.push_back(x);
    //   }
    // }
    // return v;
    vector<string> res;
    string s = "";
    for (int64_t i = 0; i < n; i++) str += names.at(i);
    permute(res, s, 0, n - 1);
    return res;
  }

  double panel_count(int64_t n) {
    if (n == 1) mymap.insert(std::pair<int64_t, int64_t>(n, 1));
    if (n == 2) mymap.insert(std::pair<int64_t, int64_t>(n, 2));
    if (mymap.find(n) == mymap.end()) {
      double res = panel_count(n - 1) + panel_count(n - 2);
      mymap.insert(std::pair<int64_t, int64_t>(n, res));
    }
    return mymap.at(n);
  }
  double dinner_count(int64_t n) {
    if (n == 1) dinner_map.insert(std::pair<int64_t, int64_t>(n, 1));
    if (n == 2) dinner_map.insert(std::pair<int64_t, int64_t>(n, 2));
    if (dinner_map.find(n) == dinner_map.end()) {
      double res = panel_count(n - 2) + 2 + panel_count(n);
      dinner_map.insert(std::pair<int64_t, int64_t>(n, res));
    }
    return dinner_map.at(n);
  }

  // Solution goes here.
};

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
void alternate_tests();
void interactive_main();

int main(int argc, char const ** argv) {
  if (argc > 1 and string(*(argv+1)) == "alt")
    alternate_tests();
  else if (argc > 1 and (string(*(argv+1)) == string("int")))
    interactive_main();
  else
    standard_tests();
}

// tests to be run for full credit, including performance.
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

  while (t_panel.time() < 0.5 and n <= 32)  {
    double last = t_panel.time();
    t_panel.start();
    vector<string> res = standard.panel_shuffles(n);
    t_panel.stop();
    //show_partial_result("panel", res, n);
    cout << "time " << t_panel.time() - last << "\n";
    n++;
  }

  int largest_panel = n - 1;

  Timer t_dinner("dinner timing", true);
  n = 4;
  cout << "\nHow many dinner shuffles can be created in 0.5 seconds?\n";

  while (t_dinner.time() < 0.5 and n <= 32)  {
    double last = t_dinner.time();
    t_dinner.start();
    vector<string> res = standard.dinner_shuffles(n);
    t_dinner.stop();
    //show_partial_result("dinner", res, n);
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

void alternate_tests() {
  cout.precision(15);
  // Basic test
  Arrangements standard;

  cout << "\nPanel Shuffles for 4 panelists.\n";
  show_result(standard.panel_shuffles(4));

  cout << "\nPanel Shuffles for 10 panelists.\n";
  show_result(standard.panel_shuffles(10));

  int n = 1;

  // Count tests
  Timer t_pc("panel count", true);
  cout << "\nPanel Shuffle Count Table (0.1 seconds)\n";
  cout << "     N  panel(N)\n";
  while (n < 52 and t_pc.time() < 0.1) {
    t_pc.start();
    double pc = standard.panel_count(n);
    t_pc.stop();
    cout << std::setw(6) << n << " "
         << std::setw(6) << pc << "\n";
    n++;
  }

  cout << "\nHow many panel shuffles can be created in 0.5 seconds?\n";
  n = 4;

  Timer t_panel("panel", true);

  while (t_panel.time() < 0.5)  {
    t_panel.start();
    vector<string> res = standard.panel_shuffles(n);
    t_panel.stop();
    show_partial_result("panel", res, n);
    n++;
  }
  cout << "\nLargest panel shuffles performed: "
       << n - 1 << "\n";
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
