# Organizing Files

Imagine you have a collection of books, and you want to analyze how word
usage varies from book to book or author to author. 

## Our Workload

We can analyze one book by running the `wordcount.py` script, with the 
name of the book we want to analyze: 

	$ ./wordcount.py Alice_in_Wonderland.txt 

Try running the command to see what the output is for the script. 

We want to run this script on all the books we have copies of. 

1. What is the input set for this HTC workload?
2. What is the output set?

## Make an Organization Plan

Based on what you know about the script, inputs, and outputs, how would 
you organize this HTC workload in folders? 

Try making those changes before moving on to the next section of the tutorial. 

## Organize Files

There are many different ways to organize files; a simple example that works 
for most workloads is having a directory for your input files and a directory 
for your output files. We can set up this structure on the command line by running: 

	$ mkdir input
	$ mv *.txt intput/
	$ mkdir output/

We can view our current directory and its subdirectories by using the recursive flag 
with the `ls` command: 

	$ ls -R
	README.md    books.submit input        output       wordcount.py

	./input:
	Alice_in_Wonderland.txt Huckleberry_Finn.txt    Ulysses.txt
	Dracula.txt             Pride_and_Prejudice.txt

	./output:

## Submit One Job

Now we want to submit a test job that uses this organizing scheme, using just 
one item in our input set -- in this example, we'll use the `Alice_in_Wonderland.txt` 
file from our `input/` directory. The lines that need to be filled in are shown 
below and can be edited using the `nano` text editor: 

	$ nano books.submit

	executable    = wordcount.py
	arguments     = Alice_in_Wonderland.txt

	transfer_input_files    = input/Alice_in_Wonderland.txt
	transfer_output_files   = counts.Alice_in_Wonderland.tsv
	transfer_output_remaps  = "counts.Alice_in_Wonderland.tsv=output/counts.Alice_in_Wonderland.tsv"

Note that to tell HTCondor the location of the input file, we need to include 
the input directory. We're also using a submit file option called 
`transfer_output_remaps` that will essentially move the output file to our 
`output/` directory by renaming or remapping it. 

Once you've made the above changes to the `books.submit` file, you can submit it, 
and monitor its progress: 

	$ condor_submit books.submit
	$ condor_watch_q

(Type `CTRL`-`C` to stop the `condor_watch_q` command.)

## Organizing Files, Part II

Once the job finishes, we can check to see if it ran successfully and produced the output
we expect:

	$ ls output/
	counts.Alice_in_Wonderland.tsv

This is good! It means our organizational system is working. 

Note that some additional files have been created in the main directory: 

	$ ls

These are the standard error, standard output and HTCondor log file. It would be 
a good idea to separate these into their own directory or directories so that we 
still have them, but they aren't cluttering up our main directory. 

First we have to create a folder for them:

	$ mkdir logging

Then, we have to edit the submit file lines that create these files, so that they 
go into this new directory: 

	$ nano books.submit
	output        = logging/job.$(ClusterID).$(ProcID).out
	error         = logging/job.$(ClusterID).$(ProcID).err
	log           = logging/job.$(ClusterID).$(ProcID).log

We can move the currently existing files ourselves:

	$ mv job.* logging/

## Submit Multiple Jobs

> TO DO