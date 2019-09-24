import dis
import os
import random
import subprocess
import time
import unittest
import sys
import multiprocessing
from io import StringIO
import logging
import importlib
import re


VERSION = (2,1)

TESTFCNS=['is_happy','product_of_positives','proper_divisors']

refcode={'lines':22,'words':80}

max_authors = 1

comment_string = {'py': '#', 'sh': "#",  'cpp': '//'}

def read_file(filename):
    "read the contents of filename into string"
    filehand = open(filename)
    contents = filehand.read()
    filehand.close()
    return contents


def get_python_imports(file_contents):
    "get the imports of file_contents as a set"
    try:
        instructions = dis.get_instructions(file_contents)
        imports = [__ for __ in instructions if 'IMPORT' in __.opname]
    except:
        return {'ERROR PROCESSING PYTHON SCRIPT'}

    grouped = set()
    for instr in imports:
        if instr.opname == "IMPORT_NAME":
            grouped.add(instr.argval)

    return grouped

def get_authors(file_contents, ptype):
    Authors = []
    for line in file_contents.lower().splitlines():
        if line.startswith(comment_string[ptype]) and "copyright" in line:
            try:
                _, email = line.rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    Authors.append(email)
            except:
                pass
    return Authors

def repeat_terminate(T,wait):
    while T.is_alive():
        T.terminate()
        time.sleep(wait)


def silent_import(fname, q):

    s = StringIO()
    sys.stdout = s

    themod = None
    try:
        themod = importlib.import_module(fname)
    except Exception as e:
        q.put("fail")
        return
    q.put("success")


def my_import(modname, code):
    filename = modname+".py"
    with open(filename,'w') as f:
        f.write(code)

    q = multiprocessing.Queue()

    T = multiprocessing.Process(target=silent_import,args=(modname, q))
    T.start()
    try:
        result = q.get(True,1) 
    except Exception as e:
        repeat_terminate(T,0.1)
        return False

    if result=="success":
        return importlib.import_module(modname)
    return False


def progtype(program):
    try:
        _, program_type = program.split('.')
    except:
        return 'sh'
    return program_type

testwords = ['apple', 'orange', 'kiwi', 'banana',
             'strawberry', 'pineapple', 'raspberry','tomato']


Happy = [1, 31, 91, 291, 301, 331, 391, 671, 761, 881, 901, 921, 931]
UnHappy = [11, 21, 41, 51, 61, 71, 81, 101, 111, 121, 961, 971, 981, 991]

PropDivTests = [(2, (1,)), (6, (1, 2, 3)), (28, (1, 2, 4, 7, 14)), (31, (1,)), 
(100, (1, 2, 4, 5, 10, 20, 25, 50)), (2342, (1, 2, 1171)), 
(1000, (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500)), 
(9240, (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 20, 21, 22, 24, 28, 30, 33, 35, 40, 
    42, 44, 55, 56, 60, 66, 70, 77, 84, 88, 105, 110, 120, 132, 140, 154, 165, 168, 210, 220, 
    231, 264, 280, 308, 330, 385, 420, 440, 462, 616, 660, 770, 840, 924, 1155, 1320, 1540, 1848, 2310, 3080, 4620))]

ProdPosTests = [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
 8841761993739701954543616000000), 
((-1, -2, 3), 3), ((2, 0, 3), 6), ([-9, -8, -7, -6, -5, -4, -3, -2], 1), 
((0.5, 2, -1, 0.1, 100.5), 10.05), ((-1, 5, 6, 5, -1, 2, -0.1), 300)]

class numbersTestCase(unittest.TestCase):
    def test_happyness(self):
        "a. check is_happy for happy numbers"
        for n in Happy:
           res = is_happy(n)
           with self.subTest(CASE=f" is_happy({n})"):
            if res != True:
                self.fail(f'{n} is a happy number, you returned {repr(res)}')
    def test_unhappyness(self):
        "b. check is_happy for unhappy numbers"
        for n in UnHappy:
           res = is_happy(n)
           with self.subTest(CASE=f" is_happy({n})"):
            if is_happy(n) != False:
                self.fail(f'{n} is not a happy number, you returned {repr(res)}')
    def test_is_happy_large(self):
        "c. is_happy with larger numbers"
        h = int("1"*10+"0"*100+"1"*21)
        u = int("1"*10+"0"*100+"1"*31)
        self.assertTrue(is_happy(h),msg=f"{h} is a happy number")
        self.assertFalse(is_happy(u),msg=f"{u} is not happy")
    def test_proper_divisors(self):
        "d. proper_divisors"
        for n, ans in PropDivTests:
           res = proper_divisors(n)
           with self.subTest(CASE=f" proper_divisors({n})"):
            if res != ans:
                self.fail(f'proper_divisors({n})= {ans}\nyou returned {repr(res)}')
    def test_product_positives(self):
        "e. product_of_positives"
        for n, ans in ProdPosTests:
           res = product_of_positives(n)
           with self.subTest(CASE=f" product_of_positives({n})"):
            if res != ans:
                self.fail(f'product_of_positives({n})= {ans}\nyou returned {repr(res)}')



def check_program(testclass):
    """return any errors as a list of strings"""
    errors = []
    passed = []
    gradesummary = {'pass': [], 'fail': []}

    if hasattr(testclass, "setUpClass"):
        testclass.setUpClass()

    loader = unittest.loader.TestLoader()
    tests = loader.loadTestsFromTestCase(testclass)
    for test in sorted(tests, key=lambda x: x.shortDescription()):
        run = test.run()
        if run.wasSuccessful():
            passed.append('Passed: {}\n'.format(test.shortDescription()))
            gradesummary['pass'].append(test.shortDescription()[0])
        else:
            err = 'Failed: {}\n'.format(test.shortDescription())
            for testmsg, res in run.failures + run.errors:
                casetext = re.search(".*CASE='(.*)'", str(testmsg))
                if casetext:
                    err += "CASE: {}\n".format(casetext.group(1))
                if 'AssertionError:' in res:
                    _, msg = res.split('AssertionError: ')
                else:
                    msg = res
                err += msg
            errors.append(err)
            gradesummary['fail'].append(test.shortDescription()[0])

    if hasattr(testclass, "tearDownClass"):
        testclass.tearDownClass()

    return errors, passed, gradesummary


def test_numbers(actualname,code=None):

    chk = one_checker
    module_name = "numbersx_"+str(random.randint(1000,100000))
    chk.progname = module_name+".py"

    with open(chk.progname,'w') as f:
        f.write(code)

    module_tested = my_import(module_name, code)

    if not module_tested:
        logging.warning('Unable to import your module.')
        os.remove(chk.progname)
        return False,'Unable to import your module. Timeout or error',0



    for fcn in TESTFCNS:
        if hasattr(module_tested,fcn):
            setattr(chk,fcn,getattr(module_tested,fcn))
        else:
            os.remove(chk.progname)
            return False, f"No function named {fcn}. Test aborted.",0

    try:

        st = time.time()
        q = multiprocessing.Queue()
        T = multiprocessing.Process(target=pyshell,args=(chk.numbersTestCase,q))
        T.start()
        try:
            result = q.get(True,2)
        except:
            #logging.info('trying to kill'+str(T)+"authors:"+str(authors))
            repeat_terminate(T,0.1)
            raise TimeoutError()
        duration = time.time() - st
        #logging.info("duration"+str(authors)+ " " + str(duration))

        errors, passed, gradesummary = result
    except TimeoutError:
        #logging.warning('Timeout error:'+str(authors))
        return False,'ERROR. Your program is taking too long to test.',0
    except Exception as e:
        #logging.warning("Your program crashed the checker: {}".format(e))
        return False,"Your program crashed the checker: {}".format(e),0
    finally:
        os.remove(chk.progname)


    Penalty = {"a":15,"b":15}
    Points = {"a":15,'b':15,'c':10,'d':30,'e':30}


    grade, grade_report = make_grades(gradesummary,Penalty,Points)
    msg = ''.join(passed)+''.join(errors)+grade_report

    return (not bool(errors), msg, grade)


def test_splitargspy(actualname,code=None):
    s = ""
    for n in [0, 3, 4, 5, 7]:
        words = random.sample(testwords, n)
        try:
            T = subprocess.run(['python', actualname, *words],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,timeout=2)
        except:
            s +="your script timed out."
            return (False,s,0)

        if T.stdout.decode() != ''.join([a+'\n' for a in words[:4]]):
            s += f"Your stdout is not correct for {n} arguments.\n"
        if T.stderr.decode() != ''.join([a+'\n' for a in words[4:]]):
            s += f"Your stderr is not correct for {n} arguments.\n"
    if s:
        return (False,s,0)
    else:
        return (True,'Grade: 100\n',1)


DIR='files_for_args_checker'
def make_files():
    this_dir = os.getcwd()
    if DIR not in os.listdir():
        os.mkdir(DIR)
        os.system('wget -N curl.bu.edu/static/content/ec602_fall19/test_files.zip')
        os.system('unzip test_files.zip')

    testfiles = ['one','two.txt','three.py','four.cpp','five.md','six.exe','seven.java']
    
    return testfiles


def test_oldest(actualname,code=None):
    orderedfiles = make_files()
    orderedfiles.reverse()

    this_dir = os.getcwd()
    os.chdir(DIR)
    
    s = ""
    for n in [1,3,6]:
        try:
            T = subprocess.run(['../'+actualname,str(n)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True,timeout=5)
        except TimeoutError:
            s +="your script timed out.\n"
            continue
        except Exception as e:
            s += f"exception: {e}\n"
            continue

        output = T.stdout.strip().split('\n')
        if output != orderedfiles[:n]:
            s += f"your script failed on the case {actualname} {n}\n"
            s += f"your output: {output}\n"
            s += f"correct output: {orderedfiles[:n]}\n"
        
    
    os.chdir(this_dir)

    if s:
        return (False, s, 0)
    else:
        return (True,"Grade: 100\n",1)


programs = {'splitargs.py': test_splitargspy,
            'oldest':test_oldest,
            "numbers.py":test_numbers}


def make_grades(gradesummary,Penalty,Points,special_str="",spec_grade=0):
    grade = 0
    grade_report = special_str

    grade_report += "Points for passed tests: "
    for test in sorted(Points):
        if test in gradesummary['pass']:
            grade_report += "{}({}) ".format(test,Points[test])
            grade += Points[test]
    grade_report += "\n"

    for test in Penalty:
        if test in gradesummary['fail']:
            grade_report += "Penalty for fail {}: {}\n".format(test,Penalty[test])
            grade -= Penalty[test]
   
    grade = max(grade+spec_grade,0)
    grade_report += "Grade: {}\n".format(grade)

    return grade, grade_report


def pyshell(testclass,q):
      errors, passed, gradesummary = check_program(testclass)    
      q.put([errors, passed, gradesummary])

def analyse(program,actualprogramname=None):
    
    actualprogramname = actualprogramname or program

    s = f'Checking {program}.\n'
    ptype = progtype(program)
    try:
        f = open(actualprogramname)
        contents = f.read()
        f.close()
    except:
        s += f'The program {actualprogramname} does not exist here.\n'
        return 'No file', s

    the_program = read_file(actualprogramname)
    authors = get_authors(the_program, 'py')
    imported = get_python_imports(the_program)

    s += 'imported modules : {}\n'.format(" ".join(imported))

    if program=="numbers.py":
        if imported:
            s+= "you may not import any modules in this assignment"
            return False,s
    elif program=="oldest":
        s += 'imported modules : {}\n'.format(" ".join(imported))

        # include tests
        if 'sys' not in imported:
            s+= "you will need to import sys for this assignment."
            return False,s
        elif 'os' not in imported:
            s+= "you will need to import os for this assignment."
            return False,s            
        else:
            if the_program.count('sys') > 1 or the_program.count('from sys import argv') != 1:
                s += 'you must import sys once using "from sys import argv". Please correct'
                return False,s
            if the_program.count('os') > 1 or the_program.count('from os import listdir, stat') != 1:
                s += 'you must import os once using "from os import listdir, stat". Please correct'
                return False,s


    authors = get_authors(contents, ptype)
    s += 'authors       : {}\n'.format(" ".join(authors))

    if ptype=='sh' and 'sudo' in contents:
        s += "Please do not use sudo in your program."
        return False, s
    
    if len(authors) > max_authors:
        s += "You have exceeded the maximum number of authors.\n"
        return 'Too many authors', s

    summary, results, gradesummary = programs[program](actualprogramname,the_program)
    s += 'program check :'
    if not summary:
        s += " failed.\n"
        s += results
        return False, s
    else:
        s += " passed.\n"
        s += results
        return "Pass", s

one_checker=sys.modules[__name__]

if __name__ == '__main__':
    print('Python and Unix Checker Version {0}.{1}\n'.format(*VERSION))
    for program in programs:
        summary, results = analyse(program)
        print(results)