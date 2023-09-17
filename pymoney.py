import os.path
import sys

filename = "records.txt"

def initialize(): #Initialize the file
    if os.path.isfile(filename): #Check if the file exists
        print("Welcome back!")
        try:
            with open(filename, 'r') as myfile:
                recordsList = [] #empty list
                data = myfile.readlines() #read all lines
                for i in data: #read each line
                    temp = i.split(" ",1)
                    price = int(temp[1])
                    things = temp[0]
                    recordsList.append((things,price)) #append tuple ke list
                
                initialmoney = recordsList[1][1] #Call The tuple inside list

            myfile.close()
            return initialmoney,recordsList
            
        except: #If theres no data inside
            print("Invalid format in records.txt. Deleting the contents.")
            recordsList = []
            while(True):
                try:
                    balance = int(input("How much money do you have? "))
                except ValueError:
                    print("The input isn't valid!")
                else:
                    recordsList.append(("CurrentBal", balance))
                    recordsList.append(("InitialBal", balance))
                    initialmoney = recordsList[1][1]
                    return initialmoney,recordsList
    else:
        recordsList = []
        while(True):
            try:
                balance = int(input("How much money do you have? "))

            except ValueError:
                print("You should input a interger!")
            else:
                recordsList.append(("CurrentBal", balance))
                recordsList.append(("InitialBal", balance))
                initialmoney = recordsList[1][1]
                return initialmoney,recordsList

def add(recordsList):
    addMode = input(
        "Add an expense or income record with description and amount:\n")
    try:
        item, money = addMode.split(" ", 1) #initialize the item and money when entering the add mode
        money = int(money)
        recordsList.append((item, money)) #add tuple inside list
    except ValueError:
        print("Wrong Format!")
        print("The format of a record should be like this: 'breakfast -50'.")
        print("Failed to add a record.")
        return recordsList
    except UnboundLocalError:
        print("Wrong Format!")
        return recordsList
    
    return recordsList

def view(recordsList): #View the records
    print("Description                    Amount\n============================    =======\n")
    items =[item[1] for item in recordsList[1:]]
    totalMoney = sum(items) #Total current money
    index = 1
    for idx, val in recordsList[2:]:
        length=30-len(idx)
        formats=" "*length
        space =" "
        print(index,space,idx,formats,val, sep="")
        index += 1
    print("\n=======================================")
    print("You now have", totalMoney, "balances.")
    
def delete(recordsList):
    try:
        if (len(recordsList) == 2) :
            print("There is no record to delete!")
        else :
            delPart = int(input("Which Record do you want to delete? "))
            if(delPart > len(recordsList)-2) :
                print("Out of bounds records!")
            elif(delPart <= 0) :
                print("Out of bounds records!")
            else :
                recordsList.pop(delPart+1)

    except IndexError:
        print("There is no record with index", delPart, ". Failed to delete a record!")        
    except:
        print("Invalid format. Fail to delete a record.")

    return recordsList

def save(initialmoney,recordsList):
    result = []
    items =[item[1] for item in recordsList[1:]]
    totalMoney = sum(items) #Total current money
    result.append(str(recordsList[0][0]) + " " + str(totalMoney) + "\n")
    for lou in recordsList[1:]:
        result.append(str(lou[0]) + " " + str(lou[1]) + " " + str(lou[2])+ "\n") #append the list to the result

    with open(filename, 'w') as file:
        file.writelines(result)
    file.close()

if __name__ == '__main__':
    initialmoney,recordsList = initialize()
    while(True):
        command = input("What do you want to do (add / view / delete / reset / exit)? ")
        if command == "add":
            recordsList = add(recordsList)

        elif command == "view":
            view(recordsList)

        elif command == "delete":
            recordsList = delete(recordsList)

        elif command == "reset" : #Reset the records
            try:
                os.remove(filename)
                print("Resetting the records...")
                initialmoney,recordsList = initialize()
            except FileNotFoundError:
                print("There is no Records / File to reset in the directory!")

        elif command == "exit":
            save(initialmoney,recordsList)
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')