// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <unordered_map>
#include "movedef.h"

using std::cout;
using std::string;
using std::vector;
using std::unordered_map;

char tttresult(string board) {
    vector<char> res;
    if (board.size() != 9) return 'e';
    for (char i : board) {
        if (i != 'o' && i != 'x' && i != '#') {
            return 'e';
        }
    }
    int countX = 0;
    int countO = 0;
    for (char i : board) {
        if (i == 'x') countX++;
        if (i == 'o') countO++;
    }
    int diff = countX - countO;
    if (diff > 1 || diff < 0) return 'i';

    bool xwon = false, owon = false;
    for (int i = 0; i < 9 ; i += 3) {
        if (board.at(i) == board.at(i+1) && board.at(i+1) == board.at(i+2)) {
            if (board.at(i) == 'x') xwon = true;
            else if (board.at(i) == 'o') owon = true;
        }
    }

    for (int i = 0; i < 3 ; i++) {
        if (board.at(i) == board.at(i+3) && board.at(i+3) == board.at(i+6)) {
            if (board.at(i) == 'x') xwon = true;
            else if (board.at(i) == 'o') owon = true;
        }
    }

    if (board.at(0) == board.at(4) && board.at(4) == board.at(8)) {
        if (board.at(4) == 'x') xwon = true;
        else if (board.at(4) == 'o') owon = true;
    }

    if (board.at(2) == board.at(4) && board.at(4) == board.at(6)) {
        if (board.at(4) == 'x') xwon = true;
        else if (board.at(4) == 'o') owon = true;
    }

    if (xwon && owon) return 'i';
    if (!xwon && !owon) {
        if (countO + countX < 9) {
            return 'c';
        } else if (countO + countX == 9) {
            return 't';
        } else {
            return 'e';
        }
    }

    if (xwon) {
        if (diff == 1) {
            return 'x';
        } else {
            return 'i';
        }
    }

    if (owon) {
        if (diff == 0) {
            return 'o';
        } else {
            return 'i';
        }
    }
    return 'e';
}

char tttresult(vector<Move> board) {
    string res = "#########";
    for (auto & i : board) {
        if (i.r == 0) {
            res.at(i.c) = i.player;
        } else if (i.r == 1) {
            res.at(i.c + 3) = i.player;
        } else {
            res.at(i.c + 6) = i.player;
        }
    }
    return tttresult(res);
}

string permutation(int permutation) {
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
    string board;
    vector<string> allBoards;
    for (int i = 0; i < 19683; ++i) {
        allBoards.push_back(permutation(i));
    }
    return allBoards;
}

void ttt_tally() {
    unordered_map <char, int> tally;
    char res;
    vector<string> boards = get_all_boards();
    for (auto & board : boards) {
        res = tttresult(board);
        tally[res] += 1;
    }
    unordered_map<char, int>::iterator it;
    for (auto x : tally) {
        cout << x.first << " " << x.second << endl;
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
