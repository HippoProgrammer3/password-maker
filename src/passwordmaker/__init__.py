from pythonhash import php256

import csv, getpass

# Define custom error classes

class CSVReadError(Exception):
    pass

# Define user timeout list

timeoutDict = []

# Load the current hash table

# Define a dictionary to hold the hash data

hashDict = dict()

with open('hash.csv','r',newline='') as csvfile:
    hashReader = csv.reader(csvfile)
    for pair in hashReader: # iterate over the lines in the csv file
        if len(pair) == 2: # check if hash pair has two variablse
            hashDict[pair[0]] = pair[1] # set key:value pair with pair[0] and [1] respectively
        elif len(pair) > 2:
            raise CSVReadError('Hash pair has too many variables')
        elif len(pair) < 2:
            raise CSVReadError('Hash pair has too few variables')
        else:
            raise CSVReadError('Hash pair has broken the fundamentals of logic')

# Create the login screen and loop it
while True:
    print('HashWord Checker v0.0.1')
    while True:
        try:
            cmd = int(input('Login [1] / signup [2] / quit [3]? '))
            break
        except ValueError:
            print('Not a valid option - try again!')
    if cmd == 1:
        try:
            while True:
                username = input('Enter a username: ')
                if not (username in hashDict.keys()): # if username exists
                    print('Username does not exist - try again!')
                    continue
                elif username in timeoutDict:
                    print('Username is timed out - please reload to log in!')
                break
            timeoutCounter = 0
            while True:
                password = php256(getpass.getpass('Enter your password: '))
                # by this point we should have a working name and a password to check
                # verify from the local hash dictionary
                if password == hashDict[username]:
                    break
                else:
                    print('Password incorrect - try again!')
                    timeoutCounter += 1
                if timeoutCounter == 3:
                    timeoutDict.append(username)
                    print('Too many incorrect guesses - timing out user!')
                    break
            # either timed out or password correct
            if timeoutCounter < 3: # if not timed out
                print('Logged in!')
                # do logged in stuff
            else:
                pass
        except KeyboardInterrupt:
            print('Returning to menu...')
    elif cmd == 2:
        try:
            while True:
                username = input('Enter a username: ')
                if username in hashDict.keys(): # if username exists
                    print('Username already taken - try again!')
                    continue
                break
            password = php256(getpass.getpass('Enter a password: '))
            while True:
                if php256(getpass.getpass('Re-enter your password:')) == password:
                    break
                else: 
                    print('Passwords do not match - try again!')
            # by this point we should have a working username and password pair
            # add it to the local hash dictionary
            hashDict[username] = password
            print('New user added!')
        except KeyboardInterrupt:
            print('Going back to menu...')
    elif cmd == 3:
        break
    else:
        print('Not a valid option - try again!')

# Flush the updated password csv to disk

with open('hash.csv','w',newline='') as csvfile:
    hashWriter = csv.writer(csvfile)
    for hashPair in hashDict:
        hashWriter.writerow(hashPair)

# Print an exit message
print('Quitting...')