"tttanalyzer checker"
import unittest
import time
import logging
import subprocess as sub
import random
import os
import math
import random
import numpy as np
import itertools
import hashlib

from threading import Thread

from queue import Queue, Empty

VERSION, EC602VER = (2,8), (3,5)
DEBUG = False

def update_ec602lib():
    print('updating ec602lib')
    from requests import get
    r = get('http://curl.bu.edu/static/content/ec602_fall19/ec602lib.py')
    with open('ec602lib.py','w') as f:
        f.write(r.text)

def get_ec602lib():
    from os import listdir
    files = listdir();
    if "ec602lib.py" not in files:
        update_ec602lib()

    import ec602lib as e
    if e.VERSION < EC602VER:
        update_ec602lib()
        from importlib import reload
        e = reload(e)

    return e

ec602lib = get_ec602lib()


programs = ['tttanalyzer.cpp']

real_main=r"""
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
"""

popen_specs={'stdout':sub.PIPE,'stdin':sub.PIPE,'stderr':sub.PIPE,
'universal_newlines':True}


Boards= sorted(tuple("".join(b) for b in list(itertools.product('xo#',repeat=9))))

# all x,o,t are included
MapAnswer = {'xx##xoxxo': 'i', 'oooxx##x#': 'o', 'xoxxoo#ox': 'o', 'xxxo#oo#x': 'x', '#o##ox#xx': 'c', 'x#xooox##': 'o', 'o#xox#xox': 'x', '#oxxoxo#x': 'x', 'o#o#xoxxx': 'x', 'ooxxoxxo#': 'o', 'xx##x#ooo': 'o', 'ox#xoxoxx': 'i', 'xooxxo#xo': 'o', 'x#x##xooo': 'o', 'xxxo#o###': 'x', 'x#xoxoxo#': 'x', 'xxxoo#x#o': 'x', 'xxxo#x#oo': 'x', 'ox##o##o#': 'i', 'xox#o##ox': 'o', 'xooo####x': 'i', '#xx##xooo': 'o', '#oxo#oxxx': 'x', 'oxoxxx##o': 'x', 'xo#x#ox##': 'x', 'o#x#x#o##': 'c', '##xoxxxoo': 'x', '#xooo#xxx': 'x', 'xoxoo#x#x': 'c', '##xoxoxxo': 'x', '#o#xxxoox': 'x', 'xooxo#oxx': 'o', '#ox#oxoxx': 'x', 'xxoxooo#x': 'o', 'xxooxox#o': 'o', 'oxoox##xx': 'x', 'xo#ooxxox': 'o', '#ox#ox##x': 'x', 'xoo#x###x': 'x', 'xoox#xxo#': 'x', 'oxxo##ox#': 'o', 'xooxoxox#': 'o', 'oo#x#oxxx': 'x', '####ox#o#': 'i', 'oxo#oxxxo': 'o', 'xxx##o#o#': 'x', 'x#oxx#xoo': 'x', 'x#x#xoxoo': 'x', 'xoxoxo##x': 'x', 'xxoooxo#x': 'o', '#o#oxoxxx': 'x', 'xoxx#oxo#': 'x', '#oxox#xxo': 'x', 'ox#ooxoxx': 'o', 'xooxx##ox': 'x', 'xxoxo#x#o': 'x', '#oxo###o#': 'i', '##oxo#oxx': 'o', 'x##x#oxo#': 'x', 'x#ox#oxox': 'x', 'oxoxx#ox#': 'x', 'o#x#xoxxo': 'x', 'x#x#xooox': 'x', 'x#o#x##ox': 'x', '##x#xxo#o': 'c', '###oxooox': 'i', 'o##xoxx#o': 'o', 'x#xxxoooo': 'o', 'o#x##xo#x': 'x', 'ox#xooxxo': 'o', 'xooxxxxoo': 'x', '#xoxoooxx': 'o', 'xooxx#x#o': 'x', 'ooxxxoxxo': 'x', 'o#xo#x##x': 'x', '#xxxxxxoo': 'i', 'xxooxxoox': 'x', '#xxo#xoox': 'x', 'oxxxxooox': 't', 'x#xoooxox': 'o', 'xoxoooo##': 'i', 'o#oxo#xxx': 'x', 'oox#xox#x': 'x', '#xoxo#o#x': 'o', 'oxo#x#oxx': 'x', 'o#xx#xoox': 'x', 'ox#ox##x#': 'x', '#oox#oxxx': 'x', '#x#ooox#x': 'o', 'xo#ox#oxx': 'x', '#xoxx#xoo': 'c', 'o#o#ooxxx': 'i', 'x#oxoooxx': 'o', 'x#o#x#o#x': 'x', 'x#xxo#xoo': 'x', 'xxoxxo#oo': 'o', 'oxxxox#oo': 'o', 'oxxxo#oxo': 'o', '#oxxx##oo': 'c', 'oxxo#xo##': 'o', '#oxxxxo#o': 'x', 'xoxxo#oox': 'o', 'x#ooxox#x': 'x', 'x#xoooxxo': 'o', 'o#xoxo##x': 'c', 'xxx#o###o': 'x', 'xo##xooxx': 'x', '#xoxxx#oo': 'x', 'ooo#x#x#x': 'o', '#xoxxoxoo': 'o', 'xo#xox#o#': 'o', 'o#xx#o#ox': 'c', 'x###xxo#o': 'c', 'xoxoxox##': 'x', 'ooxxxoxox': 'x', 'x#o#xxoox': 'x', 'x##x##xoo': 'x', 'x#ooxxo#x': 'x', 'xxxox#o#o': 'x', 'xo#oxx##o': 'c', '#xoxx#oxo': 'x', 'xxoxoxxoo': 'x', 'o##xo#xxx': 'i', '#xxoxoox#': 'x', 'x#ooxo#xx': 'x', 'ooo##x#xx': 'o', 'xxoxoo#xo': 'o', 'oox#xxx#o': 'x', '#xoxo#ox#': 'o', 'oxo#o##xx': 'c', '#xxxxoooo': 'o', 'oxo#xxox#': 'x', 'xo##ox#ox': 'o', 'oo#ooooox': 'i', 'oox##x##x': 'x', 'o#xxo##xo': 'o', 'xoxooo#xx': 'o', '##o#oxoxx': 'o', 'xxoxooox#': 'o', 'xx###xooo': 'o', 'x##o#oxxo': 'c', 'oxoxxxoox': 'x', 'xoxoxoxxo': 'x', 'oxoxxxoxo': 'x', 'ooox###xx': 'o', 'xxxooxo##': 'x', 'xxooxooxx': 'x', 'oxxx#ox#o': 'c', 'xoooxxxox': 'x', '#xoxoxoxo': 'o', 'x#oox#xox': 'x', '#x#o#x#ox': 'c', 'xxxo#o#xo': 'x', 'o#xoxox#x': 'x', 'ooxo#xx#x': 'x', 'oox##oxxx': 'x', '#oxxxox#o': 'x', '#xo##oxxo': 'o', '#ox#xxxoo': 'x', '##o#o#xxx': 'x', 'xoxox#xo#': 'x', 'o#x#o#xxo': 'o', 'o#oxxxx#o': 'x', 'xo#oo#xxx': 'x', 'ox#xo##xo': 'o', 'x#o#oxox#': 'o', 'o#xo#oxxx': 'x', '#xoxoxoox': 'o', 'o#xoo#xxx': 'x', 'xxoxoox##': 'x', 'oxx#oo#oo': 'i', '#oxxxxoo#': 'x', 'xoo#x#xox': 'x', '#x##xoox#': 'x', 'o#o#oxxxx': 'x', 'o#x##x#ox': 'x', '#o#xxoxox': 'c', 'oxxox#x#o': 'x', 'xo#ox#xox': 'x', 'o##xooxxx': 'x', 'xooxo#xx#': 'x', 'xxooo#oxx': 'o', '#xxooo#x#': 'o', 'oxooxxo#x': 'o', '##ooxoxxx': 'x', 'o#ox#xxox': 'c', 'xooox##xx': 'x', 'o#xo#xox#': 'o', 'xoxoxxoxo': 't', '#xooxx#xo': 'x', '#ox##xo##': 'c', 'o#x#x#x#o': 'x', '###oo#xxo': 'i', 'xxxo##xoo': 'x', 'xoxxx#ooo': 'o', 'o#oox#xxx': 'x', '#ooxoxxox': 'o', 'oxoxxx#o#': 'x', 'x#oxoxxo#': 'x', '#ooxxx###': 'x', 'oooxoxoo#': 'i', 'x#xx#oxo#': 'i', 'oo#x#ox#x': 'c', '#xxxoxoo#': 'c', 'xxxxoo##o': 'x', 'oxo#xx#xx': 'i', 'o##xxxxoo': 'x', '#xxoooxxx': 'i', 'o##xx#xxx': 'i', '#ox#oxxo#': 'o', 'x#xoxo#ox': 'x', 'ox##oxx#o': 'o', 'ox#xoxxoo': 'o', 'oo#ox#xxx': 'x', 'xoooxx##x': 'x', 'ox##xooxx': 'x', '#oxoo#xxx': 'x', '#xx#o#ooo': 'i', '##x##xoox': 'x', '#ooxxx#ox': 'x', 'xxxoxooxo': 'x', 'o#o#xxoxo': 'i', 'o###o#xxx': 'x', '#o##o#xxx': 'x', 'xxoxooxox': 'x', 'oxo#o#x##': 'i', '#o#xooxxx': 'x', 'xo#xxx#oo': 'x', '##oxxxxoo': 'x', 'xxox#o###': 'c', '##oooxxxx': 'x', '##xoxoxox': 'x', 'ooox#xxxo': 'o', 'oooxox#xx': 'o', '##oxxxo##': 'x', 'oxx#xoox#': 'x', '#xx#xoxoo': 'x', 'xoxoox##x': 'x', 'oo#o#xxxx': 'x', 'o#oo#xxxx': 'x', 'xox#x#oox': 'x', '##xxx#ooo': 'o', 'xox#xo#ox': 'x', 'xo#xxo###': 'c', 'xx#xooxo#': 'x', 'o#xxox##o': 'o', 'o#oxooo#o': 'i', 'x#o#ox#ox': 'c', 'oxxo#xoxo': 'o', '#xo#oxo#x': 'o', '##xx#xooo': 'o', 'x#oxoxoxo': 'o', 'xxx###o#o': 'x', 'x#xooooxx': 'o', '#oxox#x##': 'x', '#o#x#o#xx': 'c', 'xoxo#xo#x': 'x', 'ooxx#xo#x': 'x', 'xxooxxoxo': 'x', 'o#xxxxoo#': 'x', '#oxxo#xo#': 'o', '#oxxo#x#o': 'c', 'oox#x#xxo': 'x', 'oxoxoxxox': 't', 'x#o#xoxox': 'x', 'xxo####o#': 'c', '#xo#xo#x#': 'x', '##oo##xxx': 'x', 'xo#xx#xx#': 'i', 'ooxxxx#o#': 'x', 'o#oxxxxo#': 'x', 'xoo#xox#x': 'x', 'x##oxx#o#': 'c', '#xoo#ooo#': 'i', 'xxoox#o#x': 'x', 'oo#xxxox#': 'x', 'xo#xxoxo#': 'x', 'oo#xxoxxx': 'i', 'xo##oxxxo': 'c', 'ooxxxxoox': 'x', '#xo#x##xo': 'x', 'xx##xooxo': 'x', '##xo#x#ox': 'x', 'oooxx#oxx': 'o', 'xxxo##oox': 'x', 'oxxoxoo#x': 'o', '#ox##x#ox': 'x', 'oxoxxooxx': 'x', '##oxxx##o': 'x', 'x#ox##x#o': 'x', 'ox#o#xo#x': 'o', 'oxxo#ooxx': 'o', '#xx#x#ooo': 'o', 'oxxox#xo#': 'x', 'o#xxoxxoo': 'o', 'xxoo##oxx': 'c', 'xo#o#oxxx': 'x', 'xo#xoxx#o': 'x', 'o##ooxxxx': 'x', 'oxxxo#xoo': 'o', 'x#xx##ooo': 'o', 'xoxxo#x#o': 'x', 'xo#ox###x': 'x', 'xxx#oox#o': 'x', 'ooxo##xxx': 'x', 'x#oxo#o#x': 'o', 'o##oxoxxx': 'x', 'xxo#xo##o': 'o', '#o##oxxox': 'o', 'oooxoxxx#': 'o', 'oxxxoxoox': 'x', '#xo#oxox#': 'o', '##oxoxox#': 'o', 'xo#oxo#xx': 'x', 'x#oxxx#oo': 'x', 'ooox#x##x': 'o', '#oxxxoxox': 'i', '#xx#oxoox': 'x', 'oxx#oxxoo': 'o', 'xxx#oo##x': 'i', '##xox#x#o': 'x', '#oo###xxx': 'x', 'xox#xoxo#': 'x', '#x#x#xooo': 'o', 'xxxxo#o#o': 'x', 'xo#xo#x##': 'x', 'xx#xoox#x': 'i', 'oxoxoxox#': 'o', 'xoxo#x#o#': 'c', '###xooxox': 'c', '#x#oxoxox': 'c', 'xxx#o#oox': 'x', 'oo#xoxxxo': 'o', '#oxoox#xx': 'x', 'xo#x#oxox': 'x', 'xxo#o#ox#': 'o', 'oxoo##xxx': 'x', 'ox##ox#x#': 'c', 'xoox#ox#x': 'x', 'ooo#xx#x#': 'o', '#ox#xoxxo': 'x', 'oxoxox#xo': 'o', 'xxo#xxooo': 'o', 'o#x#oxx#o': 'o', 'ooxox#x#x': 'x', 'xxxxo#oo#': 'x', '##x#x#xoo': 'x', 'xoxoxooxx': 'x', 'ox#oxoxx#': 'x', '##xoooxo#': 'i', 'oox#xoxx#': 'x', 'xxooxoxox': 'x', 'ooo#x#xx#': 'o', '#xoxxxo#o': 'x', '##xooxxox': 'x', '#oxooxx#x': 'x', 'ooxxxox##': 'x', '#ooxxxxo#': 'x', 'oo#xxx#xo': 'x', 'oo#xo#xxx': 'x', 'xxxxooo##': 'x', 'oxx##xoo#': 'c', 'ooxoxxx##': 'x', 'xo#oxox#x': 'x', 'oxx#xox#o': 'x', 'xooxxxoox': 'x', 'x#o#oxo#x': 'o', 'o#o###xxx': 'x', '#xoxxo##o': 'o', 'ooo#xxxxo': 'o', '#ox#x#x#o': 'x', '#xxoxo#ox': 'c', 'x#o#xxxoo': 'c', 'xo##xoxox': 'x', 'oxx#xoxo#': 'x', 'oox#o#xxx': 'x', 'ooxxxooxx': 't', 'xxxox#oo#': 'x', '#ooxxxox#': 'x', 'ooxoxxxxo': 'x', 'o#xxooxxo': 'o', 'x#xoxoo#x': 'x', 'x#x#oxoox': 'x', 'x##xo#xo#': 'x', '#oo#xoooo': 'i', 'xxxo####o': 'x', 'o#ox##x#o': 'i', '#oxoxox#x': 'x', '#xoooxxox': 'c', '#xxooox##': 'o', '#xo#xooxx': 'x', 'xo###ooxx': 'c', 'o#oxxx#ox': 'x', 'o##o##xxx': 'x', 'oxoxo#xxo': 'o', '#xxxoxooo': 'o', '##xoxxoox': 'x', 'oxxoox##x': 'x', 'oxoxxox#o': 'o', '##oo#xxox': 'c', 'oxx#ox##o': 'o', 'x#xox#oox': 'x', 'x#oxxoxo#': 'x', 'o#oxxxox#': 'x', 'xxxoxoxoo': 'x', 'x#o#xo#xo': 'o', 'xxx#xooo#': 'x', '#oxxxoxo#': 'x', 'xxx#oxo#o': 'x', '#xoooxoxx': 'o', 'x#xoxxooo': 'o', 'oox#ox#xx': 'x', 'xxo##ox#o': 'o', 'ox#xxxo#o': 'x', 'oxooxxxxo': 'x', 'oxox#oxxo': 'o', 'xxo#o#o#x': 'o', 'o#xxxxo##': 'i', 'xxxoxo#o#': 'x', 'xxo#x#oox': 'x', '##xxoxoox': 'x', '#ox#x#xo#': 'x', 'x#xx#oxoo': 'x', 'ox##ooxxx': 'x', 'o#x#ooxxx': 'x', 'xoxoooxx#': 'o', '##o#x#x##': 'c', 'xx#oxo#xo': 'x', 'x#oxo#xxo': 'x', 'x##xo#x#o': 'x', 'ox#oxxoox': 'o', '#xxoooxox': 'o', '##oxoxo#x': 'o', 'oxxxoxo#o': 'o', 'xxoxoxoo#': 'o', 'xxxoo##ox': 'x', 'ox#ooxxxo': 'o', '#ooxxxx#o': 'x', '##x#oooxx': 'c', '##oxxxoxo': 'x', 'oxx##xoox': 'x', '#x#xx#xoo': 'i', 'o#oox####': 'i', 'xxxooxoxo': 'x', 'xxx###oo#': 'x', '#oxxoxxoo': 'o', 'ooxxo#xxo': 'o', 'oo#x##oo#': 'i', '##ox#oxxo': 'o', 'oxx#x#oxo': 'x', 'o#xxoxo#x': 'x', 'ooo#xx##x': 'o', 'xox#ooxox': 'o', 'xxox#ooxo': 'o', 'xo##xxoxo': 'c', 'xooo##xxx': 'x', 'xooxxxoxo': 'x', 'o##xo#xxo': 'o', 'xxoxo#o##': 'o', 'xxxo#xo#o': 'x', 'o#x#oxxox': 'x', '###xxx#oo': 'x', 'ox##xoxxo': 'x', 'o###oxxxo': 'o', '#oxoxxo#x': 'x', 'xxx#o#oxo': 'x', 'oo####xxx': 'x', 'ooox##xx#': 'o', 'oxxoo#xxo': 'o', '####ooxxx': 'x', '##xooxoxx': 'x', '##o#xoox#': 'i', 'xxx#oo#ox': 'x', 'xxox#xooo': 'o', 'xxoooxxox': 't', '#xoox#oxx': 'x', 'xo#oxx#ox': 'x', 'xox#o#xo#': 'o', 'xxxoxo##o': 'x', 'oxoxxxxoo': 'x', '#xo#ooxxx': 'x', 'xo##x##ox': 'x', 'xoox##xox': 'x', 'xooxoxxxo': 'x', '###o#oxxx': 'x', 'o##o#xoxx': 'o', 'oxxoxxoo#': 'o', 'x#xoox#ox': 'x', '#oxx#xoox': 'x', 'o#xoxo###': 'i', 'x#xooxo#x': 'x', 'xo#x##xo#': 'x', 'x#o#o#oxx': 'o', 'xxoxo#oox': 'o', 'xoxoxoxox': 'x', 'xx#ooo#x#': 'o', 'xxo###xxo': 'i', '##ox###x#': 'c', 'xx#oxo#ox': 'x', 'oxxoxoxox': 'x', '#xxoxxxox': 'i', 'ooxxxxxoo': 'x', 'x#oo#oxxx': 'x', 'xxo#xoox#': 'x', 'xoox#oxx#': 'x', 'oxxxxooxo': 'x', 'ox#xxoox#': 'x', '#o#xxxo##': 'x', '#xxooooxx': 'o', 'o#xo#xxox': 'x', '#oxxooxox': 'o', 'xxoooxox#': 'o', 'ooox#xxox': 'o', '#o#o##xxx': 'x', 'ooxox#oxx': 'o', 'x#ox#xxoo': 'x', '#xxooxo#x': 'x', 'o#xoxxxo#': 'x', 'xo##oxxo#': 'o', 'xxxx#oo#o': 'x', 'xxoooox#x': 'o', 'xxxo#o#ox': 'x', '##x#xxooo': 'o', 'xo#o#oooo': 'i', 'o#xxxoxo#': 'x', 'xooxxx#o#': 'x', '#oxoxoxx#': 'x', 'ox##xxoxo': 'x', 'o#oxxx###': 'x', 'xxx##ooxo': 'x', 'xo#x##x#o': 'x', 'oo#oxxoxx': 'o', 'ooxxoxx#o': 'o', '#xxoox#ox': 'x', 'x#oooxoxx': 'o', '#xxxooxo#': 'c', 'oxxxoox#o': 'o', '#xoox#xxo': 'x', 'xo##ooxxx': 'x', 'oooxxoxx#': 'o', '#ox#ooxxx': 'x', 'xo#xo###x': 'c', 'ox#xxxoo#': 'x', '#ooxxx#xo': 'x', 'ooxoxxox#': 'o', 'xoxx##xoo': 'x', '#oxoxxx#o': 'x', 'oo#xxx#ox': 'x', '#xxo#ox#x': 'i', 'x#xooo#x#': 'o', 'xo#xxo#ox': 'x', 'ox#oxxo##': 'o', 'o#ox#oxxx': 'x', 'oxx#o#x#o': 'o', '#xoox##x#': 'x', 'ox#oo#xxx': 'x', 'oxo#xoxx#': 'x', '#x#ox##xo': 'x', '###xxxoo#': 'x', '#o#xxxoxo': 'x', 'xx#xoxooo': 'o', 'xxx#xo#oo': 'x', 'x##xxooox': 'x', 'ox#xx#oxo': 'x', '#ox##xxoo': 'c', 'oooxx###x': 'o', 'o#xx##x#o': 'c', 'o#xoxooxx': 'o', 'oxooxoxxx': 'x', 'xoxxoooxx': 't', 'o##ox#oxx': 'o', 'o#xoxxo##': 'o', 'o#oxoxxxo': 'o', 'xo#xoxoox': 'o', '##x#oxo#x': 'x', '#xo#xxoxo': 'x', 'o####oxxx': 'x', 'xx#oooxox': 'o', '#x#oxo#x#': 'x', 'xxxoo##xo': 'x', 'x#oxx#oox': 'x', 'oxxo##o#x': 'o', 'xx#oooxxo': 'o', 'o#xxo#x#o': 'o', 'xxoo#oxxo': 'o', 'xxxoxxx#x': 'i', '#x#xxooxo': 'x', 'oxooox#oo': 'i', 'xxxo##o##': 'x', '#ooo#xxxx': 'x', '#xxoxo#xo': 'x', 'xxxoo####': 'x', 'xxx#oo#xo': 'x', '#xo##xx#o': 'c', 'oxoxo#oxx': 'o', 'x#ox##xo#': 'x', 'xx#x#oxoo': 'x', 'o#x#xoxox': 'x', 'x##xooxxo': 'x', 'o#xooxxxo': 'o', '##o#xx#o#': 'c', 'x#x#x#ooo': 'o', '##ooox###': 'i', '###xxxo#o': 'x', 'xx#xxo##o': 'i', 'x##x#ooxx': 'i', 'oxxxo###o': 'o', 'oxxox#oox': 'o', 'xxox##xo#': 'i', '#xxox#xoo': 'x', 'xxo#ooxxo': 'o', '#xo#xox#o': 'o', 'oox#oxx#x': 'x', 'xoxxxooxo': 't', 'xx##xooox': 'x', 'o##xxxoxo': 'x', '#x##xo#xo': 'x', 'xo#xx#xoo': 'x', 'x#oxxo##o': 'o', 'oxxx#o#ox': 'c', 'o#xoxxoxo': 'o', 'x##x#xooo': 'o', 'o#ox###x#': 'c', 'o#x#x#xo#': 'x', 'xoxox#o#x': 'x', 'oooo#ooxx': 'i', 'o###o##o#': 'i', 'xoxoxxxoo': 'x', 'ox#ox####': 'c', 'xoo##oxxx': 'x', 'x#oxoox#x': 'x', 'o#xoxxxoo': 'i', 'xxoox#ox#': 'x', '#oxoxxxo#': 'x', '#o##oxo##': 'i', '#o#ooxxxx': 'x', '#xoo#xox#': 'c', 'xo#oxxo#x': 'x', 'oxo#o#xxx': 'x', 'xxx#ooxo#': 'x', '#ooxxxo#x': 'x', 'oox#xx#ox': 'x', '#xxoxox##': 'i', 'o#oxoooxo': 'i', 'xoxooxxxo': 't', 'xx#oxoooo': 'i', 'x#oxoxo##': 'o', 'xxx##oxoo': 'x', 'x#xoxox#o': 'x', 'o##oxxo#x': 'o', 'xooox#x#x': 'x', 'ox##o#xxo': 'o', 'xxxooxxoo': 'x', '#o###oo#o': 'i', 'xxxxoo#o#': 'x', 'xxx#o#xoo': 'x', 'xxxooxoox': 'x', 'ooxxxxo##': 'x', 'oxxooxox#': 'o', 'oxxooo#xx': 'o', '##xoox##x': 'x', 'o#xxoxoxo': 'o', 'xx#xxoooo': 'o', 'xooxxooxx': 'x', 'xox#oxo#x': 'x', 'x###x#oox': 'x', 'xx#ooox##': 'o', 'x#oox###x': 'x', 'ooxxooxxx': 'x', 'oox#oxxxo': 'o', 'xo#xx#oox': 'x', 'x#ooxox##': 'c', 'x#oxxoo#x': 'x', 'o#xxxox#o': 'x', 'oxxoxxo#o': 'o', 'oxo#o#o##': 'i', 'ooo#xxxox': 'o', 'x##ooox#x': 'o', 'oxxxooxox': 't', '#ox##xo#x': 'x', 'oxo#x##x#': 'x', '#x#ooo#xx': 'o', 'xooxoxo#x': 'o', 'xxx#oo###': 'x', '###xoxox#': 'c', 'o#xxox#ox': 'x', 'oxxox#o##': 'o', 'xx#oxxooo': 'o', 'xooxxx##o': 'x', 'xxo#oooxx': 'o', 'oxo#xx#xo': 'x', 'xo##oo#xo': 'i', 'oox##xxox': 'x', 'xxoxo#oxo': 'o', 'oox##xx#o': 'c', 'oox##xox#': 'c', 'ox#oxx#xo': 'x', '#oooo#ox#': 'i', 'oxoo#xoxx': 'o', '##xo#xo#x': 'x', 'xoxoxxoox': 'x', '#oxoxxxxo': 'i', 'xoxox#o#o': 'i', 'o##x###x#': 'c', 'ox#o##oxx': 'o', 'o#oxx#xxo': 'c', 'o#xox#x##': 'x', 'xxox##xoo': 'x', 'xxxoo#xo#': 'x', 'xoxxoxoxo': 't', 'x#oox#oxx': 'x', 'oxx#o##xo': 'o', '#xxoxoxo#': 'x', 'xox#ox#o#': 'o', 'ox#xoxoxo': 'o', 'oxo#x#xxo': 'x', 'ooxo###o#': 'i', 'ooxoxoxxx': 'x', 'xo##xxoox': 'x', 'x##xoxxoo': 'x', 'xxxox##oo': 'x', 'oxxxooo#x': 'c', 'xox##ox##': 'c', 'ooo#xxoxx': 'o', 'oxoxoxo#x': 'o', 'xo##xo#xo': 'c', '#oxxxxo#x': 'i', 'o#xoxx#ox': 'x', 'xoxooxoxx': 'x', 'oox#x#xox': 'x', 'xxxxooxoo': 'x', 'oooxx#x##': 'o', 'xxoxxoo#o': 'o', '#oxoo#oo#': 'i', 'x###xo#ox': 'x', 'ooooxx#xx': 'o', '#xoxxxoo#': 'x', 'xx#ox#oox': 'x', 'xooxxxo##': 'x', 'o##xxx##o': 'x', 'o##xxxoox': 'x', '#xxoxxooo': 'o', 'ooooxxxx#': 'o', 'xxox#oxo#': 'x', '#o#xxx##o': 'x', 'o##o##xx#': 'c', 'xxx#xoo#o': 'x', 'oo#xoxxox': 'o', 'xoo#x#oxx': 'x', 'xxxo#oox#': 'x', '#oxo#xoxx': 'x', 'x####oo#x': 'c', '#ooox#xxx': 'x', 'ooox#ox##': 'i', 'xxxxoooxo': 'x', 'oo##x#x#x': 'c', 'oxoox#xx#': 'x', 'x#ooo#xxx': 'x', '#oo#oxxxx': 'x', 'xo##oxo#x': 'c', '#xxooo##x': 'o', 'xo#xxxo#o': 'x', '#oxox#xox': 'x', 'o#xox#o#x': 'o', 'xooxxxoxx': 'i', 'oxx#xo#xo': 'x', 'xoo#oxxox': 'o', 'x#oxxooxo': 'o', 'ox#ox#xxo': 'x', '#ox#o#xox': 'o', 'x#xox#xoo': 'x', 'o#xo##oxx': 'o', 'ooox#xoxx': 'o', 'x#o##oxxo': 'o', '#xx#xooxo': 'x', 'xxx##o##o': 'x', 'xxx##oo##': 'x', '##xoooxx#': 'o', 'xo#xoox#x': 'x', 'xoxoo#xox': 'o', '###oo#xxx': 'x', 'oxoxxo#x#': 'x', 'x##oxooxx': 'x', '#x#ox#ox#': 'x', 'xxoooxxxo': 't', 'xooxox#ox': 'o', 'ooooxxx#x': 'o', 'o#xoox#xx': 'x', 'xooxooxxx': 'x', 'xoxxxooox': 'x', 'xxooxo##x': 'x', '##xxxoxoo': 'x', 'ox#ox#o#x': 'o', '#xoo#oxxx': 'x', '####o#xx#': 'c', 'xox#xox#o': 'x', 'xooxx#xo#': 'x', 'ooxxoxoxx': 'x', 'oxxooox#x': 'o', '#x#oxxoxo': 'x', 'xxx#ooox#': 'x', 'xoo#o#xxx': 'x', 'oo#xox#ox': 'i', 'x##ox#o#x': 'x', 'oxxoxoxxo': 'x', 'xxooox#x#': 'c', 'oxx#ooxxo': 'o', 'x#o###ox#': 'c', 'xxox#o##o': 'o', 'oooxxxxox': 'i', 'oxx#x#xoo': 'x', '#xo#x#ox#': 'x', '#x#xx#ooo': 'o', 'oxo#xx###': 'c', 'xoxox#x#o': 'x', 'oxxo#xxo#': 'c', 'o##xox#xo': 'o', 'xooxxox##': 'x', '#x#oxooxx': 'x', '#o#xo#xox': 'o', 'xx###xx#x': 'i', 'oxxoxxxoo': 'x', 'xo#xxoo#x': 'x', '###xoooox': 'i', 'xoooxxoxx': 'x', 'x#oo#o#ox': 'i', 'xxxo#ox#o': 'x', 'xxoooo#xx': 'o', 'xo#oo##ox': 'i', 'o#oxxoxxo': 'o', '#xxx##ooo': 'o', 'o#oxoxoxx': 'o', '#ooxxoxxo': 'o', 'xxxx#o#oo': 'x', 'x#ooxoxxo': 'o', '#oxxx#xoo': 'x', 'oxxox##xo': 'x', '#xox#o#xo': 'o', 'xooooxxxx': 'x', 'xoo#xx#ox': 'x', 'ooxox#xx#': 'x', 'ooxoxxxox': 'x', 'xxo#xoo#x': 'x', '#x##xxooo': 'o', '#xoxoxo##': 'o', 'o#xox#xxo': 'x', 'oooxxox#x': 'o', 'xxooooxx#': 'o', 'oox#xxxo#': 'x', 'oxox#xo##': 'c', 'xxoxoxo#o': 'o', 'x#o#xooxx': 'x', 'o#x#ox#xo': 'o', 'xxoxx#ooo': 'o', 'ox#xox##o': 'o', 'o##xxx#o#': 'x', 'xoox#xx#o': 'x', 'xoooxxxxo': 't', '#xxoxox#o': 'x', 'xxxoxooox': 'x', 'oo#xxxx#o': 'x', 'xo#oxoxxo': 'c', 'ooxoxx##x': 'x', 'xooxxoxox': 'x', 'xoxox##ox': 'x', 'x###o#xo#': 'c', 'o#xoxxx#o': 'x', '###o###oo': 'i', '#x#oxoxxo': 'x', '##oxxxoox': 'x', 'o#oxxx#xo': 'x', 'xx#x#xx##': 'i', 'ox#oxo#xx': 'x', 'xo#oxxxo#': 'c', 'x#ox#ox##': 'x', 'o#xxx#xoo': 'x', 'oxxxx#ooo': 'o', 'ox#o#xox#': 'o', 'xox#x#xoo': 'x', '##x#xoxo#': 'x', 'xoo#xxo#x': 'x', 'xx#x##ooo': 'o', '#ox#xox##': 'x', 'oxooxx#x#': 'x', 'oxx#ox#ox': 'x', '#x##x#oxo': 'x', 'o#ooxxoxx': 'o', 'oo##xoxxx': 'x', 'xxx####oo': 'x', 'x#xxoxooo': 'o', 'oox#xxo#x': 'x', '#oxo#xxox': 'x', '#oxo#x##x': 'x', 'xx#oxoox#': 'x', '#o#xxxxoo': 'x', '#xo#xx##x': 'i', 'oox##xoxx': 'x', 'x##xoox##': 'x', 'ooo#xxx##': 'o', 'x##o##o#x': 'c', 'xox#oxxoo': 'o', 'x##oxoxox': 'x', 'xoxxooxxo': 'x', 'x#oxxxoo#': 'x', 'x##x#ox#o': 'x', 'ooxxx#xo#': 'x', '#x#oxxxoo': 'c', 'xoxx#ox#o': 'x', 'o#x#oxxo#': 'c', 'ooo#x##xx': 'o', 'oxooxxxox': 't', 'x#o###oox': 'i', 'oxoooxxxx': 'x', 'xo#xooxx#': 'x', 'oxo#xo#xx': 'x', 'ox##ox#xo': 'o', 'xx#xo#xoo': 'x', 'xooxx#o#x': 'x', 'x#o#xox#o': 'o', 'ooox##x#x': 'o', 'x#oxoxx#o': 'x', '#x#x##o##': 'c', 'xxxo###o#': 'x', '#xox#ox#o': 'o', 'xo##x#o#x': 'x', 'xo#xo#xxo': 'x', 'xxxoxoo##': 'x', 'xoo####x#': 'c', '#o#xxx#o#': 'x', '##xooo#xx': 'o', '##oxxo#xo': 'o', 'xxo#oxo##': 'o', 'x#xxoox#o': 'x', 'xxo#xoxoo': 'o', 'x#oxo#x##': 'x', 'ox#o#oxxx': 'x', '#xooxo#xx': 'x', '###o#####': 'i', 'xxxoox##o': 'x', 'xoxxoxoo#': 'o', 'xo#xxox#o': 'x', 'x##oooxx#': 'o', 'o##oxooox': 'i', 'xxxoox#o#': 'x', 'x##ox##ox': 'x', 'x#oxooxx#': 'x', 'oxoxx##xo': 'x', 'oo####x#o': 'i', 'x#xooo##x': 'o', 'xox#xxooo': 'o', '##x#ox#ox': 'x', '#ox#xoxox': 'x', 'x#oxoxoox': 'o', 'x##ooo#xx': 'o', 'x#xo##o##': 'c', 'oo##oxxxx': 'x', 'xxxxoooox': 'x', 'xoox##xxo': 'x', 'oxoxoxx#o': 'o', 'xoxxo##o#': 'o', 'ooxx#x#ox': 'x', 'oooxxo#xx': 'o', 'xxxxo##oo': 'x', 'xx#oxoo#x': 'x', '#x#x##xoo': 'c', 'oooxx#xox': 'o', '#xooxxox#': 'x', '#xoxooxxo': 'o', '##oxxx#o#': 'x', 'oxxx#xooo': 'o', 'xxxx#oxo#': 'i', 'x##xoxoo#': 'c', 'x#oxo#xox': 'x', 'xxooxo#x#': 'x', 'oooxx#xxo': 'o', 'oxxoox#xo': 'o', 'oxxo#x#ox': 'x', 'x##oxxoox': 'x', 'ooxooxxxx': 'x', 'o#xox#ox#': 'o', 'oo#xxxo#x': 'x', 'o#xoxoxx#': 'x', '#x#oox#x#': 'c', 'xoxxoox##': 'x', '#oxxo##ox': 'o', 'xoo#xo#xx': 'x', 'o#oxxxo#x': 'x', '#oox#oxoo': 'i', 'xox#xoo#x': 'x', 'o#oo####x': 'i', 'oxx#xxooo': 'o', 'xxx#o##o#': 'x', 'xoo#oo#o#': 'i', 'oxo#oxoxx': 'o', 'xoxxox#oo': 'o', 'xxo#oxoxo': 'o', 'x#xxooxo#': 'x', '#o###oxxx': 'x', 'oxoxxoxox': 't', 'oxxxoo#xo': 'o', 'o##oxxox#': 'o', 'xxo#oxoox': 'o', '##x#xox#o': 'x', 'xxoxxooox': 'x', '#o#xox#ox': 'o', '##o##oxxx': 'x', '#o##oooox': 'i', 'xxooxxxoo': 't', 'xoxxxo#oo': 'c', 'x#oxo#ox#': 'o', 'xoxxxoxoo': 'x', 'ooox#x#x#': 'o', 'xxx#ox#oo': 'x', 'xxoxo#xo#': 'x', 'xxoxxoxox': 'i', 'x###xxooo': 'o', '#xoxxoox#': 'x', 'ooxxox##x': 'x', '##xox#xo#': 'x', 'x#xo#xoox': 'x', 'ooo##xx#x': 'o', 'xo##xo##x': 'x', 'o#xxxxo#o': 'x', '#ooxoxoxx': 'o', '#oxxxx#oo': 'x', 'oox#x#x##': 'x', '##oxooxxx': 'x', 'ox##xo#x#': 'x', '##o#xoxxo': 'o', 'x##xooxox': 'x', 'xoo#ooxx#': 'i', 'o#x#xox##': 'x', 'ooxo#xxx#': 'c', 'xxx#o#o##': 'x', '#oooooooo': 'i', 'ox#xxo#xo': 'x', 'xoxo#x#ox': 'x', 'xooxo#x#x': 'x', 'o#x#oxoxx': 'x', 'x#xoox###': 'c', 'oxx#oxo#x': 'x', 'ooo##xxx#': 'o', 'oxxoxox##': 'x', 'xoxx#xooo': 'o', 'xxo##o#xo': 'o', 'ox#x#oooo': 'i', 'xooxxo##x': 'x', 'x##oxo##x': 'x', 'xxxo##oxo': 'x', 'oxoxxxo##': 'x', 'x#o#ooxxx': 'x', 'oox#xoooo': 'i', '##xx#o#xo': 'c', 'xoooxoxxx': 'x', '#oxxox#o#': 'o', 'o#oxox##x': 'c', 'xxxo#oxo#': 'x', 'x#oxxo#ox': 'x', 'xo#x#oxxo': 'x', 'x##xx#ooo': 'o', 'x#o#xo##x': 'x', 'xo#xo##ox': 'o', 'xo#x#xxoo': 'x', 'oxo##oxxx': 'x', 'oooooox#x': 'i', 'o#oxx#ox#': 'c', 'oo#o#xx#o': 'i', 'oo#x#x###': 'c', 'oxoxooxxx': 'x', 'o#x#ox##x': 'x', 'xoxooxxo#': 'o', 'oo#xxx###': 'x', 'xxoox##xo': 'x', '#x##xoo#x': 'c', 'xoo#xoxxo': 'o', 'xoo#oxoxx': 'o', 'o#ooxxxxo': 'c', 'ooox#xx##': 'o', '#xo#o#oxx': 'o', 'oxxooxxox': 'x', 'ox#xox#oo': 'i', 'xxxoo#o#x': 'x', '#oxoxxox#': 'c', 'ox#xo#x#o': 'o', '#xxxooxx#': 'i', 'ooxx#x##x': 'i', '#oo#xoxxx': 'x', 'xoox##x##': 'x', 'ooxxo#xox': 'o', 'xoo###oxo': 'i', 'xxo#xo#ox': 'x', 'xxx#oxoo#': 'x', '#oxoxx#ox': 'x', 'x#ox#o#xo': 'o', '#xooxoxx#': 'x', 'x###xoo#x': 'x', '#ooxo#xxx': 'x', 'x#ooxxoo#': 'i', 'oxxoxo#x#': 'x', 'x#ooxx#ox': 'x', 'o#xxxx#oo': 'x', 'ox#xxx#oo': 'x', 'xox##xoox': 'x', 'xo##o#xox': 'o', 'oxoooo##x': 'i', 'xxxx#ooo#': 'x', 'o#o##oxox': 'i', 'ooxxox#xo': 'o', 'xxxo#xoo#': 'x', '#ox#xxoox': 'x', '##xooox#x': 'o', 'xxoox##ox': 'x', 'o#x#xxxoo': 'x', 'xxo#x#oxo': 'x', 'ooxxxxoxo': 'x', 'o#xooxx#x': 'x', 'xooxoxx##': 'x', 'xxx##ooox': 'x', '#x#oooxx#': 'o', 'oxxoooxx#': 'o', 'oxxooxx#o': 'o', 'xx#ooooxx': 'o', 'x##xoxo#x': 'i', 'x##oooox#': 'i', 'xo#xxxoo#': 'x', '#xxox#oxo': 'x', 'oxxoo#oxx': 'o', '##oxxox#o': 'o', 'oox##oxx#': 'c', 'xx#ooo##x': 'o', 'xoxooox#x': 'o', '#xxxooo##': 'c', '##xoxox##': 'x', 'oxxxoooxx': 't', 'ox##x##xo': 'x', 'oo#xxxxo#': 'x', 'o#xx##oox': 'c', 'oxxxxoxoo': 'x', 'x#oxxxo#o': 'x', 'xxxoo#ox#': 'x', 'xx#xoox#o': 'x', '#xo##o##x': 'c', 'ooxxxx##o': 'x', 'xox#ox###': 'c', 'ooxxx##xo': 'c', 'ox##x#ox#': 'x', 'xxx#ooo#x': 'x', 'ooxxx#x#o': 'x', 'x##xxoxoo': 'x', 'ooxo#x#xx': 'x', '#xxoooxxo': 'o', 'xx#ox#oxo': 'x', 'oxx#oxoxo': 'o', '#o#xoxxo#': 'o', '#o###xx#o': 'c', 'o##xxxo##': 'x', 'oooxoxx#x': 'o', 'o#x#xxoox': 'x'}

StringErrors = ["xxxooo###___","xxx","trianglepoem","000**####","x"]

VectorErrors = [
"""2
2 4 x
2 2 o
""",
"""1
1 1 ?
""",
"""3
1 1 x
0 1 o
1 1 o
"""
]

valid_vector_games={
"""2
1 1 x
2 2 o
""":'c',
"""3
1 0 x
1 1 o
2 2 x
""":'c',
"""9
1 1 x
0 0 o
1 0 x
1 2 o
2 0 x
0 2 o
0 1 x
2 1 o
2 2 x
""":'t',
"""8
1 1 x
0 0 o
1 0 x
1 2 o
2 0 x
0 2 o
0 1 x
2 1 o
""":'c'
}

def ask_program(process,case,command):
    process.stdin.write(command+'\n')
    process.stdin.write(case+'\n')
    process.stdin.flush()
    return process.stdout.readline().strip()


def check(answer,youranswer,case):
    if youranswer != answer:
        return "problem with case {}\n correct: {}\n   yours: {}\n".format(case,repr(answer),repr(youranswer))   
    return ""

class TTTAnalyzerTestCase(unittest.TestCase):
    "tttanalyzer.cpp"
    @classmethod
    def tearDownClass(cls):
        try:
            D = cls.code_metrics['errors']
        except Exception as e:
            cls.fail('Something went wrong',e)
        cpplint_count= sum(len(D[x]) for x in D)
        as_grade = 5*cls.code_metrics['astyle']
        cls.msgs.append(f"astyle[max 5] {as_grade:.2f}")
        lint_grade = max(0, 5-cpplint_count)
        cls.msgs.append(f"cpplint[max 5] {lint_grade} (1 point deduction for each problem)")
        cls.Points['style'] = as_grade + lint_grade
        cls.msgs.append(f"overall style grade[max 10] {cls.Points['style']:.2f}")

        try:
          cls.process.stdin.write('q\n')
          cls.process.stdin.flush()     
          time.sleep(0.2)     
          if not DEBUG:
            os.remove(cls.baseprogname)
        except Exception as e:
          print(e)

    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'includes':100,'brackets':20,'authors':100}
        cls.Points = {"all":15,"tally":5,"style":5,'tttr_string':40,'tttr_vector':20}


        cls.authorlimit = 2
        cls.valid_includes ={"iostream","string","array","vector","map","movedef.h","cmath"}
        cls.lintoptions=['-runtime/int','-readability/casting',
                         '-readability/alt_tokens','-build/include_subdir']

        cls.refcode = {'lines':88,'words':377}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]

        with open(cls.realfilename) as f:
            cls.file_contents=f.read()

        try:
          splitter = '// MAIN'
          first_part,second_part=cls.file_contents.split(splitter)
        except Exception as e:
          if '\r\n' in cls.file_contents:
            cls.fail(cls,r"Detected windows CRLF newlines in your program. Please use linux '\n' newlines.")
          else:
            cls.fail(cls,"Unable to find the marker:\n{}\n".format(splitter))
        
        cls.baseprogname = 'st3_ttt_'+str(random.randint(1000,100000))
        new_source_file = cls.baseprogname+".cpp"

        with open(new_source_file,'w') as f:
            f.write(first_part)
        cls.code_metrics = ec602lib.code_analysis_cpp(new_source_file,cls.lintoptions)
        with open(new_source_file,'a') as f:
            f.write(real_main)

        T = sub.run(["g++","-std=c++17",new_source_file,"-o",cls.baseprogname],stderr=sub.PIPE)
        errors = T.stderr.decode()
        if errors:
          cls.fail(cls,"COMPILE ERRORS\n"+errors+"\nCOMPILE ERRORS\n")
        cls.process = sub.Popen([cls.baseprogname],**popen_specs)

        time.sleep(0.02)
        return_code = cls.process.poll()
        if return_code:
            cls.fail(cls,'Your program exited with return code {}.'.format(return_code))
        if not DEBUG:
          os.remove(new_source_file)

    test_includes = ec602lib.test_includes
    test_authors = ec602lib.test_authors
    test_style = ec602lib.test_cppstyle
    test_brackets = ec602lib.bracket_check

    def test_brevity(self):
        "brevity. measure the number of lines and words (not including main)"
        lines_words = self.code_metrics['lines']+self.code_metrics['words']

        target = self.refcode['lines']+self.refcode['words']
        self.Points['brevity'] = min(10,max(0,10- (lines_words- target)/50))

    def test_tttstring(self):
      "tttr_string. tests of tttresult(string)"

      T = sub.run([self.baseprogname],stdout=sub.PIPE,input="s\n#########\nq\n",
            universal_newlines=True)
      ans = T.stdout
      if ans != "c\n":
        self.Points['tttr_string']=0
        self.fail('cannot run your program with an empty board as input')


      base_report = ""
      vals = []
      errors = []

      for board in Boards:
          try:
              ans = ask_program(self.process,board,"s")
              vals.append(ans)
              if board in MapAnswer:
                val = check(MapAnswer[board], ans, board)
                if val:
                  errors.append(val)
              else:
                if ans in 'xot':
                  errors.append("problem with case {}\n correct: {}\n   yours: {}\n".format(board,"i or c",repr(ans)))
          except BrokenPipeError:
              errors.append("crashing!!\nproblem with case {}\n".format(repr(board)))
      
      if errors:
          basescore = max(0,100-len(errors)//2)
          self.msgs.append(f"score is 100 - NUM_ERRORS/2 = {basescore:.2f}\n")
      else:
          basescore = 100
      h = hashlib.sha256()
      h.update("".join(vals).encode())
      summary = h.hexdigest()  
      if not errors and summary != "aeb564dd31a04154eff23ebba7661b427b8389c18259b626cb6ce434c4811e46":
        errors=['All xot are correct, but some i and c are switched. I dont know which ones.']
        basescore = 75
        base_report += "BASESCORE = {:.2f}, some i /c errors detected\n".format(basescore)

      error_errors = []

      for board in StringErrors:
          ans = ask_program(self.process,board,"s")
          if ans != "e":
              error_errors.append("problem with case {}\n correct: {}\n   yours: {}\n".format(repr(board),repr("e"),repr(ans)))
      
      if error_errors:
          basescore = max(0,basescore - 5*len(error_errors))
          base_report += "BASESCORE adjusted (due to error handling problems) to {:.2f}\n".format(basescore)

      errors = error_errors + errors

      if len(errors)>100:
         errors=errors[:100]
         errors.append('...only reporting the first 100 errors.\n\n')

      self.msgs.extend(errors)
      self.msgs.append(base_report)

      
      self.Points['tttr_string']=5+ .35*basescore

    def test_tttvector(self):
      "tttr_vector. tests of tttresult(vector<Move>)"
      errors=[]
      for board,res in valid_vector_games.items():
        try:
            ans = ask_program(self.process,board,"v")
            if ans != res:
                errors.append(f"problem with vector case:\n{board}\n correct: {res!r}\n   yours: {ans!r}\n")
        except BrokenPipeError:
            errors.append("crashing!!\nproblem with case {}\n".format(repr(board)))
      self.msgs.extend(errors)
      self.Points['tttr_vector'] = max(0,20 - len(errors)*5)
    def test_get_all_boards(self):
        "all. test the generation of all boards"
        T = sub.run([self.baseprogname],stdout=sub.PIPE,input="a\nq\n",universal_newlines=True)
        ans = T.stdout.splitlines()
        ans.sort()
        all_boards_answer="\n".join(ans)+"\n"
        h = hashlib.sha256()
        h.update(all_boards_answer.encode())
        summary = h.hexdigest()  
        if summary != "26fd02c0d9e0504402322578e85aa24d5fa0b520ce92baecb750b8853553bac5":
            self.fail('you are not generating the boards correctly.\n')

    def test_tally(self):
        "tally. test the overall tally of results"
        T = sub.run([self.baseprogname],stdout=sub.PIPE,input="t\nq\n",universal_newlines=True)
        results = sorted(T.stdout.splitlines())
        the_tally={}
        try:
            for x in results:
                k,v = x.split()
                the_tally[k]=int(v)
        except:
            pass
        if len(results) != 5:
          msg = "Your tally should have 5 lines of output.\n"
        txt = "\n".join(results)
        h = hashlib.sha256()
        h.update(txt.encode())
        summary = h.hexdigest()  
        if summary != "0a04c8dacc8b13688bebdd246dda943567c006f1eecad9c205dc2208db585a28":
            self.fail('your tally of results is not correct.\n')
        tally={}
        for board in Boards:
            try:
                ans = ask_program(self.process,board,"s")
                tally[ans]=tally.get(ans,0)+1
            except:
                pass
        if tally != the_tally:
            self.fail('your tally seems to be fake.')


testcases={
'tttanalyzer.cpp':TTTAnalyzerTestCase,
}
programs = ['tttanalyzer.cpp']
tested_programs = {x:x for x in programs}

if __name__ == '__main__':
    print('TTT Analyzer (HW7) Checker Version {0}.{1}\n'.format(*VERSION))
    g={}
    for prog in testcases:
        report, g[prog] = ec602lib.check_program(testcases[prog])
        print(report)
    print('\nGrade Summary')
    for prog in testcases:
      print(prog,g[prog])