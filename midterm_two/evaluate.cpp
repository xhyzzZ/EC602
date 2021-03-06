// Copyright 2019 Haoyu Xu xhy@bu.edu

/*
Write a function evaluate
that "evaluates" the string
containing additions and subtractions
of integers. The string will
have no spaces and only integer values.

example:

evaluate("100-12+1-3+18") = 104
evaluate("+2-5") = -3
evaluate("-6+11+6") = 11

There will never be back-to-back
+ and - symbols.

The function signature below must not be modified.

RULES:
 - brackets are allowed
 - iostream and string can be included, nothing else.
 - your program should compile as submitted (main() must be here)
 - astyle and cpplint will not be used, but I
   may read and evaluate your code as part of the grade

   */

#include <iostream>
#include <string>

using std::string;
using std::vector;
using std::cout;
using std::endl;

int extract_num(string s, int &i) {
  int num = 0;
  while (i < s.size()) {
    if (isdigit(s[i])) num = num * 10 + s[i] - '0';
    else return num;
    i++;
  }
  return num;
}

int evaluate(string s) {
  int sum = 0, sign, i;
  if (s.size() < 1) return sum;
  if (s[0] == '+') {
    sign = 1;
    i = 1;
  } else if (s[0] == '-') {
    sign = -1;
    i = 1;
  } else {
    sign = 1;
    i = 0;
  }
  int num = extract_num(s, i);
  while (i < s.size()) {
    if (s[i] == '+' || s[i] == '-') {
      char op = s[i];
      sum += num * sign;
      num = extract_num(s, ++i);
      sign = (op == '+' ? 1 : -1);
    }
  }
  sum += num * sign;
  return sum;
}

int main(int argc, char **argv) {
  string s = argv[1];
  cout << evaluate(s) << endl;
}

// MAIN
// your program will be compiled with the code
// above this line, with my main() inserted
// you can add a main for testing below




