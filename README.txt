This program is written in Python 3.9.2.
To run this program, you need to call it with python3.

Inputs:
---------------------------------------------------------------
The program takes 2 inputs as command line arguments.
One of them is mandatory and other one is optional.
The syntax is
    python3 q3main.py <x> <alpha>
where <x> is in question 3.x, for 1 <= x <= 4.
For example, to get the results for Q3.1, x should be one.
    python3 q3main.py 1

If the input is not in the range [1,4] program gives an error.
Similarly, if the number of arguments < 1 or > 2, program
gives an error.

Although <x> argument is mandatory, <alpha> is optional.
For questions 3.1, 3.2 and 3.4, <alpha> is not significant
(does not change the result) but for question 3.3, specified
<alpha> value is used for calculation. If <alpha> value 
is not specified, default value of <alpha>(1) will be used.

    python3 q3main.py 3 4
This command calculates results for <alpha> = 4.

    python3 q3main.py 3
This command calculates results for <alpha> = 1, which is the 
default value.

Outputs:
---------------------------------------------------------------
Outputs of the program are quite easy to understand. 

For question 1, program gives an output as follows:
    Taking y_train
    There are 4085 emails, where 2911 of them are spams and 1174 of them are not
    %71.26070991432069 spams and %28.739290085679315 not spams

This output is used in the report. 
Lines similar to the first line makes it easy to understand what the 
program is doing.
Second line shows the number of spam, normal and total emails in the dataset.
Third line shows the ratios of spam and normal emails among all emails.

For questions 2, 3 and 4, program gives an output similar to this:
    Taking y_train
    Taking vocabulary
    Taking x_train
    Calculating MLE's
    Taking x_test
    Taking y_test
    Testing results
    ----------------------------
    Results
    ----------------------------
    Accuracy rate: 73.20441988950276
    Confusion matrix: 
    -------
    475   5 
    286 320 
    -------
    Number of wrong predictions: 291

The program first prints current steps until calculations are done. 
At the end, it prints the results. Results consist of accuracy rate,
confusion matrix and number of wrong predictions.




