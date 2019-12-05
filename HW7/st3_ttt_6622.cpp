// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <iostream>
#include <map>
#include <string>
#include <vector>
#include "movedef.h"

using std::cout;
using std::map;
using std::string;
using std::vector;

// char tttresult(string board) {
//   if (board.size() != 9) return 'e';
//   for (char i : board) {
//     if (i != 'o' && i != 'x' && i != '#') return 'e';
//   }
//   int countX = 0, countO = 0;
//   for (char i : board) {
//     if (i == 'x') countX++;
//     if (i == 'o') countO++;
//   }
//   int diff = countX - countO;
//   if (diff > 1 || diff < 0) return 'i';
//   bool xwon = false, owon = false;
//   for (int i = 0; i < 3; i++) {
//     if (board.at(i) == board.at(i + 3) && board.at(i + 3) == board.at(i + 6)) {
//       if (board.at(i) == 'x') xwon = true;
//       if (board.at(i) == 'o') owon = true;
//     }
//     if (board.at(3 * i) == board.at(3 * i + 1) && board.at(3 * i) ==
//         board.at(3 * i + 2)) {
//       if (board.at(3 * i) == 'x') xwon = true;
//       if (board.at(3 * i) == 'o') owon = true;
//     }
//   }

//   if ((board.at(0) == board.at(4) && board.at(4) == board.at(8)) ||
//       (board.at(2) == board.at(4) && board.at(4) == board.at(6))) {
//     if (board.at(4) == 'x') xwon = true;
//     if (board.at(4) == 'o') owon = true;
//   }
//   if (xwon && owon) return 'i';
//   if (!xwon && !owon) {
//     if (countO + countX < 9) return 'c';
//     if (countO + countX == 9) return 't';
//   }

//   if (xwon) {
//     if (diff == 1) return 'x';
//   }

//   if (owon) {
//     if (diff == 0) return 'o';
//   }

//   return 'i';
// }
void XOincrementer(int *x, int*o, char p) {
  if (p == 'x') *x = *x + 1;
  if (p == 'o') *o = *o + 1;
}

char tttresult(string board) {
  string b = board;
  int x = 0, o = 0;
  for (int i = 0; i < 3; i++) {
    if (b.at(i) == b.at(i + 3) && b.at(i) == b.at(i + 6))
      XOincrementer(&x, &o, b.at(i));
    if (b.at(3 * i) == b.at(3 * i + 1) && b.at(3 * i) == b.at(3 * i + 2))
      XOincrementer(&x, &o, b.at(3 * i));
  }
  if ((b.at(0) == b.at(4) && b.at(0) == b.at(8)) || b.at(6) == b.at(4) && b.at(2) == b.at(4))
    XOincrementer(&x, &o, b.at(4));
  int numx = 0, numo = 0, numE = 0;  // num #
  if (tttboard.length() != 9) return 'e';
  for (int i = 0; i < tttboard.length(); i++) {
    if (tttboard.at(i) == 'x') numx++;
    else if (tttboard.at(i) == 'o') numo++;
    else if (tttboard.at(i) == '#') numE++;
    else
        return 'e';
  }
  if ((x >= 1 && numo == numx) || (o >= 1 && numx > numo) || (x && o) ||
    numo > numx || numx > numo + 1) return 'i';
  if (x == 0 && o == 0) {
    if (numE == 0) return 't';
    else
        return 'c';
  }
  if (x >= 1) return 'x';
  if (o >= 1) return 'o';
  return 'e';
}

char tttresult(vector<Move> board) {
  string res = "#########";
  for (auto & i : board) {
    if (i.r == 0) res.at(i.c) = i.player;
    if (i.r == 1) res.at(i.c + 3) = i.player;
    if (i.r == 2) res.at(i.c + 6) = i.player;
  }
  return tttresult(res);
}

string backtrack(int permutation) {
  string board = "#########";
  int counter = 0;
  while (permutation > 0) {
    switch (permutation % 3) {
    case 0:
      break;
    case 1:
      board.at(counter) = 'o';
      break;
    case 2:
      board.at(counter) = 'x';
      break;
    }
    counter++;
    permutation = permutation / 3;
  }
  return board;
}

vector<string> get_all_boards() {
  vector<string> boards;
  for (int i = 0; i < 19683; i++) boards.push_back(backtrack(i));
  return boards;
}

void ttt_tally() {
  map<char, int> tally;
  for (auto c : std::string("toxic")) {
    tally.insert({c, 0});
  }
  for (auto & board : get_all_boards()) {
    tally.at(tttresult(board))++;
  }
  for (auto const& pair : tally) {
    std::cout << pair.first << " " << pair.second << "\n";
  }
}

// This version of main interactively
// tests either:
//
//  string tttresult "s"
//  vector tttresult "v"
// or
//  get_all_boards "a"
//

// MAIN

int main() {
  int n;
  std::string board;
  Move m;
  std::vector<Move> moves;
  std::vector<std::string> boards;
  std::string asktype;

  while (std::cin >> asktype) {
    if (asktype == "v") {  // test tttresult vector
      moves.clear();
      std::cin >> n;
      for (int i = 0; i < n; i++) {
        std::cin >> m.r >> m.c >> m.player;
        moves.push_back(m);
      }
      std::cout << tttresult(moves) << "\n";
    } else if (asktype == "s") {  // test tttresult string
      std::cin >> board;
      std::cout << tttresult(board) << "\n";
    } else if (asktype == "a") {  // test get_all_boards
      boards = get_all_boards();
      for (auto b : boards) {
        std::cout << b << "\n";
      }
    } else if (asktype == "t") {  // test ttt_tally
      ttt_tally();
    } else {
      return 0;
    }
  }
  return 0;
}
