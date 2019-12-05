"""checker for arrangements
"""
try:
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
  import string

  from threading import Thread

  from queue import Queue, Empty
except Exception as e:
    print('You are missing a part of the anaconda python3 distibution')
    print('This is required for running the checker.')
    print(e)
    quit()

VERSION, EC602VER = (3,6), (3,9)
DEBUG = False


lets = "".join(chr(33+i) for i in range(120))
lets = lets.replace("=","")


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


programs = ['arrangements.cpp']


CPPLINT_IGNORE = ['readability/alt_tokens','build/include_subdir']

MAXAUTHORS = 3

MAXSIZE = 20000

NOBRACKETS = True

AUTHWARN = "WARNING, NO VALID AUTHOR LINES FOUND"


ASTYLE_OPTIONS = [
    '--style=google', '--indent=spaces=2', '--formatted', '--dry-run'
]

REQUIRED_INCLUDES = ['algorithm','iomanip','iostream','string','vector','timer.h']

VALID_INCLUDES = REQUIRED_INCLUDES + ['array','cmath','cstdint','tuple','map','algorithm',"set","unordered_map","unordered_set"]

program_commands  = {
'panel_count':'pc',
'panel_shuffles':'ps',
'dinner_count':'dc',
"dinner_shuffles":"ds"}

full_names = {v:k for k,v in program_commands.items()}

Tests ={x:[] for x in program_commands}

Tests['pc']=[
  ('abc12 1','1'),
  ('abc12 2','2'),
  ('abc12 3','3'),
  ('!@#$% 4','5'),
  ('!@#$% 5','8'),
  (lets[:100]+" 100",'5.73147844013819e+20'),
  ("a"*26+" 26","196418")
  ]
Tests['dc']=[
  ('abc12 1','1'),
  ('abc12 2','2'),
  ('abc12 3','6'),
  ('!@#&% 4','9'),
  (lets[:100]+" 100",'7.92070839848375e+20'),
  (lets[50:96]+" 26","271445")
  ]
Tests['ps']=[
  ('abc12 2','9b1e2b25a9'),
  ('abc12 3','4b9641e0ab'),
  ('abc12 5','1c0fb84682'),
  ('12345abcdeZ 10','1cc193a1c5'),
  (lets[:15]+' 15','d2e59a4eb8'),
  ]

Tests['ds']=[
  ('abc12 2','9b1e2b25a9'),
  ('abc12 3','f555053768'),
  ('abc12 5','c68c8e0efc'),
  ('1234567890 10',"5c275b5cdc"),
  ('12345abcdeZ 11','e0c3124f47'),
  ]

speed_answers={}

speed_answers['ps']={
        21:'50e0c68665',
        22:'1e9d3a4157',
        23:'76d9b42b2f',
        24:'0e4f07da64',
        25:'53a97513d9',
        26:"80dd010b6d",
        27:"fc1a84626c",
        28:"77dde6331d",
        29:"c3d4e8e940",
        30:"b874a8550d"
        }


speed_answers['ds']={
        21:'a735edf895',
        22:'6622ec19f0',
        23:'f941784fa8',
        24:'b358fcc8f9',
        25:'53a97513d9',
        25:'a49daa40a6',
        26:"5e16ce1e05",
        27:"4820117664",
        28:"6840381969",
        29:"5122bca5e1",
        30:"2f27ca3bc2"        }

my_basic_answers = ['abcd\nabdc\nacbd\nbacd\nbadc', 'abcd\nabdc\nacbd\nbacd\nbadc\nbcda\ndabc\ndbca\ndcba', 'abcdef\nabcdfe\nabcedf\nabdcef\nabdcfe\nacbdef\nacbdfe\nacbedf\nbacdef\nbacdfe\nbacedf\nbadcef\nbadcfe\n\n123456\n123465\n123546\n124356\n124365\n132456\n132465\n132546\n213456\n213465\n213546\n214356\n214365\n\n!#@$%^\n!#@$^%\n!#@%$^\n!@#$%^\n!@#$^%\n!@#%$^\n!@$#%^\n!@$#^%\n@!#$%^\n@!#$^%\n@!#%$^\n@!$#%^\n@!$#^%', 'abcdef\nabcdfe\nabcedf\nabdcef\nabdcfe\nacbdef\nacbdfe\nacbedf\nbacdef\nbacdfe\nbacedf\nbadcef\nbadcfe\nbcdefa\nfabcde\nfbcdea\nfbceda\nfbdcea\nfcbdea\nfcbeda\n\n123456\n123465\n123546\n124356\n124365\n132456\n132465\n132546\n213456\n213465\n213546\n214356\n214365\n234561\n612345\n623451\n623541\n624351\n632451\n632541\n\n!#@$%^\n!#@$^%\n!#@%$^\n!@#$%^\n!@#$^%\n!@#%$^\n!@$#%^\n!@$#^%\n@!#$%^\n@!#$^%\n@!#%$^\n@!$#%^\n@!$#^%\n@#$%^!\n^!@#$%\n^#@$%!\n^#@%$!\n^@#$%!\n^@#%$!\n^@$#%!']
# from python with ints:
# 308061521170129
# 498454011879264
# 806515533049393
# 1304969544928657
# 2111485077978050

my_panel_count_answers = [['1', '1'], ['2', '2'], ['3', '3'], ['4', '5'], ['5', '8'], ['6', '13'], 
['7', '21'], ['8', '34'], ['9', '55'], ['10', '89'], ['11', '144'], ['12', '233'], ['13', '377'], 
['14', '610'], ['15', '987'], ['16', '1597'], ['17', '2584'], ['18', '4181'], ['19', '6765'], 
['20', '10946'], ['21', '17711'], ['22', '28657'], ['23', '46368'], ['24', '75025'], ['25', '121393'],
 ['26', '196418'], ['27', '317811'], ['28', '514229'], ['29', '832040'], ['30', '1346269'], 
 ['31', '2178309'], ['32', '3524578'], ['33', '5702887'], ['34', '9227465'], ['35', '14930352'], 
 ['36', '24157817'], ['37', '39088169'], ['38', '63245986'], ['39', '102334155'], ['40', '165580141'], 
 ['41', '267914296'], ['42', '433494437'], ['43', '701408733'], ['44', '1134903170'], 
 ['45', '1836311903'], ['46', '2971215073'], ['47', '4807526976'], ['48', '7778742049'], 
 ['49', '12586269025'], ['50', '20365011074'], ['51', '32951280099'], ['52', '53316291173'], 
 ['53', '86267571272'], ['54', '139583862445'], ['55', '225851433717'], ['56', '365435296162'], 
 ['57', '591286729879'], ['58', '956722026041'], ['59', '1548008755920'], ['60', '2504730781961'], 
 ['61', '4052739537881'], ['62', '6557470319842'], ['63', '10610209857723'], ['64', '17167680177565'], 
 ['65', '27777890035288'], ['66', '44945570212853'], ['67', '72723460248141'], ['68', '117669030460994'],
 ['69', '190392490709135'], ['70', '308061521170129'], ['71', '498454011879264'], ['72', '806515533049393'],
 ['73', '1.30496954492866e+15'], ['74', '2.11148507797806e+15'], ['75', '3.41645462290672e+15'], 
 ['76', '5.52793970088477e+15'], ['77', '8.94439432379149e+15'], ['78', '1.44723340246763e+16'], 
 ['79', '2.34167283484677e+16'], ['80', '3.7889062373144e+16'], ['81', '6.13057907216118e+16'],
  ['82', '9.91948530947558e+16'], ['83', '1.60500643816368e+17'], ['84', '2.59695496911123e+17'], 
  ['85', '4.20196140727491e+17'], ['86', '6.79891637638614e+17'], ['87', '1.10008777836611e+18'],
  ['88', '1.77997941600472e+18'], ['89', '2.88006719437082e+18'], ['90', '4.66004661037554e+18'], 
  ['91', '7.54011380474637e+18'], ['92', '1.22001604151219e+19'], ['93', '1.97402742198683e+19'], 
  ['94', '3.19404346349902e+19'], ['95', '5.16807088548585e+19'], ['96', '8.36211434898487e+19'], 
  ['97', '1.35301852344707e+20'], ['98', '2.18922995834556e+20'], ['99', '3.54224848179263e+20']]

my_dinner_count_answers = [['1', '1'], ['2', '2'], ['3', '6'], ['4', '9'], ['5', '13'], ['6', '20'], 
['7', '31'], ['8', '49'], ['9', '78'], ['10', '125'], ['11', '201'], ['12', '324'], ['13', '523'], 
['14', '845'], ['15', '1366'], ['16', '2209'], ['17', '3573'], ['18', '5780'], ['19', '9351'], 
['20', '15129'], ['21', '24478'], ['22', '39605'], ['23', '64081'], ['24', '103684'], ['25', '167763'], 
['26', '271445'], ['27', '439206'], ['28', '710649'], ['29', '1149853'], ['30', '1860500'], 
['31', '3010351'], ['32', '4870849'], ['33', '7881198'], ['34', '12752045'], ['35', '20633241'], 
['36', '33385284'], ['37', '54018523'], ['38', '87403805'], ['39', '141422326'], ['40', '228826129'], 
['41', '370248453'], ['42', '599074580'], ['43', '969323031'], ['44', '1568397609'], 
['45', '2537720638'], ['46', '4106118245'], ['47', '6643838881'], ['48', '10749957124'], 
['49', '17393796003'], ['50', '28143753125'], ['51', '45537549126'], ['52', '73681302249'], 
['53', '119218851373'], ['54', '192900153620'], ['55', '312119004991'], ['56', '505019158609'], 
['57', '817138163598'], ['58', '1322157322205'], ['59', '2139295485801'], ['60', '3461452808004'], 
['61', '5600748293803'], ['62', '9062201101805'], ['63', '14662949395606'], ['64', '23725150497409'], 
['65', '38388099893013'], ['66', '62113250390420'], ['67', '100501350283431'], 
['68', '162614600673849'], ['69', '263115950957278'], ['70', '425730551631125'], 
['71', '688846502588401'], ['72', '1.11457705421953e+15'], ['73', '1.80342355680793e+15'], 
['74', '2.91800061102745e+15'], ['75', '4.72142416783538e+15'], ['76', '7.63942477886283e+15'], 
['77', '1.23608489466982e+16'], ['78', '2.0000273725561e+16'], ['79', '3.23611226722592e+16'], 
['80', '5.23613963978203e+16'], ['81', '8.47225190700795e+16'], ['82', '1.370839154679e+17'], 
['83', '2.21806434537979e+17'], ['84', '3.58890350005879e+17'], ['85', '5.80696784543858e+17'], 
['86', '9.39587134549738e+17'], ['87', '1.5202839190936e+18'], ['88', '2.45987105364333e+18'], 
['89', '3.98015497273693e+18'], ['90', '6.44002602638026e+18'], ['91', '1.04201809991172e+19'], 
['92', '1.68602070254975e+19'], ['93', '2.72803880246146e+19'], ['94', '4.41405950501121e+19'], 
['95', '7.14209830747268e+19'], ['96', '1.15561578124839e+20'], ['97', '1.86982561199566e+20'], 
['98', '3.02544139324405e+20'], ['99', '4.8952670052397e+20']]


real_main=r"""
// TESTING: leave this line and below as is.

void show_result(vector<string> v) {
  sort(v.begin(), v.end());
  for (auto c : v)
    cout << c << "\n";
  cout << "\n";
}

void show_partial_result(string testname, vector<string> res, int n) {
  if (res.empty()) return;

  sort(res.begin(), res.end());

  std::vector<uint64_t> locs{0, res.size() / 3,
                             2 * res.size() / 3, res.size() - 1};
  std::cout << "\n" << testname << " " << n << "\n";
  for (auto i : locs) {
    std::cout << " res.at(" << i
              << ") = " << res.at(i) << "\n";
  }
}


const int COUNTLIM = 100;
const int COUNTLIM_SMALL = 30;

void standard_tests();
void interactive_main();

int main(int argc, char const ** argv) {
   if (argc > 1 and (string(*(argv + 1)) == string("int")))
    interactive_main();
  else
    standard_tests();
}

void standard_tests() {
  int n;

  cout.precision(15);

  // Basic test
  Arrangements standard;

  cout << "\nPanel Shuffles for 4 panelists.\n";
  show_result(standard.panel_shuffles(4));

  cout << "\nDinner Shuffles for 4 guests.\n";
  show_result(standard.dinner_shuffles(4));

  // Test other names
  Arrangements numbers("123456789");
  Arrangements symbols("!@#$%^&*()_+");

  std::array<Arrangements*, 3> v{&standard, &numbers, &symbols};

  cout << "\nPanel Shuffles for 6 panelists, 3 sets of names.\n";
  for (auto arr : v)
    show_result(arr->panel_shuffles(6));

  cout << "\nDinner Shuffles for 6 guests, 3 sets of names.\n";
  for (auto arr : v)
    show_result(arr->dinner_shuffles(6));

  // Count tests
  Arrangements large(string(COUNTLIM, 'a'));

  Timer t_pc("panel count", true);
  n = 1;
  cout << "\nPanel Shuffle Count Table (0.1 seconds)\n";
  cout << "     N  panel(N)\n";

  while (n < COUNTLIM and t_pc.time() < 0.1) {
    t_pc.start();
    double pc = large.panel_count(n);
    t_pc.stop();
    cout << std::setw(6) << n << " "
         << std::setw(6) << pc << "\n";
    n++;
  }


  Timer t_dc("dinner count", true);
  n = 1;
  cout << "\nDinner Shuffle Count Table (0.1 seconds)\n";
  cout << "     N  dinner(N)\n";

  while (n < COUNTLIM and t_dc.time() < 0.1) {
    t_dc.start();
    double dc = large.dinner_count(n);
    t_dc.stop();
    cout << std::setw(6) << n << " "
         << std::setw(6) << dc << "\n";
    n++;
  }

  Timer t_panel("panel", true);
  n = 4;
  cout << "\nHow many panel shuffles can be created in 0.5 seconds?\n";

  while (t_panel.time() < 0.5 and n<28)  {
    double last = t_panel.time();
    t_panel.start();
    vector<string> res = standard.panel_shuffles(n);
    t_panel.stop();
    show_partial_result("panel", res, n);
    cout << "time " << t_panel.time() - last << "\n";
    n++;
  }

  int largest_panel = n - 1;

  Timer t_dinner("dinner timing", true);
  n = 4;
  cout << "\nHow many dinner shuffles can be created in 0.5 seconds?\n";

  while (t_dinner.time() < 0.5 and n<28)  {
    double last = t_dinner.time();
    t_dinner.start();
    vector<string> res = standard.dinner_shuffles(n);
    t_dinner.stop();
    show_partial_result("dinner", res, n);
    cout << "time " << t_dinner.time() - last << "\n";
    n++;
  }
  cout << "\nLargest panel shuffles performed: "
       << largest_panel << "\n";
  cout << "\nLargest dinner shuffles performed: " << n - 1 << "\n";

  // Error checking
  Arrangements small("abcd");
  cout << "\nError Handling Tests\n";

  try {
    small.panel_count(5);
  } catch (int n) {
    cout << n;
  }
  try {
    small.panel_shuffles(6);
  } catch (int n) {
    cout << n;
  }
  try {
    small.dinner_count(7);
  } catch (int n) {
    cout << n;
  }
  try {
    small.dinner_shuffles(89);
  } catch (int n) {
    cout << n;
  }
  try {
    large.dinner_shuffles(122);
  } catch (int n) {
    cout << n;
  }
  try {
    numbers.dinner_shuffles(9);
  } catch (int n) {
    cout << n;
  }
  try {
    numbers.dinner_shuffles(10);
  } catch (int n) {
    cout << n;
  }
  cout << "\n";
}


void interactive_main() {
  std::string asktype, symbols;
  int number;
  cout << "Type quit to exit.\n";
  cout << "Commands:\npc names n\nps names n\ndc names n\nds names n\n";
  cout.precision(15);

  while (true) {
    std::cin >> asktype;
    if (asktype == "quit") break;
    std::cin >> symbols;
    Arrangements h(symbols);
    std::cin >> number;
    if (asktype == "pc") {
      std::cout << "panel_count(" << number <<  ") = ";
      std::cout << h.panel_count(number) << "\n";
    } else if (asktype == "ps") {
      std::cout << "panel_shuffles(" << number <<  ") = ";
      for (auto e : h.panel_shuffles(number) )
        std::cout << e << " ";
      std::cout << "\n";
    } else if (asktype == "dc") {
      std::cout << "dinner_count(" << number << ") = ";
      std::cout << h.dinner_count(number) << "\n";
    } else if (asktype == "ds") {
      std::cout << "dinner_shuffles(" << number <<  ") = ";
      for (auto e : h.dinner_shuffles(number))
        std::cout << e << " ";
      std::cout << "\n";
    }
  }
}
"""

COMMENT_STRING = {'py': '#', 'sh': "#", 'cpp': '//'}



def ask_program(process,case,command):
    process.stdin.write(command+'\n')
    process.stdin.write(case+'\n')
    process.stdin.flush()
    ans = process.stdout.readline().strip()
    return ans


def check(answer,youranswer,case):
    if youranswer != answer:
        return "problem with case {}\n correct: {}\n   yours: {}\n".format(case,repr(answer),repr(youranswer))   
    return ""

def hexcheck(answer,youranswer,case):
    phrase, myhex = answer.rsplit("= ",1)
    phrase, yourval = youranswer.rsplit("= ",1)
    yourval = yourval.split()
    yourval.sort()
    yourval = "\n".join(yourval)

    h = hashlib.sha256()
    h.update(yourval.encode())
    summary = h.hexdigest()[:10]

    if summary != myhex:
        return "\nproblem with case {}. My digest: {}, your digest: {}\n".format(phrase,myhex,summary)
    return ""

def numbercheck(answer,youranswer,case):
    phrase,val = answer.rsplit(" ",1)
    phrase,yourval = youranswer.rsplit(" ",1)

    if not np.isclose(float(yourval),float(val)):
        return "problem with case {}\n correct: {}\n   yours: {}\n".format(case,repr(answer),repr(youranswer))   
    return ""


checkfcn = {'pc':numbercheck,'ps':hexcheck,
                'dc':numbercheck,"ds":hexcheck}


popen_specs={'stdout':sub.PIPE,'stdin':sub.PIPE,
'stderr':sub.PIPE,'universal_newlines':True}

output_headings = ["Panel Shuffles for 4 panelists.",
"Dinner Shuffles for 4 guests.",
"Panel Shuffles for 6 panelists, 3 sets of names.",
"Dinner Shuffles for 6 guests, 3 sets of names.",
"Panel Shuffle Count Table (0.1 seconds)",
"Dinner Shuffle Count Table (0.1 seconds)",
"How many panel shuffles can be created in 0.5 seconds?",
"How many dinner shuffles can be created in 0.5 seconds?",
"Largest panel shuffles performed:",
"Largest dinner shuffles performed:",
"Error Handling Tests"]

ve_str = "your program seems to have crashed in {} using the interactive command: {} {}\n"


def cppshell(Parms,q):
      vals = main_cpp(**Parms)
 

def testfcn(self,function_to_test):
    correct = 0
    incorrect = 0
    msg = ""
    for instring,answer in Tests[function_to_test]:
        outstring = '{}({}) = {}'.format(full_names[function_to_test],",".join(instring.split()[1:]),answer)
        try:
          result = ask_program(self.process,instring,function_to_test)
          val = checkfcn[function_to_test](outstring,result,instring)
        except UnicodeDecodeError:
          val = "problem with case {}\n correct: {}\n   yours: **INVALID ASCII CHARS, CANT DECODE**\n".format(
                   instring,repr(outstring))
        except BrokenPipeError:
          val = "broken pipe crash on test: {} \n".format(instring)
        except ValueError:
          val = ve_str.format(function_to_test,full_names[function_to_test],instring)
  
        if not val:
            correct += 1
        else:
            incorrect +=1
        msg += val
    if Tests[function_to_test]:
        score = max(0,self.Points[function_to_test] * correct / len(Tests[function_to_test]))
    
    self.Points[function_to_test] = score
    if incorrect:
      self.fail(msg)


class ArrangementsTestCase(unittest.TestCase):
    "arrangements.cpp"
    @classmethod
    def tearDownClass(cls):
        try:
            D = cls.code_metrics['errors']
        except Exception as e:
            cls.fail(cls,f'Something went wrong: {e}')
        cpplint_count= sum(len(D[x]) for x in D)
        cls.msgs.append("Style Report\n============")
        as_grade = 5*cls.code_metrics['astyle']
        cls.msgs.append(f"astyle[max 5] {as_grade:.2f}")
        lint_grade = max(0, 5-cpplint_count)
        cls.msgs.append(f"cpplint[max 5] {lint_grade} (1 point deduction for each problem)")
        cls.Points['style'] = as_grade + lint_grade
        cls.msgs.append(f"overall style grade[max 10] {cls.Points['style']:.2f}")
        try:
          cls.process.stdin.write('quit\n')
          cls.process.stdin.flush()     
          time.sleep(0.2)     
          if not DEBUG:
            os.remove(cls.baseprogname)
        except Exception as e:
          print(e)

    @classmethod
    def setUpClass(cls):
        cls.Penalty = {'includes':100,'brackets':20,'authors':100}
        cls.Points = {"ds":15,"ps":15,"style":10,'speed':30,'dc':10,'pc':10,'error':10}


        cls.authorlimit = 3
        cls.valid_includes ={"cstdint","algorithm","iostream","iomanip","string","array","vector","timer.h","cmath"}
        cls.lintoptions=['-runtime/int','-readability/casting',
                         '-readability/alt_tokens','-build/include_subdir']

        cls.refcode = {'lines':163,'words':562}
        cls.msgs=[]
        cls.realfilename = tested_programs[cls.__doc__]

        with open(cls.realfilename) as f:
            cls.file_contents=f.read()

        try:
          splitter = '// TESTING: leave this line and below as is.'
          first_part,second_part=cls.file_contents.split(splitter)
        except Exception as e:
          if '\r\n' in cls.file_contents:
            cls.fail(cls,r"Detected windows CRLF newlines in your program. Please use linux '\n' newlines.")
          else:
            cls.fail(cls,"Unable to find the marker:\n{}\n".format(splitter))
        
        if cls.realfilename.startswith("st3"):
           cls.baseprogname = cls.realfilename[:-4]
        else:
           cls.baseprogname = 'st3_arr_'+str(random.randint(1000,100000))
        
        new_source_file = cls.baseprogname+".cpp"

        with open(new_source_file,'w') as f:
            f.write(first_part)
        cls.code_metrics = ec602lib.code_analysis_cpp(new_source_file,cls.lintoptions)
        with open(new_source_file,'a') as f:
            f.write(real_main)
        
        time.sleep(0.02) # give file system a chance.

        T = sub.run(["g++","-O3","-std=c++17",new_source_file,"-o",cls.baseprogname],stderr=sub.PIPE)
        errors = T.stderr.decode()
        if not DEBUG:
          os.remove(new_source_file)

        if errors:
          cls.fail(cls,"COMPILE ERRORS\n"+errors+"\nCOMPILE ERRORS\n")
        cls.process = sub.Popen([cls.baseprogname,"int"],**popen_specs)

        time.sleep(0.02)
        return_code = cls.process.poll()
        if return_code:
           # should remove new_source_file here?
           cls.fail(cls,'Your program exited with return code {}.'.format(return_code))
        # read in the help strings (6 lines)
        for i in range(6):
          val=cls.process.stdout.readline()


    def setUp(self):
        self.process = sub.Popen([self.baseprogname,"int"],**popen_specs)

        time.sleep(0.02)
        return_code = self.process.poll()
        if return_code:
           # should remove new_source_file here?
           self.fail(self,'Your program exited with return code {}.'.format(return_code))
        # read in the help strings (6 lines)
        for i in range(6):
          val=self.process.stdout.readline()

    def tearDown(self):
        try:
          self.process.stdin.write('quit\n')
          self.process.stdin.flush()     
          time.sleep(0.2)     
        except Exception as e:
          self.fail(str(e))

    test_includes = ec602lib.test_includes
    test_authors = ec602lib.test_authors
    test_style = ec602lib.test_cppstyle
    test_brackets = ec602lib.bracket_check

    def test_panel_count(self):
      "pc. panel count"
      testfcn(self,"pc")
      MX=72
      for i,ans in my_panel_count_answers:
        i=int(i)
        try:
          result=ask_program(self.process,f"{lets[:i]} {i}",'pc')
          val = result.split('=')[1].strip()
        except:
          self.fail(f"pc({i}) is crashing.")        
        if i<MX and val != ans:
            self.fail(f"pc({i})={val} != {ans}")
        elif i>=MX and not np.isclose(float(val),float(ans)):
            self.fail(f"pc({i})={val} not close to {ans}")


    def test_panel_shuffles(self):
      "ps. panel shuffles"
      testfcn(self,"ps")


    def test_dinner_count(self):
      "dc. dinner count"
      testfcn(self,"dc")
      MX=71
      for i,ans in my_dinner_count_answers:
        i=int(i)
        try:
          result=ask_program(self.process,f"{lets[:i]} {i}",'dc')
          val = result.split('=')[1].strip()
        except:
          self.fail(f"dc({i}) is crashing.")
        if i<MX and val != ans:
            self.fail(f"dc({i})={val} != {ans}")
        elif i>=MX and not np.isclose(float(val),float(ans)):
            self.fail(f"dc({i})={val} not close to {ans}")


    def test_dinner_shuffles(self):
      "ds. dinner shuffles"
      testfcn(self,"ds")

    def test_speed(self):
      "speed. check speed of shuffling"
     
      self.Points['error'] = 0
      try:
        T = sub.run([self.baseprogname],timeout=12,**popen_specs)
      except Exception as e:
        self.fail(f"Your program exceeded 12 second maximum. {e}")

   
      output = T.stdout
      if T.stderr:
        self.fail(T.stderr)
      stuff=[]
      res=""
      try:
        for heading in output_headings:
            first,second = output.split(heading)
            stuff.append(first.strip())
            output = second
      except:
        for s in stuff:
            print(len(s))
            print(output)
        self.fail(f"Unable to find the following heading in your output: {heading}\n")

      stuff.append(second.strip())
      stuff = stuff[1:]
      panel_shuffles = stuff[6]
      dinner_shuffles = stuff[7]
      try:
        largest={'ps': min(30,int(stuff[8])),'ds':min(30,int(stuff[9]))}
      except:
        self.fail("Unable to parse your output, tried to interpret\n{}\nand\n{} as numbers.".format(stuff[8],stuff[9]))
      self.errors = stuff[10]

      if self.errors == '5678912210':
          self.Points['error'] = 10


      if largest['ds']<20 or largest['ps']<20:
          res += "You must get to a threshold of 20 shuffles for both panel and dinner to get a speed score.\n"
          self.Points['speed'] = 0
      else:
          speed_ok = True
          for function_to_test in ['ps','ds']:
              answer = speed_answers[function_to_test][largest[function_to_test]-4]
              instring ="{} {}".format(string.ascii_letters,largest[function_to_test]-4)
              outstring = '{}({}) = {}'.format(function_to_test,",".join(instring.split()[1:]),answer)
              val = checkfcn[function_to_test](outstring, ask_program(self.process,instring,function_to_test), instring)
              if val:
                  res += "problem with result for {} at {}\n".format(function_to_test,largest[function_to_test]-2)
                  res += val
                  speed_ok = False

          if speed_ok:
              total_done = sum(int(largest[x]) for x in largest)
              res += f"panel shuffles performed: {largest['ps']}\n"
              res += f"dinner shuffles performed: {largest['ds']}\n"
              res += "You did {} shuffles in 1 second.\n".format(total_done)
              if total_done>=54:
                  res += "Nice work, full credit for speed.\n"
                  self.Points['speed'] = 30
              else:

                  self.Points['speed'] = (total_done-40)**2 *30 / 14**2


          else:
              res += "There is a problem, so no speed score.\n"
              self.Points['speed'] = 0

      self.msgs.append('\nSpeed Report\n============')
      self.msgs.append(res)

    def test_errors(self):
       "error. handling requirement"
       if self.Points['error']==0:
            self.fail('Error handling not working.')
      



testcases={'arrangements.cpp':ArrangementsTestCase}

programs = ['arrangements.cpp']

tested_programs = {x:x for x in programs}

testorder =["authors","includes","brackets","style","pc","dc",'ps','ds','error','speed']

if __name__ == '__main__':
    s= ' (arrangements Checker Version {0}.{1})'.format(*VERSION)
    print('arrangements checker version',VERSION)
    g={}
    for prog in testcases:
        report, g[prog] = ec602lib.check_program(testcases[prog],testorder,s)
        print(report)
    print('\nGrade Summary')
    for prog in testcases:
      print(prog,g[prog])