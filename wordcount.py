#!/usr/bin/env python

import os
import sys
import operator

if len(sys.argv) != 2:
    print 'Usage: %s DATA' % (os.path.basename(sys.argv[0]))
    sys.exit(1)
input_filename = sys.argv[1]

words = {}

my_file = open(input_filename, 'r')
for line in my_file:
    line_words = line.split()
    for word in line_words:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
my_file.close()

output_filename = "counts_"+input_filename
sorted_words = sorted(words.items(), key=operator.itemgetter(1))
my_file = open(output_filename, 'w')
for word in sorted_words:
    my_file.write('%s %8d \n' % (word[0], word[1]))
my_file.close()

