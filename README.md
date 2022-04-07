# Organizing and Submitting HTC Workloads

Imagine you have a collection of books, and you want to analyze how word
usage varies from book to book or author to author. 

This tutorial starts with the same set up as 
our [Wordcount Tutorial for Submitting Multiple Jobs](https://support.opensciencegrid.org/support/solutions/articles/12000079856-wordcount-tutorial-for-submitting-multiple-jobs), but 
focuses on how to organize that example more effectively on the Access Point, 
with an eye to scaling up to a larger HTC workload in the future. 

## Our Workload

We can analyze one book by running the `wordcount.py` script, with the 
name of the book we want to analyze: 

	$ ./wordcount.py Alice_in_Wonderland.txt 

Try running the command to see what the output is for the script. Once you have done that
delete the output file created (`rm counts.Alice_in_Wonderland.txt`).

We want to run this script on all the books we have copies of. 

1. What is the input set for this HTC workload?
2. What is the output set?

## Make an Organization Plan

Based on what you know about the script, inputs, and outputs, how would 
you organize this HTC workload in directories (folders) on the access point? 

Try making those changes before moving on to the next section of the tutorial. 

## Organize Files

There are many different ways to organize files; a simple example that works 
for most workloads is having a directory for your input files and a directory 
for your output files. We can set up this structure on the command line by running: 

	$ mkdir input
	$ mv *.txt input/
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
	transfer_output_files   = counts.Alice_in_Wonderland.txt
	transfer_output_remaps  = "counts.Alice_in_Wonderland.txt=output/counts.Alice_in_Wonderland.txt"

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
	counts.Alice_in_Wonderland.txt

This is good! It means our organizational system is working. 

Note that some additional files have been created in the main directory: 

	$ ls

These are the standard error, standard output and HTCondor log file. It would be 
a good idea to separate these into their own directory or directories so that we 
still have them, but they aren't cluttering up our main directory. 

First we have to create directories for them:

	$ mkdir logs
	$ mkdir errout

Then, we have to edit the submit file lines that create these files, so that they 
go into this new directory: 

	$ nano books.submit
	output        = logs/job.$(ClusterID).$(ProcID).out
	error         = errout/job.$(ClusterID).$(ProcID).err
	log           = errout/job.$(ClusterID).$(ProcID).log

We can move the currently existing files ourselves:

	$ mv job.*.log logs/
	$ mv job.*.err job.*.out stderr

## Submit Multiple Jobs

Finally, we are sufficiently organized to submit our whole workload

First, we need to create a file with our input set -- in this case, it will be a list of the 
book files we want to analyze. We can do this by using the shell's listing command `ls` and 
redirecting the output to a file: 

	$ cd input
	$ ls > booklist.txt
	$ cat booklist.txt
	$ mv booklist.txt ..
	$ cd ..

Then, we modify our submit file to reference this input list and replace the static values 
from our test job (`Alice_in_Wonderland.txt`) with a variable -- we've chosen `$(book)` below: 

	$ nano books.submit

	executable    = wordcount.py
	arguments     = $(book)

	transfer_input_files    = input/$(book)
	transfer_output_files   = counts.$(book)
	transfer_output_remaps  = "counts.$(book)=output/counts.$(book)"
	
	# other options
	
	queue book from booklist.txt

Once this is done, you can submit the jobs as usual: 

	$ condor_submit books.submit
