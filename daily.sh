#!/bin/bash

# daily script

# runs our front end over a set of transactions in SESH
# saves Transaction Summary files to TRANS_SUM directory
count=0
for i in ./SESH/*.txt
do
	((count++))
	FILE=$i
	cat $FILE | while read line
	do
		echo $line
	done | python ../frontEnd.py
	cp ./transactionSummary.txt ./TRANS_SUM/sum$count.txt
done

# merge Transaction Summary files with python script
now=$(date +"%T")
cat ./TRANS_SUM/sum*.txt > ./mergedTransactions.txt
cp ./mergedTransactions.txt ./mergedTransactions_$now.txt

# run back-office on the Merged Transaction Summary file
python ../backOffice.py