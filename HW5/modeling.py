#!/usr/bin/python
# Copyright 2019 Haoyu Xu xhy@bu.edu
class Polynomial():
    def __init__(self, arr = []):
        self.arr = arr
        self.dict = {}  
        ## reverse    
        for i in range (0, len(arr)):
            self.dict[i] = arr[len(arr) - 1 - i]

    def __setitem__(self, key, value):
        if value != 0:
            self.dict[key] = value
        
    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return 0    
    
    def __add__(self, v):
        new = Polynomial()
        for i in self.dict:
            new.dict[i] = self.dict[i]
        for i in v.dict:
            if i in self.dict:
                new.dict[i] += v.dict[i]
            else:
                new.dict[i] = v.dict[i]
        return new

    def __sub__(self, v):
        new = Polynomial()
        for i in self.dict:
            new.dict[i] = self.dict[i]
        for i in v.dict:
            if i in self.dict:
                new.dict[i] -= v.dict[i]
            else:
                new.dict[i] = v.dict[i]
        return new

    def __mul__(self, v):
        new = Polynomial()
        for i in self.dict:
            if self.dict[i] != 0:
                for j in v.dict:
                    if v.dict[j] != 0:
                        if i + j in new.dict:
                            new.dict[i + j] += self.dict[i] * v.dict[j]
                        else:
                            new.dict[i + j] = self.dict[i] * v.dict[j]
        return new
    
    def __eq__(self, v):
        return self.dict == v.dict
    
    def eval(self, v):
        val = 0
        for i in self.dict:
            val += self.dict[i] * (v**i)
        return val
    
    def deriv(self):
        y = Polynomial()
        for i in self.dict:
            y[i - 1] = self.dict[i] * i
        return y

    def __str__(self):
        return "{}".format(self.dict)

    def __repr__(self):
        return str(self)

def main():
    pass

if __name__ == "__main__":
    main()
    p = Polynomial([5, 4])