# Problem B: Clean Research (40%)

Write a program that reads data about a medical trial
from a file and cleans up inconsistencies.

Each line of the file contains the date of the test,
an id number for the patient, and the concentration of 
cholesterol in the blood, measured in mg/dL.

Here is an example

56112 12/16/19  231.2 

This means patient 56112 had a measured cholesteral of 
231.2 mg/dL on 12/16/19.

Unfortunately, the data entry has not been consistent,
and the three values can be in any order on the line.

So, the entry above could appear as


56112 231.2 12/16/19

or 

231.2 12/16/19 56112

and so forth.

Another problem with the data is that some tests have
been entered twice. Each patient was only tested once
a day, so if there are two entries for the same 
patient, it represents a duplicate.

Write a program that takes the filename of the database
as the first argument, and outputs a cleaned up version
of the database to the filename (which will be the 
second argument). The cleaned up version should output
the tests in order of the date of the test, then sorted
by the ID number of the patient. The output format should
be 

DATE PATIENTID MEASUREMENT

so the above data would be

12/16/19 56112 231.2

The program will be run as follows:

cleanresearch inputfilename outputfilename


There are no restrictions on imports/includes

The file you submit must be cleanresearch.x where x is the standard extension
for whichever programming language you have solved the problem.
