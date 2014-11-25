def mergeTransactions():
	#Merges the transaction summary file to the end of the mergedTransactions file
	transactionFile = open("transactionSummary.txt",'r')
	merged = open("mergedTransactions.txt", 'a') #append to mergedTransactions.txt
	merged.write(transactionFile.read())
	merged.close()
	transactionFile.close()

def pad(type, str):
        if type == "account":
                return str.zfill(6)
        elif type == "name":
                return str.ljust(15)
        elif type == "amount":
                return str.zfill(8)

def giveMoney(line, accounts):
	#adds money to an account
	#used by deposit and transfer
	account = line[3:9] #account from transaction line
	amount = int(line[17:25]) #amount from transaction line
	i = 0
	while i < len(accounts):
		#find line in master accounts file that matches account of transaction line
		if accounts[i][:6] == account:
			ind = i
			i = len(accounts) #used to break out of while loop
		else:
			i += 1
	balance = int(accounts[ind][7:15]) + amount #add amount to previous value of account 
	balance = pad("amount", str(balance)) #reformat amount to 8 characters
	accounts[ind] = accounts[ind][:7] + balance + accounts[ind][15:] #update line in master accounts list
	return accounts
	
def takeMoney(line, accounts):
	#takes money from an account
	#used by withdraw and transfer
	account = line[10:16] #account from transaction line
	amount = int(line[17:25]) #amount from transaction line
	i = 0
	while i < len(accounts):
		#find line in master accounts file that matches account of transaction line
		if accounts[i][:6] == account:
			ind = i
			i = len(accounts)
		else:
			i += 1
	balance = int(accounts[ind][7:15]) - amount #subtract amount from previous value of account
	#check balance is not less than 0 
	if balance >= 0:
		balance = pad("amount", str(balance)) #reformat balance to 8 characters
		accounts[ind] = accounts[ind][:7] + balance + accounts[ind][15:] #update line in master accounts list
	else:
		sys.exit("Failure: insufficient funds") #Error message if balance is less than 0
	return accounts

	
def updateAccounts():
	old = open("masterAccounts.txt","r")
	accounts = old.read().splitlines() #put all account numbers, balances, and names into a list
	old.close()
	transaction = open("mergedTransactions.txt","r")
	transList = transaction.read().splitlines() #put all transaction lines into a list
	transaction.close()
	for line in transList: #process every transaction
		if line[:2] == "01":
			#deposit
			accounts = giveMoney(line, accounts)
		elif line[:2] == "02":
			#withdraw
			accounts = takeMoney(line, accounts)
		elif line[:2] == "03":
			#transfer
			accounts = takeMoney(line, accounts)
			accounts = giveMoney(line, accounts)
		elif line[:2] == "04":
			#create
			accounts.append(getAccount(line))
		elif line[:2] == "05":
			#delete
			account = getAccount(line)
			for a in accounts:
				if a[:6] == account[:6]:
					if a[7:15] == "00000000":
						accounts.remove(a)
					else:
						sys.exit("Failure: account balance not zero")
	accounts.sort() #sorts accounts list in ascending order by account number
	new = open("masterAccounts.txt","w")
	valid = open("validAccounts.txt","w")
	for line in accounts:
		new.write(line + "\n") #write account line to masterAccounts.txt
		valid.write(line[:6] + "\n") #take first 6 characters (account number) and write to validAccounts.txt
	new.close()
	valid.write("000000") #add 000000 to end of valid accounts file
	valid.close
	
def getAccount(line):
	#returns account number, balance, and name
	#used by create and delete transactions
	account = line[3:9] + " " + line[17:]
	return account
		
updateAccounts()
	
	