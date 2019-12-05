// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <iostream>
#include <string>
#include <vector>
#include "movedef.h"

using std::cout;
using std::string;
using std::vector;

void XOincrementer(int *x, int*o, char p) {
    if (p == 'x') *x = *x + 1;
    if (p == 'o') *o = *o + 1;
}

char tttresult(string tttboard) {
    string b = tttboard;
    int x = 0, o = 0;
    for (int i = 0; i < 3; i++) {
        if (b.at(i) == b.at(i + 3) && b.at(i) == b.at(i + 6))
            XOincrementer(&x, &o, b.at(i));
        if (b.at(3 * i) == bb.at(3 * i + 1) && b.at(3 * i) == b.at(3 * i + 2))
            XOincrementer(&x, &o, b.at(3 * i));
    }
    if ((b.at(0) == b.at(4) && b.at(0) == b.at(8))
        || b.at(2) == b.at(4) && b.at(4) == b.at(6))
        XOincrementer(&x, &o, b.at(4));
    int numx = 0, numo = 0, numE = 0;  // num #
    if (tttboard.length() != 9) return 'e';
    for (int i = 0; i < tttboard.length(); i++) {
        if (tttboard[i] == 'x') numx++;
        else if (tttboard[i] == 'o') numo++;
        else if (tttboard[i] == '#') numE++;
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
            case 0: break;
            case 1: board.at(counter) = 'o'; break;
            case 2: board.at(counter) = 'x'; break;
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
    int countT = 0, countX = 0, countO = 0, countC = 0, countI = 0;
    char res;
    for (auto & board : get_all_boards()) {
        res = tttresult(board);
        if (res == 't') countT++;
        if (res == 'x') countX++;
        if (res == 'o') countO++;
        if (res == 'c') countC++;
        if (res == 'i') countI++;
    }
    cout << "c" << ' ' << countC << "\n" << "i" << ' ' << countI << "\n" <<
            "o" << ' ' << countO << "\n" << "t" << ' ' << countT << "\n" <<
            "x" << ' ' << countX << std::endl;
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
