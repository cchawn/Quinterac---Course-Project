#!/bin/bash

# CHRISTINA CHAN
# LAURA BROOKS

# weekly script

# run daily script 5 times (with different transactions)
# use masterAccounts + validAccounts from previous day
# information for each day is located in it's own directory

cd 1_MON
../daily.sh
cd ..
cp ./1_MON/masterAccounts.txt ./2_TUES/masterAccounts.txt
cp ./1_MON/validAccounts.txt ./2_TUES/validAccounts.txt

cd 2_TUES
../daily.sh
cd ..
cp ./2_TUES/masterAccounts.txt ./3_WED/masterAccounts.txt
cp ./2_TUES/validAccounts.txt ./3_WED/validAccounts.txt

cd 3_WED
../daily.sh
cd ..
cp ./3_WED/masterAccounts.txt ./4_THUR/masterAccounts.txt
cp ./3_WED/validAccounts.txt ./4_THUR/validAccounts.txt

cd 4_THUR
../daily.sh
cd ..
cp ./4_THUR/masterAccounts.txt ./5_FRI/masterAccounts.txt
cp ./4_THUR/validAccounts.txt ./5_FRI/validAccounts.txt

cd 5_FRI
../daily.sh
cd ..