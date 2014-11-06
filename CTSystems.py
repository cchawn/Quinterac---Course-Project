#Christina Chan
#Laura Brooks

# Queen's University
# CISC 327: Software Quality Assurance
# Create the front end for a banking system
# automate testing

import Queue
import re

def pad(type, str):
        if type == "account":
                return str.zfill(6)
        elif type == "name":
                return str.ljust(15)
        elif type == "amount":
                return str.zfill(8)

def getAccountNum(msg):
    # check account number is valid format
    accountNum = raw_input("Enter account number to " + msg +":\n")
    accountNum = accountNum.strip()
    accountNum = pad("account", accountNum)
    if re.match('^[0-9]{6}$', accountNum) and not re.match('^0+$', accountNum):
        # if accountNum is valid length digits, and it's not all zeroes
        return accountNum
    else:
        print "Error: invalid account number"
        return 0
        
def getAmount(mode):
    # check account number is valid format
    amount = raw_input("Enter amount:\n")
    amount = amount.strip()
    for char in amount:
        if not char.isdigit():
                print "Error: invalid amount"
                return -1
    amount = pad("amount", amount)
    if mode == "agent":
        max = 100000000
    elif mode == "retail":
        max = 100001
    else:
        max = 0
    if int(amount) < max:
            if re.match('^[0-9]{8}$', amount):
                # if amount is valid
                return amount
            else:
                print "Error: invalid amount"
                return -1
    else:
            print "Error: invalid amount"
            return -1

def getName():
    # get account name from standard input
    # check formatting
    accountName = raw_input("Enter account name:\n")
    accountName = accountName.strip()  
    accountName = pad("name", accountName)
    if re.match('^.{15}$', accountName):
            return accountName
    else:
            print "Error: invalid account name"
            return 0

def create(list):
    # only in Agent mode
    # create a new account
    # takes name + new account number as textline
    # save account for Transaction Summary file
    #print"create"
    accountNum = getAccountNum("create") #checks format
    if accountNum in list:
            print "Error: account already exists"
            return 0
    elif accountNum != 0:
        # check that accountNum is valid (doens't already exist)
        accountName = getName()
        if accountName != 0:
                return writeTrans("04", accountNum, "000000", "00000000", accountName)
        else:
                return 0
    else: 
        return 0

def delete(list):
    # only in Agent mode
    # delete an existing account
    # take name + account number as textline
    # checks account is valid, save account num + name for Transaction Summary file
    #print"delete"
    accountNum = getAccountNum("delete") #checks format
    if (accountNum not in list) and (accountNum != 0):
            print "Error: account does not exist"
            return 0
    elif accountNum != 0:
        # check that accountNum is valid (exists)
        accountName = getName()
        if accountName != 0:
                list.remove(accountNum)
                return writeTrans("05", accountNum, "000000", "00000000", accountName)
        else:
                return 0
    else: 
        return 0

def withdraw(mode, list, w_Dict):
    # any mode (Agent, Retail)
    # ask for account number + amount to withdraw
    # convert to cents - withdraw from account
    # check account is valid and amount is valid
    #print"withdraw"
    fromAccount = getAccountNum("withdraw from")
    if (fromAccount not in list) and (fromAccount != 0):
            print "Error: account does not exist"
            return 0
    elif fromAccount != 0:
        amount = int(getAmount(mode))
        if amount != (-1):
            if mode == "retail":
                if (fromAccount not in w_Dict):
                    w_Dict[fromAccount] = amount
                elif (w_Dict[fromAccount] + amount) > 100000:
                    print "Error: maximum daily withdraw limit reached"
                    return 0
                else:
                    w_Dict[fromAccount] = w_Dict[fromAccount] + amount
            return writeTrans("02", "000000", fromAccount, str(amount), "               ")
        else:
                return 0
    else:
            return 0

def deposit(mode, list):
    # any mode (Agent, Retail)
    # ask for account num + amount
    # check valid
    # convert amount to cents - add to account
    #print"deposit"
    toAccount = getAccountNum("deposit to")
    if toAccount not in list:
            print "Error: account does not exist"
            return 0
    elif toAccount != 0:
        amount = getAmount(mode)
        if amount != (-1):
                return writeTrans("01", toAccount, "000000", amount, "               ")
        else:
                return 0
    else:
            return 0

def transfer(mode, list):
    # any mode (Agent, Retail)
    # ask fro from account number, to account number, and the amount
    # check valid
    # transfer!
    #print"transfer"
    toAccount = getAccountNum("transfer to")
    if (toAccount not in list) and (toAccount != 0):
            print "Error: account does not exist"
            return 0
    elif toAccount != 0:
        fromAccount = getAccountNum("transfer from")
        if (fromAccount not in list) and (fromAccount != 0):
                print "Error: account does not exist"
                return 0
        elif fromAccount != 0:
                amount = getAmount(mode)
                if amount != (-1):
                        return writeTrans("03", toAccount, fromAccount, amount, "               ")
                else:
                        return 0
        else:
                return 0
    else:
            return 0
    

def writeTrans(code, toAccount, fromAccount, amount, name):
    # writes the line that will go into the Transaction Summary file
    # used by all transactions
    # output is a string
    transaction = code + " " + toAccount + " " + fromAccount + " " + amount + " " + name
    return transaction

def main():
        # where the action happens

    while True:
        try:
                loginState = 0
                q = Queue.Queue()
                # store the information that will be processed at logout (as strings)
                # these strings will be added to Transaction Summary File at end of day
                # q is reset every day

                w_Dict = {}
                # stores daily withdraw value for accounts
                # rest every day

                command = raw_input("Please login:\n")
                command = command.strip() # removes whitespace
                #print command
                if command == "login":
                    loginState = 1
                while loginState == 1:
                    mode = raw_input("Please enter a mode:\n")
                    mode = mode.strip() # removes whitespace
                    if mode == "agent" or mode == "retail":
                        print "You are now in " + mode + " mode!"
                        accounts = open("validAccounts.txt",'r')
                        accountsList = accounts.read().splitlines()
                        while loginState == 1:
                            command = raw_input("Please enter a transaction:\n")
                            command = command.strip()
                            if mode == "agent" and command == "create":
                                        trans = create(accountsList)
                                        if trans != 0:
                                                q.put(trans)
                            elif mode == "agent" and command == "delete":
                                        trans = delete(accountsList)
                                        if trans != 0:
                                                q.put(trans)
                            elif command == "deposit":
                                trans = deposit(mode, accountsList)
                                if trans != 0:
                                        q.put(trans)
                            elif command == "withdraw":
                                trans = withdraw(mode, accountsList, w_Dict)
                                if trans != 0:
                                        q.put(trans)
                            elif command == "transfer":
                                trans = transfer(mode, accountsList)
                                if trans != 0:
                                        q.put(trans)
                            elif command == "logout":
                                trans =writeTrans("00", "000000", "000000", "00000000", "               ")
                                q.put(trans)
                                loginState = 0
                                print "Logout successful!"
                            else:
                                print "Error: invalid command"
                    else:
                        print "Error: invalid mode"
                    if q.empty():
                        loginState = 0
                    else:
                        transactionFile = open("transactionSummary.txt",'w')
                        while not q.empty(): # while q is not empty
                                trans = q.get()
                                # print trans
                                transactionFile.write(trans + "\n") # TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
                                #print trans
                                # write trans to Transaction Summary File
                        loginState = 0
                        transactionFile.close()
                        transactionFile = open("transactionSummary.txt",'r')
                        merged = open("mergedTransactions.txt", 'a')
                        merged.write(transactionFile.read())
                        merged.close()
        except (EOFError):
                break # end of file reached

# calling the main function
main()
        

        
    


