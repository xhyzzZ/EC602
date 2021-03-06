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
using std::pair;
using std::queue;
using std::set;
using std::string;
using std::vector;

class TrieNode {
 public:
  vector<TrieNode*> children{26, nullptr};
  string word;

  void insert(const string &word) {
    TrieNode *cur = this;
    for (char c : word) {
      int index = c - 'a';
      if (cur->children[index] == nullptr)
        cur->children[index] = new TrieNode();
      cur = cur->children[index];
    }
    cur->word = word;
  }
};
int rowSize = 0, colSize = 0;
typedef vector<vector<char>> matrix;
bool dfs(matrix &puzzle, int rowIndex, int colIndex, TrieNode *cur,
         const string &target, int targetIndex,
         vector<pair<string, matrix>> &res, bool isLast) {
  char targetChar = target[targetIndex];
  char puzzleChar = puzzle[rowIndex][colIndex];
  if (puzzleChar == '#')
    return false;
  if (targetChar != '*' && puzzleChar != targetChar)
    return false;
  int index = puzzleChar - 'a';
  if (cur->children[index] == nullptr)
    return false;
  cur = cur->children[index];
  if (!cur->word.empty()) {
    puzzle[rowIndex][colIndex] = '#';
    if (isLast)
      res.emplace_back(cur->word, matrix());
    else
      res.emplace_back(cur->word, puzzle);
    puzzle[rowIndex][colIndex] = puzzleChar;
    return true;
  }

  // search adjacent in puzzle
  puzzle[rowIndex][colIndex] = '#';
  bool flag = false;
  for (int r = -1; r <= 1; r++) {
    for (int c = -1; c <= 1; c++) {
      if (r != 0 || c != 0) {
        int newRow = rowIndex + r, newCol = colIndex + c;
        if (newRow < 0 || newRow >= puzzle.size() || newCol < 0
            || newCol >= puzzle.size()) continue;
        bool search = dfs(puzzle, newRow, newCol, cur, target,
                          targetIndex + 1, res, isLast);
        flag |= search;
      }
    }
  }
  puzzle[rowIndex][colIndex] = puzzleChar;
  return flag;
}
// remove elements in puzzle
void remove(matrix &puzzle) {
  for (int colIndex = 0; colIndex < colSize; colIndex++) {
    int i = rowSize - 1, j = rowSize - 1;
    while (true) {
      while (i >= 0 && puzzle[i][colIndex] != '#') {
        i--;
        j--;
      }
      while (j >= 0 && puzzle[j][colIndex] == '#') {
        j--;
      }
      if (j >= 0) {
        puzzle[i][colIndex] = puzzle[j][colIndex];
        puzzle[j][colIndex] = '#';
      } else {
        break;
      }
    }
  }
}

bool solve(matrix &puzzle, const vector<TrieNode*> &triesBucket,
           const vector<string> &targets, vector<vector<string>> &res) {
  bool flag = false;
  rowSize = puzzle.size(), colSize = puzzle.size();
  int puzzleSize = rowSize * colSize;
  int targetNum = targets.size();
  vector<int> targetLength;
  targetLength.reserve(targets.size());
  for (const string &s : targets) targetLength.push_back(s.size());
  if (triesBucket[targetLength[0] - 1] == nullptr) return false;
  typedef pair<vector<string>, matrix> record;
  queue<record> queue;
  vector<pair<string, matrix>> matched;
  for (int i = 0; i < puzzleSize; i++) {
    if (dfs(puzzle, i / colSize, i % colSize,
            triesBucket[targetLength[0] - 1], targets[0], 0,
            matched, targetNum == 1)) {
      for (const auto &match : matched) {
        queue.push(record(vector<string> (1, match.first), match.second));
      }
      matched.clear();
    }
  }

  while (!queue.empty()) {
    int curTargetNum = queue.front().first.size();
    if (curTargetNum == targetNum) {
      res.push_back(queue.front().first);
      flag = true;
    } else {
      if (triesBucket[targetLength[curTargetNum] - 1] == nullptr) {
        queue.pop();
        continue;
      }
      remove(queue.front().second);
      vector<pair<string, matrix>> matched;
      for (int i = 0; i < puzzleSize; i++) {
        if (dfs(queue.front().second, i / colSize, i % colSize,
                triesBucket[targetLength[curTargetNum] - 1],
                targets[curTargetNum], 0, matched,
                curTargetNum == targetNum - 1)) {
          for (const auto &match : matched) {
            vector<string> matchingWords(queue.front().first);
            matchingWords.push_back(match.first);
            queue.push(record(matchingWords, match.second));
          }
          matched.clear();
        }
      }
    }
    queue.pop();
  }

  return flag;
}

int main(int argc, char *argv[]) {
  if (argc < 3) {
    return 1;
  }
  char *smallName = argv[1];
  char *largeName = argv[2];

  ifstream smallFS(smallName);
  if (!smallFS.is_open()) {
    return 2;
  }
  vector<TrieNode*> smallTriesBucket(30, nullptr);
  vector<TrieNode*> largeTriesBucket(30, nullptr);
  bool hasBuildLarge = false;
  string word;
  while (smallFS >> word) {
    int index = word.size() - 1;
    if (smallTriesBucket[index] == nullptr) {
      smallTriesBucket[index] = new TrieNode();
      smallTriesBucket[index]->insert(word);
    } else {
      smallTriesBucket[index]->insert(word);
    }
  }

  matrix puzzle;
  string line;
  while (getline(cin, line)) {
    if (line.find('*') != string::npos) {
      vector<string> targetList;
      std::istringstream in(line);
      string word;
      while (in >> word) targetList.push_back(word);
      vector<vector<string>> solved;
      if (!solve(puzzle, smallTriesBucket, targetList, solved)) {
        if (!hasBuildLarge) {
          ifstream largeFS(largeName);
          if (!largeFS.is_open()) return 2;
          while (largeFS >> word) {
            int index = word.size() - 1;
            if (largeTriesBucket[index] == nullptr) {
              largeTriesBucket[index] = new TrieNode();
              largeTriesBucket[index]->insert(word);
            } else {
              largeTriesBucket[index]->insert(word);
            }
          }
          hasBuildLarge = true;
        }
        solve(puzzle, largeTriesBucket, targetList, solved);
      }
      set<string> answerSet;
      for (const auto &answer : solved) {
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
    } else if (line.empty()) {
      break;
    } else {
      vector<char> row(line.begin(), line.end());
      puzzle.push_back(row);
    }
  }
  return 0;
}
