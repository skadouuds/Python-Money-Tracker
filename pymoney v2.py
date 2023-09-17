import os.path

flags = False
filename = "records.txt"

class Record:
    """Represent a record."""
    def __init__(self, cat, item, money):
        self._cat = cat
        self._item = item
        self._money = money

    @property
    def money(self):
        return self._money
    
    @property
    def cat(self):
        return self._cat
    
    @property
    def item(self):
        return self._item
    
    """
    Define getter methods for each attribute with @property decorator.
    """

class categories:
    def __init__(self):
        self.categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', [
            'bus', 'railway']], 'income', ['salary', 'bonus']] 
        """
        Categories are stored in a nested list.
        """
        
    def view(self, categories, space=0):
        """
        Function to view the list of the categories available.
        """
        for chosen in categories:
            if type(chosen) != list:
                print(" " * space + " - " + chosen)
            else:
                space += 3
                self.view(chosen, space)

    #todo:ganti2
    """
    Validating the category input by the user.
    """
    def is_category_valid(self, category, categories, space=0):
        global flags
        for chosen in categories:
            if type(chosen) == list:
                self.is_category_valid(category, chosen, space+1)
            elif str(chosen) == str(category):
                global flags
                flags = True
        if space == 0 and flags == True:
            flags = False #resetin
            return True
        elif space == 0 and flags == False:
            return False
   
    def find_subcategories(self, category, categories):
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and  type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index+1], True)
            else:
                if categories == category or found :
                    yield categories

        gen = find_subcategories_gen(category,categories)   
        ans=[res for res in gen]
        return ans
            

class Records:

    def __init__(self): 

        """
        Using the same like the previous assignment.
        """      
        self.item_list = []
        if os.path.isfile(filename):
            print("Welcome back!")
            try:
                with open(filename, 'r') as file:
                    self.item_list = []
                    for i in file.readlines():
                        loys = i.split()
                        self.item_list.append((loys[0], loys[1], int(loys[2])))
    
            except: #Eof error
                print("File is corrupted!\nPlease remove the " + filename + " file!")
                self.item_list = []

                try:
                    dollar = int(input("How much money do you have? "))
                except ValueError:
                    print("You should input a number!")
                else:
                    self.item_list.append(("Initial_Bal", "Init", dollar))
                    print(self.item_list)
        else:
            self.item_list = []
            try:
                dollar = int(input("How much money do you have? "))
            except ValueError:
                print("You should input a number!")
            else:
                self.item_list.append(("Initial_Bal", "Init", dollar))

    def add(self, addMode, categories):
        try:
            cat, item, money = addMode.split()
            money = int(money)
            self.item_list.append((cat, item, money))

            if categories.is_category_valid(cat, categories.categories):
                pass
            else:
                print('The specified category is not in the category list.\n You can check the category list by command "view categories".\n Fail to add a record.')
                return
            pass

        except ValueError:
            print("Wrong Format!")
            print("The format of a record should be like this: 'meal breakfast -50'.")
            print("Failed to add a record.")
            return

        except UnboundLocalError:
            print("Wrong Format!")
            print("The format of a record should be like this: 'meal breakfast -50'.")
            print("Failed to add a record.")
            return

    def view(self):
        items = [item[2] for item in self.item_list]
        sum_dollar = sum(items)
        print("Category            Description         Amount\n================== ==================== ======\n")
        for index, row in enumerate(self.item_list[1:], start=1):

            formats = 21 - len(row[1])
            formatsSp = " " * formats
            formats1 = 18 - len(row[0])
            formatsSp1 = " " * formats1
            print(str(index) + " " + row[0] +formatsSp1+ row[1] + formatsSp + str(row[2]))
        print("\n==========================================")
        print("Now you have " + str(sum_dollar) + " dollars.\n")

    def delete(self,delPart):

        if delPart < len(self.item_list) :
            self.item_list.pop(delPart)
            return self.item_list
        elif delPart > 0:
            self.item_list.pop(delPart)
            return self.item_list
        else:
            print("Out of bounds records!")

    def save(self):
        result = []
        for i in self.item_list:
            result.append(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
        with open(filename, 'w') as file:
            file.writelines(result)

    def find(self,target, categories):
        
        self.insideCat = [item[0] for item in self.item_list]
        ans = list(filter(lambda it: True if it in categories.find_subcategories(target, categories.categories) else False, self.insideCat))
        items = [item[2] for item in self.item_list]
        sum_dollar = sum(items)
        print("Category            Description         Amount\n================== ==================== ======\n")
        for index, row in enumerate(self.item_list[1:], start=1):
            if row[0] in ans:
                formats = 21 - len(row[1])
                formatsSp = " " * formats
                formats1 = 18 - len(row[0])
                formatsSp1 = " " * formats1
                print(str(index) + " " + row[0] +formatsSp1+ row[1] + formatsSp + str(row[2]))
        print("\n===========================================")
        print("Now you have " + str(sum_dollar) + " dollars.\n")

    def reset(self):
        try:
            os.remove(filename)
            print("Resetting the records...")
            return
        except FileNotFoundError:
            print("There is no Records / File to reset in the directory!")

if __name__ == '__main__':

    categories = categories()
    records = Records()

    while(True):
        command = input("What do you want to do (add / view / delete / find / view categories / reset / exit )?")
        if command == "add":
            addMode = input(
                "Add an expense or income record with description and amount:\n")
            records.add(addMode, categories)

        elif command == "view":
            records.view()

        elif command == "delete":
            try:
                delPart = int(input("which line doe you want to delete?"))
            except ValueError:
                print("You should input a number!")
            else:
                records.delete(delPart)

        elif command == "view categories":
            categories.view(categories.categories)

        elif command == "find":
            target = input("Which category do you want to find?")
            records.find(target, categories)

        elif command == "reset": #reseting all the data in the records.txt 
            if not os.path.isfile(filename):
                print("There is no Records / File to reset in the directory!")
                continue
            else :
                records.reset()
                records.__init__()
                continue

        elif command == "exit":
            records.save()
            break
        else:
            print("Please check your command!")