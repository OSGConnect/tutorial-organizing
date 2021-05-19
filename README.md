# Counting Words in Files

Imagine you have a collection of books, and you want to analyze how word
usage varies from book to book or author to author. 

## Analyzing One Book

We can analyze one book by running the `wordcount.py` script, with the 
name of the book we want to analyze: 

	$ ./wordcount.py Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt 

If we wanted to submit a single job that ran this command and analyzed the 
Alice's Adventures in Wonderland book, the submit file would look like this: 


	$ cat wordcount-alice.submit

	executable = wordcount.py
	arguments = Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt

	transfer_input_files    = Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt
	should_transfer_files   = Yes
	when_to_transfer_output = ON_EXIT

	output        = logs/job.$(Cluster).$(Process).out
	error         = logs/job.$(Cluster).$(Process).error
	log           = logs/job.$(Cluster).$(Process).log

	requirements   = (OSGVO_OS_STRING == "RHEL 7")
	request_cpus   = 1
	request_memory = 512MB
	request_disk   = 512MB

	queue 1     

Let's remove the previous output we created and then submit this job: 

	$ rm counts_Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt 
	$ condor_submit wordcount-alice.submit

You can check the job's progress using `condor_q`. Once it finishes, you should 
see the same `counts_Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt` output. 

## Analyzing Multiple Books

Now suppose you wanted to analyze multiple books - more than one at a time. 
You could create a separate submit file for each book, and submit all of the
files manually, but you'd have a lot of file lines to modify each time
(in particular, the "arguments" and "transfer_input_files" line from the 
previous submit file. 

This would be overly verbose and tedious. HTCondor has options that make it easy to 
submit many jobs from one submit file. 

First, in our submit file, every time we used the name of the book (in the previous example, 
everywhere you see "Alices_Adventures_in_Wonderland_by_Lewis_Carroll.txt") should be 
replaced with a variable. HTCondor's variable syntax looks like this: `$(variablename)`

For this example, we can use the variable `$(book)`, which you can see in the 
`wordfreq-books.submit` file:

	$ cat wordcount-alice.submit

	executable = wordcount.py
	arguments = $(book)

	transfer_input_files    = $(book)
	should_transfer_files   = Yes
	when_to_transfer_output = ON_EXIT

	output        = logs/job.$(Cluster).$(Process).out
	error         = logs/job.$(Cluster).$(Process).error
	log           = logs/job.$(Cluster).$(Process).log

	requirements   = (OSGVO_OS_STRING == "RHEL 7")
	request_cpus   = 1
	request_memory = 512MB
	request_disk   = 512MB

	queue book from book.list 

See also the last line of this submit file - here we are providing a file (`book.list`) 
with the names of all the different books we want to analyze. 

Our final step is to create this list of input values in a file 
called `book.list`. We can easily create this list by using an `ls` command and 
sending the output to a file: 

	$ ls *.txt > book.list 

We're now ready to submit all of our jobs. 

	$ condor_submit wordfreq-books.submit

This will now submit five jobs (one for each book on our list). Once all five 
have finished running, we should see "counts" files for each book in the directory. 