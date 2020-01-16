# Copyright 2019 Haoyu Xu xhy@bu.edu
import sys

def generate_anagram(dicts):
    dic = {}
    for str in dicts:
        key = ''.join(sorted(str))
        if key in dic:
            dic.get(key).append(str)
        else:
            dic[key] = [str]
    return dic.values()

def is_palindrome(str):
    rev = ''.join(reversed(str))
    if (str == rev):
        return True
    return False

def check_clean(lists):
    for val in lists:
        for x in val:
            if is_palindrome(x) == False:
                val.remove(x)
    for val in lists:
        for x in val:
            print(x)
        print()

def main():
    file_name = sys.argv[1]
    str_list = []
    with open(file_name) as f:
        for line in f:
            str_list.append(line)
    lists = generate_anagram(str_list)

    check_clean(lists)


if __name__ == "__main__":
    main()
