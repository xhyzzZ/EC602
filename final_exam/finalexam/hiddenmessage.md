# Problem C: Hidden Message (20%)

A message is hidden in a text file in the following way:

The ASCII codes for the letters a-z are repeated in groups
of 25 codes. For each group of codes, the letter that is 
missing represents the letter of the hidden message. The
ASCII code for anything other than a-z is also part of the
message.

Here is the message "cat.", which is also provided
in the file collection as cat_msg.txt:

```
98 97  100 101 102 103 104 105 106 107 108 109 
110 111 112 113 114 115 116 117 118 119 120 121 
122  98 99 100 101 102 103 104 105 106 107 108 
109 110 111 112 113 114 115 116 117 118 119 120 
121 122 97 98 99 100 101 102 103 104 105 106 107 
108 109 110 111 112 113 114 115 117 118 119 120 
122 121 46 
```


Notice that 99 ('c'), 97 ('a') and 116 ('t') are missing from each group of 25 letter codes.

Also, notice that 46 ('.') was added to the 
message 

In the real messages, the ASCII codes are not necessarily in order.

If a character code for anything other than a-z occurs
within the group of 25 message letters, then that letter comes before the current coded-letter.

So, for example,

```
98 97  100 101 102 103 104 105 106 107 108 109 
110 111 112 113 114 115 116 117 118 119 120 121 
122  98 99 100 101 102 103 104 105 106 107 108 
109 110 111 112 113 114 115 116 117 118 119 120 
121 122 97 98 99 100 101 102 103 104 105 106 107 
108 109 110 111 112 113 114 115 117 118 119 120 
122 46 121
```

would be the code for "ca.t" because the 46 ('.')
comes  within the block of letters coding "t"


## Program specification

Your program should be called hiddenmessage.x 
and the name of the file  with the message specified on the command line.

The output of the program should be the message, printed to stdout.

If the message is invalid for any reason, the program
should exit with a return code of 1.

Suppose the message for "cat." is stored in 

