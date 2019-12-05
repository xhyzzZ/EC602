"""This program generates a collection
of results (saved in text files) for the spheres problem by
repeatedly running spheres.py with the 
parameters specified in the list "spheres_tests"
defined below.

The file name is partly based on "myid"

My results were created with "myid" set to jbc

You should change this variable so you can
compare your results with mine.

"""

myid = "xhy"

from subprocess import run, PIPE

spheres_tests=[
('tennisball',100,3),
('tennisball',10.41,2),
('zmover',100,3),
('xyzmovers',200,2),
('three',120,2), # min radius is 120
('threeonxaxis',50,4),
('diagonal',100,2),
('randompool',200,5),
('lineup',2000,2),
('smashup',2000,5),
('slow',2000,2),
('glancing',40,2)]


for basename,radius,N in spheres_tests:
    with open(f'{basename}.txt') as g:
        text = g.read()

    T = run(['spheres',str(radius),str(N)],input=text,stdout=PIPE,
          universal_newlines=True)
    
    with open(f"{basename}_{radius}_{N}_{myid}.txt",'w') as out:
        out.write(T.stdout)
    