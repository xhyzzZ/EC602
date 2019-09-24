"c++/unix checker"
import unittest
import time
import logging
import subprocess
import random
import os

from threading  import Thread

from queue import Queue, Empty


VERSION = (2,1)

tested_programs = {'splitargs':'splitargs.cpp','numbers':'numbers.cpp'}

refcode = {'splitargs': {'lines':8,'words':45},'numbers':{'lines':55,'words':232}}

valid_includes = {'splitargs':set(['vector']), 'numbers':set(['vector','string'])}


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
    if e.VERSION < (2,8):
        update_ec602lib()
        from importlib import reload
        e = reload(e)

    return e

ec602lib = get_ec602lib()


TIMEALLOWED = 1
COMPILEALLOWED = 2

P={"stdout":subprocess.PIPE,"timeout":TIMEALLOWED,"stderr":subprocess.PIPE}

CP={"stdout":subprocess.PIPE,"timeout":COMPILEALLOWED,"stderr":subprocess.PIPE}

bracket_msg="""You are not allowed to use brackets []

a) Use .at() or other methods instead
b) replace c-style arrays with vectors or strings etc
c) if you must use a c-style array (e.g. argv) use pointers

You have {} brackets.
"""

def bracket_check(self):
    bracket_count = self.file_contents.count('[')
    if bracket_count:
      self.fail(bracket_msg.format(bracket_count))

      self.fail('Invalid includes: {}'.format(" ".join(x for x in invalid_includes)))



# splitargs testing

testwords = ['apple', 'orange', 'kiwi', 'banana',
             'strawberry', 'pineapple', 'raspberry','tomato']

sa_msg="""
Your {fstream} is not correct for {n} arguments.

Correct output (between the dashed lines)
--------------
{cor}--------------
Your output (between the dashed lines)
-----------
{out}-----------
"""

class SplitArgsTestCase(unittest.TestCase):
    """unit testing for splitargs.cpp"""
    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'1':100}
        cls.Points = {"a":50,"b":50}
        with open(tested_programs['splitargs']) as f:
            cls.file_contents=f.read()

        baseprogname = 'st3_split_'+str(random.randint(1000,100000))

        try:
          C = subprocess.run(ec602lib.compile(tested_programs['splitargs'],baseprogname),**CP)
        except Exception as e:
          raise unittest.SkipTest("Compile failed.\n"+str(e))

        if C.returncode:
            raise unittest.SkipTest("Compile failed.\n"+str(C.stderr.decode()))

        cls.executable = baseprogname

    def test_brackets(self):
        "1. check for brackets"
        bracket_check(self)

    def test_stdout_outputs(self):
        "a. stdout outputs"
        for n in [0, 3, 4, 5, 7]:
            with self.subTest(CASE=f"{n} arguments"):
                words = random.sample(testwords, n)
                try:
                    T = subprocess.run([self.executable, *words], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,timeout=1)
                except TimeoutError:
                    self.fail("your program timed out.")
                except Exception as e:
                    self.fail(f"Error: {e}")  
                out = T.stdout.decode()
                cor = ''.join([a+'\n' for a in words[:4]])
                if out != cor:
                    self.fail(sa_msg.format(fstream='stdout',n=n,cor=cor,out=out))
    def test_stderr_outputs(self):
        "b. stderr outputs"
        for n in [0, 3, 4, 5, 7]:
            with self.subTest(CASE=f"{n} arguments"):
                words = random.sample(testwords, n)
                try:
                    T = subprocess.run([self.executable, *words], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,timeout=1)
                except TimeoutError:
                    self.fail("your program timed out.")
                except Exception as e:
                    self.fail(f"Error: {e}") 
                out = T.stderr.decode()
                cor = ''.join([a+'\n' for a in words[4:]])
                if out != cor:
                    self.fail(sa_msg.format(fstream='stderr',n=n,cor=cor,out=out))

    @classmethod
    def tearDownClass(cls):
       try:
        os.remove(cls.executable)
       except:
        pass



# numbers testing


Happy = [1, 31, 91, 291, 301, 331, 391, 671, 761, 881, 901, 921, 931]
UnHappy = [11, 21, 41, 51, 61, 71, 81, 101, 111, 121, 961, 971, 981, 991]

PropDivTests = [(2, (1,)), (6, (1, 2, 3)), (28, (1, 2, 4, 7, 14)), (31, (1,)), 
(100, (1, 2, 4, 5, 10, 20, 25, 50)), (2342, (1, 2, 1171)), 
(1000, (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500)), 
(9240, (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 20, 21, 22, 24, 28, 30, 33, 35, 40, 
    42, 44, 55, 56, 60, 66, 70, 77, 84, 88, 105, 110, 120, 132, 140, 154, 165, 168, 210, 220, 
    231, 264, 280, 308, 330, 385, 420, 440, 462, 616, 660, 770, 840, 924, 1155, 1320, 1540, 1848, 2310, 3080, 4620))]

ProdPosTestsInt = [
([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],3628800),
((-1, -2, 3), 3), 
((2, 0, 3), 6), 
([-9, -8, -7, -6, -5, -4, -3, -2], 1), 
]

ProdPosTestsDbl = [ ((0.5, 2, -1, 0.1, 100.5), 10.05),
((-1, 5, 6, 5, -1, 2, -0.1), 300),
((0.1,0.2,0.3,0.4,0.5,-0.1),0.0012)
]

# add

real_main=r"""#include "numbers_solution.cpp"
#include <iostream>
#include <vector>
#include <string>
using std::vector;
using std::string;
using std::cin;
using std::cout;


int main() {
  string asktype, num1, num2;
  int n, num_count;
  vector<int> res;
  double d;
  

  while (cin >> asktype) {
    if (asktype == "h") {  // is_word
      std::cin >> n;
      cout << is_happy(n) << "\n";
    } else if (asktype == "pd") {
      std::cin >> n;
      res = proper_divisors(n);
      for (auto x : res) cout << x << "\n";
    } else if (asktype == "add") {
      std::cin >> num1 >> num2;
      cout << add(num1, num2) << "\n";
    } else if (asktype == "pop_i") {
      vector<int> list;
      cin >> num_count;
      for (int i = 0; i < num_count; i++) {
         cin >> n;
         list.push_back(n);
       }
      cout << product_of_positives(list) << "\n";
    } else if (asktype == "pop_d") {
      vector<double> list;
      cin >> num_count;
      for (int i = 0; i < num_count; i++) {
        cin >> d;
        list.push_back(d);
      }
      cout << product_of_positives(list) << "\n";
    } else {
      return 0;
    }
    cout << ".\n";
  }
  return 0;
}
"""

AddTests=[
  ('1234 6','1240'),
  ('6 1234','1240'),
  ('123 312','435'),
  ('4 6','10'),
  ('88 99','187'),
  ('6'*234+' '+'7'*236,'78'+'4'*233+'3'),
  ('123456789 987654321','1111111110')
  ]


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class NumbersTestCase(unittest.TestCase):
    @classmethod
    def start_prog(self):
        self.executable = self.baseprogname
        popen_specs={'stdout':subprocess.PIPE,'stdin':subprocess.PIPE,'universal_newlines':True}

        self.process = subprocess.Popen([self.executable],**popen_specs)
        time.sleep(0.02)
        return_code = self.process.poll()
        if return_code:
          raise unittest.SkipTest("Problem running your executable.\n")
        self.q = Queue()
        self.t = Thread(target=enqueue_output, args=(self.process.stdout, self.q))
        self.t.daemon = True # thread dies with the program
        self.t.start()

    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'0':100,'1':100}
        cls.Points = {"a":5,"b":5,'c':10,'d':20,'e':10,'f':10,'g':40}

        with open(tested_programs['numbers']) as f:
            cls.file_contents=f.read()

        cls.baseprogname = 'st3_numbers_'+str(random.randint(1000,100000))
        new_source_file = cls.baseprogname+".cpp"
        prog_text =real_main.replace("numbers_solution.cpp",tested_programs['numbers'])
    
        with open(new_source_file,'w') as f:
            f.write(prog_text)
        try:
            T = subprocess.run(["g++","-std=c++17",'-Wall','-Wno-sign-compare',new_source_file,"-o",cls.baseprogname],
             stderr=subprocess.PIPE,universal_newlines=True)
        except Exception as e:
          raise unittest.SkipTest("Compile failed.\n"+str(e))

        if T.returncode:
            raise unittest.SkipTest(str(T)+T.stderr)

        if T.stderr:
            print('your program compiled, but generated the following warning messages. Please check them.')
            print(T.stderr)
            print()
        os.remove(new_source_file)
      
        cls.start_prog()



    @classmethod
    def tearDownClass(cls):
       cls.process.communicate("exit\n")
       try:
        os.remove(cls.executable)
       except Exception as e:
        print(e)

    def ask_program(self, case):
        self.process.stdin.write(case+'\n')
        self.process.stdin.flush()
        words = []
        while True:
            try:  
                res = self.q.get(timeout=.1)
            except Empty:
                self.process.kill()
                
                self.start_prog() # restart executable 
                self.fail('no output\n'+case)

            if res=='.\n':
                break
            else:
                words.append(res.strip())
        return words

    def is_happy(self,n):
        res = self.ask_program(f"h\n{n}\n")
        if res == ['1']:
            return True
        elif res == ['0']:
            return False
        else:
            self.fail(f'Invalid output for is_happy: {res}')
  
    def proper_divisors(self,n):
        res = self.ask_program(f"pd\n{n}\n")
        try:
           res = [int(x) for x in res]
        except:
            self.fail(f'Invalid output for proper_divisors: {res}')
        return tuple(res)

    def product_of_positives_dbl(self,vec):
        nums="\n".join(str(x) for x in vec)
        res = self.ask_program(f"pop_d {len(vec)}\n{nums}\n")
        try:
           res = float(res[0])
        except:
            self.fail(f'Invalid output for product_of_positives_dbl: {res}')
        return res

    def product_of_positives_int(self,vec):
        nums="\n".join(str(x) for x in vec)

        res = self.ask_program(f"pop_i {len(vec)}\n{nums}\n")
        try:
           res = int(res[0])
        except:
            self.fail(f'Invalid output for product_of_positives_dbl: {res}')
        return res

    def add(self,nums):
        res = self.ask_program(f"add\n{nums}\n")
        try:
           res = res[0]
        except:
            self.fail(f'Invalid output for add: {res}')
        return res

    def test_includes(self):
        "0. check the included libraries are allowed"

        includes = ec602lib.get_includes(self.file_contents)
        invalid_includes = includes - valid_includes['numbers']
        if invalid_includes:
          self.fail('Invalid includes: {}'.format(" ".join(x for x in invalid_includes)))

    def test_brackets(self):
        "1. check for brackets"
        bracket_check(self)

    def test_happyness(self):
        "a. check is_happy for happy numbers"
        for n in Happy:
           res = self.is_happy(n)
           with self.subTest(CASE=f" is_happy({n})"):
            if res != True:
                self.fail(f'{n} is a happy number, you returned {repr(res)}')
    
    def test_unhappyness(self):
        "b. check is_happy for unhappy numbers"
        for n in UnHappy:
           res = self.is_happy(n)
           with self.subTest(CASE=f" is_happy({n})"):
            if res != False:
                self.fail(f'{n} is not a happy number, you returned {repr(res)}')

    def test_is_happy_large(self):
        "c. is_happy with larger numbers"
        h = 2214211
        u = 2342144
        self.assertTrue(self.is_happy(h),msg=f"{h} is a happy number")
        self.assertFalse(self.is_happy(u),msg=f"{u} is not happy")

    def test_proper_divisors(self):
        "d. proper_divisors"
        for n, ans in PropDivTests:
           res = self.proper_divisors(n)
           with self.subTest(CASE=f" proper_divisors({n})"):
            if res != ans:
                self.fail(f'proper_divisors({n})= {ans}\nyou returned {repr(res)}')

    def test_product_positives_int(self):
        "e. product_of_positives for int"
        for vec, ans in ProdPosTestsInt:
           res = self.product_of_positives_int(vec)
           with self.subTest(CASE=f" product_of_positives({vec})"):
            if res != ans:
                self.fail(f'product_of_positives({vec})= {ans}\nyou returned {repr(res)}')

    def test_product_positives_dbl(self):
        "f. product_of_positives for double"
        for vec, ans in ProdPosTestsDbl:
           res = self.product_of_positives_dbl(vec)
           with self.subTest(CASE=f" product_of_positives({vec})"):
            if res != ans:
                self.fail(f'product_of_positives({vec})= {ans}\nyou returned {repr(res)}')
    def test_add(self):
        "g. add tests"
        for nums, ans in AddTests:
           res = self.add(nums)
           with self.subTest(CASE=f" add({nums})"):
            if res != ans:
                self.fail(f'add({nums})= {ans}\nyou returned {repr(res)}')



testcases={'splitargs':SplitArgsTestCase,'numbers':NumbersTestCase}

if __name__ == '__main__':
    print('C++/Unix Checker Version {0}.{1}\n'.format(*VERSION))
    for prog in testcases:
        pname = tested_programs[prog]
        tcase = testcases[prog]
        refc = refcode[prog]

        first,msg, grade = ec602lib.overallcpp(pname, tcase, refc, docompile=False,)
        print(msg)
