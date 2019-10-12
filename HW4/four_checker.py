"polynomials/sequences checker"
import unittest
import time
import logging
import subprocess as sub
import random
import os
import math
import random
import numpy as np

from threading import Thread

from queue import Queue, Empty


VERSION, EC602VER = (1,5), (3,3)

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

programs = ['bigint.cpp',
'polyops.cpp',
"system.py"]

tested_programs = {x:x for x in programs}


TIMEALLOWED = 1
COMPILEALLOWED = 2

P={"stdout":sub.PIPE,"timeout":TIMEALLOWED,"stderr":sub.PIPE}

CP={"stdout":sub.PIPE,"timeout":COMPILEALLOWED,"stderr":sub.PIPE}



cppmain="""
#include <iostream>
#include <vector>

using namespace std;

#include "PROGNAME"

int main()
{ 

  int Alen,Blen;

  cin >> Alen >> Blen;

  Poly A(Alen,0),B(Blen,0);

  for (auto& e : A)
     cin >> e;
  
  for (auto& e : B)
     cin >> e;

  for (auto e : add_poly(A,B))
     cout << e << " ";
  cout << endl;


  for (auto e : multiply_poly(A,B))
     cout << e << " ";
  cout << endl;  

}"""

Same_Add_Tests=[
[(1.2,0,5),(3,2,1),(4.2,2,6)],
[(1,2,3),(4,5,6),(5,7,9)],
[(0,0,4),(0,0,0.1),(0,0,4.1)],
]

Diff_Add_Tests=[
[(1.2,0,0, 5),(3,2,1),(4.2,2,1,5)],
[(1,6,3),(4,),(5,6,3)],
[(0,0,0,0,5),(0,0,1,4),(0,0,1,4,5)],
]

Same_Mul_Tests=[
[(1.2,0,5),(3,2,1),(3.6, 2.4, 16.2, 10, 5)],
[(1,2,3),(4,5,6),(4, 13, 28, 27, 18)],
[(0,0,4),(0,0,0.1),(0, 0, 0, 0, 0.4)],
]

Diff_Mul_Tests=[
[(1.2,0,0, 5),(3,2,1),(3.6, 2.4, 1.2, 15, 10, 5)],
[(1,6,3),(4,),(4, 24, 12)],
[(1,1,-1),(1,1,1),(1, 2, 1, 0.0, -1)],
[(0,0,0,0,5),(0,0,1,4),(0, 0, 0, 0, 0, 0, 5, 20)],
]

Tricky_Add_Tests=[
[(1,3,2),(1,6,-2),(2,9)],
[(1,1,1),(-1,-1,-1),(0,) ],
]


Tricky_Mul_Tests=[
[(1,2,1,1,1,6),(0,),(0,) ],
]

double_add_tests=[
[(1e-50,),(-0.99e-50,),(1e-52,)],
[(1e300,2e300),(0,0,3e300),(1e300,2e300,3e300)],
]

def fin(a,b):
  "format the input for polyops_example_main"
  astr = " ".join(str(x) for x in a)
  bstr = " ".join(str(x) for x in b)
  return "{} {} {} {}".format(len(a),len(b),astr,bstr).encode()

def fout(T):
  "extract the output for polyops_example_main"
  text = T.stdout.decode().splitlines()
  addition = tuple(float(x) for x in text[0].strip().split())
  multiply = tuple(float(x) for x in text[1].strip().split())
  return addition,multiply

def compile(cpp,executable):
  return ['g++','-std=c++14',cpp, '-o', executable]
          
def check_poly_add(self,a,b,aplusb):
   with self.subTest(CASE=" {} + {} = {}".format(a,b,aplusb)):
      T = sub.run([self.executable],input=fin(a,b),**P)
      add_res,_ = fout(T)
      #self.assertEqual(len(add_res),len(aplusb),
      #     "your addition: {}\ncorrect answer: {}\n".format(add_res,aplusb))
      if len(add_res) != len(aplusb) or not np.allclose(add_res,aplusb,atol=0):
        self.fail("your addition: {}\ncorrect answer: {}\n".format(add_res,aplusb))


def check_poly_mult(self,a,b,atimesb):
    with self.subTest(CASE=" {} * {} = {}".format(a,b,atimesb)):
      T = sub.run([self.executable],input=fin(a,b),**P)
      _,res = fout(T)
      if len(res) != len(atimesb) or not np.allclose(res,atimesb,atol=0):
        self.fail("your multiply: {}\ncorrect answer: {}\n".format(res,atimesb))


class polyopsTestCase(unittest.TestCase):
    "polyops.cpp"
    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'0':50,'1':50,'2':50}
        cls.Points = {"a":10,"b":15,'c':15,"d":15,"e":15,"f":15,"g":15}
        cls.authorlimit = 2
        cls.valid_includes = set(['vector'])

        cls.refcode = {'lines':29,'words':130}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]
        cls.file_contents_main = cppmain.replace("PROGNAME",
                                            cls.realfilename)

        ec602lib.compile_main(cls,"st3_poly")


    @classmethod
    def tearDownClass(cls):
        ec602lib.safe_remove(cls.executable)

    test_includes = ec602lib.test_includes
    test_authors = ec602lib.test_authors
    test_style = ec602lib.test_cppstyle
    test_brackets = ec602lib.bracket_check



    def test_add_same_size(self):
       "b. add same size vectors"
       for (a,b,res) in Same_Add_Tests:
           check_poly_add(self,a,b,res)


    def test_add_different_size(self):
       "c. add different size vectors"
       for (a,b,res) in Diff_Add_Tests:
           check_poly_add(self,a,b,res)

    def test_mult_same_size(self):
       "d. multiply same size vectors"
       for (a,b,res) in Same_Mul_Tests:
           check_poly_mult(self,a,b,res)

    def test_mult_different_size(self):
       "e. multiply different size vectors"
       for (a,b,res) in Diff_Mul_Tests:
           check_poly_mult(self,a,b,res)

    def test_add_tricky(self):
       "f. add vectors with result smaller"
       for (a,b,res) in Tricky_Add_Tests:
           check_poly_add(self,a,b,res)

    def test_mult_tricky(self):
       "g. multiply vectors with result smaller"
       for (a,b,res) in Tricky_Mul_Tests:
           check_poly_mult(self,a,b,res)
    
    def test_double_add(self):
       "a. vector double"
       for (a,b,res) in double_add_tests:
             check_poly_add(self,a,b,res)



bigintmain="""
#include <iostream>
#include <vector>

using namespace std;

#include "PROGNAME"

int main()
{ 

  BigInt A,B;

  cin >> A >> B;

  cout << multiply_int(A,B) << endl;

}"""

SmallIntTests=[(8,9),(4,5),(999,1001)]

BigIntTests=[(123456,123456),(10000100060043,34444234234),(10**19-1,10**19-1),
(100000001,9900000099)]

ZeroTests=[(12340,0),(0,23342342)]

def compile(cpp,executable):
  return ['g++','-std=c++14',cpp, '-o', executable]
          
        
def check_bi_mult(self,a,b,atimesb):
    with self.subTest(CASE=" {} * {} = {}".format(a,b,atimesb)):
      intext="{} {}".format(a,b).encode()
      T = sub.run([self.executable],input=intext,**P)
      res = T.stdout.decode().strip()
      if res != str(atimesb):
        self.fail("your multiply: {}\ncorrect answer: {}\n".format(res,atimesb))


class bigintTestCase(unittest.TestCase):
    "bigint.cpp"
    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'0':50,'1':50,'2':50}
        cls.Points = {"a":40,"b":40,'c':20}
        cls.authorlimit = 2
        cls.valid_includes = set(['vector','string'])

        cls.refcode = {'lines':36,'words':165}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]
        cls.file_contents_main = bigintmain.replace("PROGNAME",
                                            cls.realfilename)

        ec602lib.compile_main(cls,"st3_big")

    @classmethod
    def tearDownClass(cls):
       try:
        os.remove(cls.executable)
       except:
        pass


    test_includes = ec602lib.test_includes
    test_authors = ec602lib.test_authors
    test_style = ec602lib.test_cppstyle
    test_brackets = ec602lib.bracket_check

    def test_mult(self):
       "a. test small numbers"
       for (a,b) in SmallIntTests:
           check_bi_mult(self,a,b,a*b)

    def test_big_mult(self):
       "b. test big numbers"
       for (a,b) in BigIntTests:
           check_bi_mult(self,a,b,a*b)

    def test_zero_mult(self):
       "c. test mult by zero"
       for (a,b) in ZeroTests:
           check_bi_mult(self,a,b,a*b)



# system.py



Output_Same_Tests = [
    [(1.2, 0, 5), (3, 2, 1), (3.6, 2.4, 16.2, 10, 5)],
    [(1, 2, 3), (4, 5, 6), (4, 13, 28, 27, 18)],
    [(0, 0, 4), (0, 0, 0.1), (0, 0, 0, 0, 0.4)],
]

Output_Diff_Tests = [
    [(1.2, 0, 0, 5), (3, 2, 1), (3.6, 2.4, 1.2, 15, 10, 5)],
    [(1, 6, 3), (4, ), (4, 24, 12)],
    [(1, 1, -1), (1, 1, 1), (1, 2, 1, 0.0, -1)],
    [(0, 0, 0, 0, 5), (0, 0, 1, 4), (0, 0, 0, 0, 0, 0, 5, 20)],
]


def fin_sys(x, h):
    "format the input for system"
    xstr = " ".join(str(f) for f in x)
    hstr = " ".join(str(f) for f in h)
    input_str = "{x}\n{h}\n".format(x=xstr, h=hstr)
    return input_str.encode()


def check_output(self, x, h, yans):
    with self.subTest(CASE=" x[n] = {}, h[n] = {} y[n] = {}".format(
            x, h, yans)):
        T = sub.run(['python', self.realfilename], input=fin_sys(x, h), **P)
        if T.returncode:
           self.fail('program terminated with error:\n'+T.stderr.decode()+"\n")
        res = [float(x) for x in T.stdout.decode().strip().split()]
        if len(res) != len(yans) or not np.allclose(res, yans, atol=0):
            self.fail(
                "your output: {}\ncorrect answer: {}\n".format(res, yans))


class systemTestCase(unittest.TestCase):
    "system.py"
    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'0':50,'1':50,'2':50}
        cls.Points = {"a":50,"b":50}
        cls.authorlimit = 2
        cls.valid_includes = set(['numpy'])

        cls.refcode = {'lines':3,'words':15}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]

        with open(cls.realfilename) as f:
            cls.file_contents=f.read()



    test_includes = ec602lib.test_imports
    test_authors = ec602lib.test_authors
    test_style = ec602lib.test_pystyle

    def test_same_system(self):
        "a. h and x same size"
        for (x, h, y) in Output_Same_Tests:
            check_output(self, x, h, y)

    def test_diff_system(self):
        "b. h and x different size"
        for (x, h, y) in Output_Diff_Tests:
            check_output(self, x, h, y)

testcases={
'polyops.cpp':polyopsTestCase,
'bigint.cpp':bigintTestCase,
'system.py':systemTestCase,
}

if __name__ == '__main__':
    print('Polynomials and Sequences (HW4) Checker Version {0}.{1}\n'.format(*VERSION))
    g={}
    for prog in testcases:
        report, g[prog] = ec602lib.check_program(testcases[prog])
        print(report)
    print('\nGrade Summary')
    for prog in testcases:
      print(prog,g[prog])
