# Table of Contents
1. [Challenge Summary](README.md#challenge-summary)
2. [Details of Implementation](README.md#details-of-implementation)

# Challenge Summary
Written in python3, using only default python modules :)

To run unittests use the following command:
'''python3 -m unittest insight_testsuite/tests/test_process/[test file]'''


## Details of Implementation
### Feature 1
Parsed the log file and built a list of tuples containing the frequency count and the ip address, plus dictionary tracking where specific ip addresses are in the list (index value). I used a list of tuples because it meant I could take advantage of python's timesort algorithm while still keeping the count and the ip address associated.
### Feature 2
Building on the process in Feature 1, but doing some additional parsing of the block containing resource information.
### Feature 3
This one was tricky because many of the top periods of traffic actually overlap. So I started by isolating traffic peaks and filtering the top ones so that there were at least 3,600 seconds away from one another. For each peak I built a sublist consisting of 3,600s before the peak and 3,600 after, then stepped through the sublist doing sums of 3,600 values to identify both the maximum value for that period and where it starts.
### Feature 4
Reused some of work for Feature 3 to calculate the gaps between failed requests. Had to change the encoding to ascii to take advantage of the speed and efficiency of slicing instead of regex or substring searching.
