#!/bin/bash                                                                                                                   

# LAURA BROOKS                                                                                                   
# CHRISTINA CHAN                                                                                                  

# testing functionality of script                                                                                             
# for every file in the TESTS directory:                                                                                      
#   open file, that has test inputs                                                                                           
#   pipe these commands into the python script                                                                                
#   redirect the output to a file
#	copy transaction summary file to OUTPUT directory                                                                                             
count=0
for i in TESTS/*.txt
do
    ((count++))
    FILE=$i
    cat $FILE | while read line
    do
        echo $line
    done | python CTSystem_v2.py > ./OUTPUT/ACTUAL/CONSOLE/out$count.txt
	cp ./transactionSummary.txt ./OUTPUT/ACTUAL/TRANS_SUM/sum$count.txt
done