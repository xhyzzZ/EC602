// Copyright 2019 Haoyu Xu xhy@bu.edu

#include<fstream>
#include<iostream>
#include<queue>
#include<set>
#include<sstream>
#include<string>
#include<utility>
#include<vector>

using std::cin;
using std::cout;
using std::endl;
using std::ifstream;
using std::set;
using std::string;
using std::vector;
using std::pair;
using std::queue;

class TrieNode {
 public:
  vector<TrieNode*> children{26, nullptr};
  string word;

  void insert(const string &word) {
    TrieNode *node = this;
    for (char c : word) {
      int index = c - 'a';
      if (node->children[index] == nullptr)
        node->children[index] = new TrieNode();
      node = node->children[index];
    }
    node->word = word;
  }
};
// store puzzle's rowSize and columnSize in global variable
int rowSize = 0, columnSize = 0;
typedef vector<vector<char>> matrix;
bool dfs(matrix &puzzle, int rowIndex, int columnIndex, TrieNode *cur,
        const string &targetStr, int targetStrIndex,
        vector<pair<string, matrix>> &res, bool isLast) {
  char targetChar = targetStr[targetStrIndex];
  char puzzleChar = puzzle[rowIndex][columnIndex];
  if (puzzleChar == '#')
    return false;
  if (targetChar != '*' && puzzleChar != targetChar)
    return false;
  int index = puzzleChar - 'a';
  if (cur->children[index] == nullptr)
    return false;
  cur = cur->children[index];
  if (!cur->word.empty()) {
    puzzle[rowIndex][columnIndex] = '#';
    if (isLast)
      res.push_back(pair<string, matrix>(cur->word, matrix()));
    else
      res.push_back(pair<string, matrix>(cur->word, puzzle));
    puzzle[rowIndex][columnIndex] = puzzleChar;
    return true;
  }

  // search adjacent cells in puzzle
  bool returnValue = false;
  puzzle[rowIndex][columnIndex] = '#';
  for (int r = -1; r <= 1; r++) {
    for (int c = -1; c <= 1; c++) {
      if (r != 0 || c != 0) {
        bool search = dfs(puzzle, rowIndex + r, columnIndex + c,
          cur, targetStr, targetStrIndex + 1, res, isLast);
        returnValue |= search;
      }
    }
  }
  puzzle[rowIndex][columnIndex] = puzzleChar;
  return returnValue;
}
// drop elements in puzzle in order to fill all blank space
void drop(matrix &puzzle) {
  for (int columnIndex = 0; columnIndex < columnSize; columnIndex++) {
    int i = rowSize - 1;
    int j = rowSize - 1;
    while (true) {
      while (i >= 0 && puzzle[i][columnIndex] != '#') {
        i--;
        j--;
      }
      while (j >= 0 && puzzle[j][columnIndex] == '#') {
        j--;
      }
      if (j < 0) {
        break;
      } else {
        puzzle[i][columnIndex] = puzzle[j][columnIndex];
        puzzle[j][columnIndex] = '#';
      }
    }
  }
}

bool solve(matrix &puzzle, const vector<TrieNode*> &triesBucket,
  const vector<string> &targets, vector<vector<string>> &res) {
  // init the state of current puzzle solver
  bool returnValue = false;
  rowSize = puzzle.size();
  columnSize = puzzle.size();
  int puzzleSize = rowSize * columnSize;
  int targetNum = targets.size();
  vector<int> targetLength;
  for (const string &s : targets) targetLength.push_back(s.size());
  if (triesBucket[targetLength[0] - 1] == nullptr) return false;
  typedef pair<vector<string>, matrix> record;
  queue<record> queue;
  vector<pair<string, matrix>> matchingResults;
  for (int i = 0; i < puzzleSize; i++) {
    if (dfs(puzzle, i / columnSize, i % columnSize,
    triesBucket[targetLength[0] - 1], targets[0], 0,
    matchingResults, targetNum == 1)) {
      for (const auto &match : matchingResults) {
        queue.push(record(vector<string>
          (1, match.first), match.second));
      }
      matchingResults.clear();
    }
  }

  // start loop -- the same order as bfs
  while (!queue.empty()) {
    int curTargetNum = queue.front().first.size();
    if (curTargetNum == targetNum) {
      res.push_back(queue.front().first);
      returnValue = true;
    } else {
      if (triesBucket[targetLength[curTargetNum] - 1] == nullptr) {
        queue.pop();
        continue;
      }
      drop(queue.front().second);
      vector<pair<string, matrix>> matchingResults;
      for (int i = 0; i < puzzleSize; i++) {
        if (dfs(queue.front().second, i / columnSize, i % columnSize,
        triesBucket[targetLength[curTargetNum] - 1], targets[curTargetNum],
        0, matchingResults, curTargetNum == targetNum - 1)) {
          for (const auto &match : matchingResults) {
            vector<string> matchingWords(queue.front().first);
            matchingWords.push_back(match.first);
            queue.push(record(matchingWords, match.second));
          }
          matchingResults.clear();
        }
      }
    }
    queue.pop();
  }

  return returnValue;
}

int main(int argc, char *argv[]) {
  if (argc < 3) {
    return 1;
  }
  char *smallListFileName = argv[1];
  char *largeListFileName = argv[2];

  ifstream smallListFS(smallListFileName);
  // exit if can not open samll_word_list file
  if (!smallListFS.is_open()) {
    return 2;
  }
  // build trie trees from samll word list
  // consider that the length of each target word is known
  // so build several trie trees and words in the same tree have same length
  // this is an important pre pruning step
  vector<TrieNode*> smallTriesBucket(30, nullptr);
  vector<TrieNode*> largeTriesBucket(30, nullptr);
  bool hasBuildLarge = false;
  string word;
  while (smallListFS >> word) {
    int bucketIndex = word.size() - 1;
    if (smallTriesBucket[bucketIndex] == nullptr) {
      smallTriesBucket[bucketIndex] = new TrieNode();
      smallTriesBucket[bucketIndex]->insert(word);
    } else {
      smallTriesBucket[bucketIndex]->insert(word);
    }
  }

  // puzzle matrix
  matrix puzzle;
  // loop and waiting for input until an EOF or CTRL+D
  string line;
  while (getline(cin, line)) {
    // exit when input an empty line
    if (line.empty()) {
      break;
    } else if (line.find('*') != string::npos) {
      // use std::istringstream in order to split a string
      vector<string> targetList;
      std::istringstream ss(line);
      string word;
      while (ss >> word) targetList.push_back(word);
      vector<vector<string>> solvedList;
      if (!solve(puzzle, smallTriesBucket, targetList, solvedList)) {
        if (!hasBuildLarge) {
          ifstream largeListFS(largeListFileName);
          if (!largeListFS.is_open()) return 2;
          while (largeListFS >> word) {
            int bucketIndex = word.size() - 1;
            if (largeTriesBucket[bucketIndex] == nullptr) {
              largeTriesBucket[bucketIndex] = new TrieNode();
              largeTriesBucket[bucketIndex]->insert(word);
            } else {
              largeTriesBucket[bucketIndex]->insert(word);
            }
          }
          hasBuildLarge = true;
        }
        solve(puzzle, largeTriesBucket, targetList, solvedList);
      }
      // start output solved answers
      // use an set to Deduplicate and output in dictionary order
      set<string> answerSet;
      for (const auto &answer : solvedList) {
        std::stringstream ss;
        for (int i = 0; i < answer.size() - 1; i++)
          ss << answer[i] << " ";
        ss << answer[answer.size() - 1];
        answerSet.insert(ss.str());
      }
      for (const string &answerLine : answerSet)
        cout << answerLine << endl;
      cout << "." << endl;
      puzzle.clear();
    } else {
      vector<char> puzzleRow(line.begin(), line.end());
      puzzle.push_back(puzzleRow);
    }
  }
  return 0;
}