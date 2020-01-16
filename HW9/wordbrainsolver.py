# Copyright 2019 Haoyu Xu xhy@bu.edu

from sys import argv


def word_dict(ind, word, dic):
    if ind == len(word) - 1:
        dic.setdefault(word[ind], {})['end'] = True
    else:
        word_dict(ind + 1, word, dic.setdefault(word[ind], {}))


def drop(matrix, num, cor):
    grid = list(matrix)
    for i in sorted(cor):
        row = ord(i) // num
        col = ord(i) % num
        if row != 0:
            while row != 0:
                grid[row * num + col] = grid[(row - 1) * num + col]
                grid[(row - 1) * num + col] = " "
                row -= 1
        else:
            grid[col] = " "
    return ''.join(grid)


def generate_neighbor(num, matrix):
    neighbor = [[] for i in matrix]
    for i in range(num ** 2):
        row = i // num
        col = i % num
        if row > 0:
            neighbor[i].append(i - num)
        if row < num - 1:
            neighbor[i].append(i + num)
        if col < num - 1:
            neighbor[i].append(i + 1)
            if row > 0:
                neighbor[i].append(i - num + 1)
            if row < num - 1:
                neighbor[i].append(i + num + 1)
        if col > 0:
            neighbor[i].append(i - 1)
            if row > 0:
                neighbor[i].append(i - num - 1)
            if row < num - 1:
                neighbor[i].append(i + num - 1)
    return neighbor


def find_word(i, matrix, n_word, dic, res,
              word, length, neighbor, unvisit, str_l):
    num_word = len(word)
    if matrix[i] in dic:
        unvisit[i] = False
        if str_l[n_word][num_word].isalpha() is True:
            if matrix[i] == str_l[n_word][num_word]:
                word += chr(i)
        else:
            word += chr(i)
        if len(word) == length[n_word]:
            if 'end' in dic[matrix[i]]:
                res.append(word)
            return res
        for letter in neighbor[i]:
            if unvisit[letter]:
                find_word(letter, matrix, n_word, dic[matrix[i]], res,
                          word, length, neighbor, unvisit, str_l)
                unvisit[letter] = True


def find_solution(matrix, n_word, dic, tem, sol, length,
                  neighbor, num, str_l):
    num_grid = len(matrix)
    for start in range(num_grid):
        if matrix[start] == " ":
            continue
        if str_l[n_word][0].isalpha() is True:
            if matrix[start] != str_l[n_word][0]:
                continue
        res = []
        unvisited = [True] * len(matrix)
        find_word(start, matrix, n_word, dic, res, '', length,
                  neighbor, unvisited, str_l)
        for words in res:
            word_tem = ''
            temp = tem
            for i in words:
                word_tem = word_tem + matrix[ord(i)]
            temp = temp + ' ' + word_tem
            if n_word == len(length) - 1:
                sol.append(temp)
            else:
                grid = matrix[:]
                grid = drop(grid, num, words)
                find_solution(grid, n_word + 1, dic, temp, sol,
                              length, neighbor, num, str_l)
    return sol


def main():
    with open(argv[1]) as small:
        words = small.read().split()
    small_dic = {}
    for word in words:
        word_dict(0, word, small_dic)

    with open(argv[2]) as big:
        words = big.read().split()
    big_dic = {}
    for word in words:
        word_dict(0, word, big_dic)

    count = 0
    word_list = []
    try:
        while True:
            line = input().split('\n')
            if line is '':
                break
            word_list.append(''.join(line))
            if '*' in line[0]:
                while count < len(word_list):
                    str1 = []
                    length = []
                    num = len(word_list[count])
                    for i in range(num):
                        str1.append(word_list[count + i])
                    str2 = ''.join(str1)
                    str_l = word_list[count + num].split()
                    num_strl = len(str_l)
                    for i in range(num_strl):
                        length.append(len(str_l[i]))

                    neighbor = generate_neighbor(num, str2)
                    sol = []
                    find_solution(str2, 0, small_dic, '', sol,
                                  length, neighbor, num, str_l)
                    if len(sol) == 0:
                        find_solution(str2, 0, big_dic, '', sol,
                                      length, neighbor, num, str_l)

                    num_sol = len(sol)
                    for i in range(num_sol):
                        sol[i] = sol[i][1:len(sol[i])]
                    sol = list(set(sol))
                    sol.sort()

                    if sol:
                        print('\n'.join(info for info in sol))
                    print('.')

                    count += (num + 1)
    except EOFError:
        pass


if __name__ == "__main__":
    main()
