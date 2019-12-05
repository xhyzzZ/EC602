// Copyright 2019 Haoyu Xu xhy@bu.edu

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include "movedef.h"

using std::cout;
using std::string;
using std::vector;
using std::map;

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
        if (board[i] == board[i + 1] && board[i + 1] == board[i + 2]) {
            if (board[i] == 'x') xwon = true;
            else if (board[i] == 'o') owon = true;
        }
    }

    for (int i = 0; i < 3 ; i += 3) {
        if (board[i] == board[i + 3] && board[i + 3] == board[i + 6]) {
            if (board[i] == 'x') xwon = true;
            else if (board[i] == 'o') owon = true;
        }
    }

    if ((board[0] == board[4] && board[4] == board[8]) || (board[2] == board[4] && board[4] == board[6])) {
        if (board[4] == 'x') xwon = true;
        else if (board[4] == 'o') owon = true;
    }

    if (xwon && owon) return 'i';
    else if (!xwon && !owon) {
        if (countO + countX < 9) return 'c';
        else if (countO + countX == 9) return 't';
        else return 'e';
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
}

char tttresult(vector<Move> board) {
    string res = "#########";
    for (auto & i : board) {
        if (i.r == 0) {
            res[i.c] = i.player;
        } else if (i.r == 1) {
            res[i.c + 3] = i.player;
        } else {
            res[i.c + 6] = i.player;
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
                //do nothing
                break;
            case 1:
                board[counter] = 'o';
                break;
            case 2:
                board[counter] = 'x';
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
    map <char, int> tally;
    char res;
    vector<string> boards = get_all_boards();
    for (auto & board : boards) {
        res = tttresult(board);
        tally[res] += 1;
    }
    map<char, int>::iterator it;
    for (it = tally.begin(); it != tally.end(); it++) {
        cout << it -> first << ' ' << it -> second << "\n";
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
