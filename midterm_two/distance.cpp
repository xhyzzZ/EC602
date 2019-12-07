// Copyright 2019 Haoyu Xu xhy@bu.edu

/*

Distance Between Two Vectors
----------------------------


Given two vectors of integers which are
re-arrangements of each other, write
a function to find
the distance between the
locations (ie. the difference of their
index values) of the matching elements.

Example:

distance({3,9,5},{5,3,9}) = 4

because 3 has been moved 1 spot, 9 moved 1 spot , and 5 moved 2 spots


distance({2,5,3},{5,2,3}) = 2

because 2 and 5 are each 1 away from
where they are in the other vector


distance({42,12},{42,12}) = 0

because the values are in the same locations
in each vector.

If the vectors are not
re-arrangements of each other,
throw the string "int not found"

extra credit: make it fast.

You may assume that the elements
are unique.

The function signature below must not be modified.


RULES:
 - brackets are allowed
 - iostream and vector can be included, nothing else.
 - your program should compile as submitted (main() must be here)
 - astyle and cpplint will not be used, but I
   may read and evaluate your code as part of the grade
*/


#include <iostream>
#include <vector>
#include <string>

using std::vector;
using std::string;

int distance(vector<int> a, vector<int> b) {
  // insert code here.
  sort(a.begin(), a.end());
  sort(b.begin(), b.end());
  if (a != b) throw std::string("int not found");
//    sort(a.begin(), a.end());
  int res = 0;
  for (int i = 0; i < a.size(); i++) {
    for (int j = 0; j < b.size(); j++) {
      if (a[i] == b[j]) {
        res += abs(j - i);
      }
    }
  }
  return res;
}

int main() {
  vector<int> a{1, 2, 3};
  vector<int> b{3, 2, 1};
  int res = distance(a, b);
  std::cout << res;
}

// MAIN
// your program will be compiled with the code
// above this line, with my main() inserted
// you can add a main for testing below




