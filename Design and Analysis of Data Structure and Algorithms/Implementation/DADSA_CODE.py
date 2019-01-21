'''
Program Description:
     ---> A well-known Art colletor who possesses mythical wealth has thousands of art objects stored 
         in 4 Warehouses. Each warehouse has an insurance of 2 billion pushing the overall insurance
         across all 4 to 8 billion.
         This program will assist the Art collector in managing the objects across all 4 Warehouses.

Main functionalities:
     --->  Add an item to warehouse")
     --->  Display Warehouse Items")
     --->  Move Items")
     --->  Remove Items")
     --->  Restore Discarded Items")
     --->  Search an Item")

User interface Variables:
     --->  OUT(Return Values):
           bool: Success indicator(False:Failure,True:Success)
     --->  IN(Value parameters):
           Uses value Parameter()
     ---> IN AND OUT(Reference Parameters):
           Uses reference parameters()
 
History[Date:         Author:   Description:]
        21/11/2018    16015212  DADSA

'''

#Python modules
import csv
import os
import pickle
import copy

#global variable
redistribute_items =False

'''
class Warehouse(object):
  ---> Record Data-type Declaration
  ---> Contains a contructor which assigns values to instance variables 
         Constructor fields:
          - Warehouse name
          - Remaining Insurance

  ---> Methods:
       - increase_warehouse_insurance()
       - decrease_warehouse_insurance()
       - get_warehouse_name()
       - get_warehouse_remaining_insurance(self)
       - def __str__(self)
       - def __repr__(self)
'''
class Warehouse(object):

    overall_insurance =8000000000

    #default constructor
    def __init__(self,warehouse_name=None,remaining_insurance=None):
        self.warehouse_name = warehouse_name
        self.remaining_insurance = remaining_insurance
        self.warehouse_contents =[]

    def increase_warehouse_insurance(self,amount):
        self.remaining_insurance+=amount
        Warehouse.overall_insurance+=amount
    
    def decrease_warehouse_insurance(self,amount):
        self.remaining_insurance-=amount
        Warehouse.overall_insurance-=amount
    
    def get_warehouse_name(self):
        return self.warehouse_name

    def get_warehouse_remaining_insurance(self):
        return self.remaining_insurance

    #converts object to string
    def __str__(self):
         return "%s %s"%(self.warehouse_name,self.remaining_insurance)

    #converts object to string debug
    def __repr__(self):
         return "%s %s"%(self.warehouse_name, self.remaining_insurance)

'''
class Item(object):
  ---> Record Data-type Declaration
  ---> Contains a contructor which assigns values to instance variables 
         Constructor fields:
          - Item Number
          - Item Description
          - Item Price

  ---> Methods:
       - def __str__(self)
       - def __repr__(self)
'''
class Item():

    #default constructor
    def __init__(self,item_number=None,item_description=None,item_price=None ):

        self.item_number = item_number
        self.item_description =item_description
        self.item_price = item_price
 
    #converts object to string
    def __str__(self):
        return "%-11s  %-45s £%s"%(self.item_number,self.item_description,self.item_price)
    
    #converts object to string debug
    def __repr__(self):
        return "%-11s  %-45s %s"%(self.item_number,self.item_description,self.item_price)
'''
Function Name: 
  --> save_records_to_file()

Function Description:
  --> Iterates over the list of 4 warehouse objects and write the contents
      which consists of multiple Class Items instance, into binary file.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      Allwarehouses list
      Warehouse.overall_insurance
'''
def save_records_to_file():

   with open('DADSA','wb') as filestream: #open binary file
       #iterate over all warehouses and save contents to file
        for i in range(0,len(allwarehouses )):
           pickle.dump(allwarehouses[i].warehouse_contents,filestream)
           pickle.dump(allwarehouses[i].remaining_insurance,filestream)
        pickle.dump(discarded_items.warehouse_contents,filestream)
        pickle.dump(Warehouse.overall_insurance,filestream)
       
   return

'''
Function Name: 
  --> read_file()

Function Description:
  --> Checks if the file the user is opening exists,
       - if exists then open the file and load it into the program
       - if the file doesnt exit throw FileNotFound exception 

User Interface Variables:
  --> OUT(Return Values):
      - saved_items_read
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      Allwarehouses list
      Warehouse.overall_insurance
'''
def read_file():

    #local variable
    saved_items_read=0
    try: 
      with open('DADSA','rb') as filestream:#read binary file
         #iterates and read data back to the program
         for i in range(0,len(allwarehouses)):
            allwarehouses[i].warehouse_contents = pickle.load(filestream)
            allwarehouses[i].remaining_insurance =pickle.load(filestream)
         discarded_items.warehouse_contents = pickle.load(filestream)
         Warehouse.overall_insurance = pickle.load(filestream)
      saved_items_read+=1
    
    #throws filenotfound error if file non existent
    except FileNotFoundError:
       print(FileNotFoundError)
       
    return saved_items_read

'''
Function Name: 
  --> read_csvs_to_warehouse_object()

Function Description:
  --> Gets csv file name and assign it to a warehouse.
      It will then call the function load_csvs() which
      loads the csvs to appropriate warehouse.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - Warehouse 1 object
      - Warehouse 2 object
      - Warehouse 3 object
      - Warehouse 4 object
'''
def read_csvs_to_warehouse_object():

     load_csvs("DADSA Assignment 2018-19 Warehouse A.csv",w1)
     load_csvs("DADSA Assignment 2018-19 Warehouse B.csv",w2)
     load_csvs("DADSA Assignment 2018-19 Warehouse C.csv",w3)
     load_csvs("DADSA Assignment 2018-19 Warehouse D.csv",w4)

'''
Function Name: 
  --> load_csvs(csv_name,warehouse)

Function Description:
  --> Opens the csv in the correct path and load data into appropriate warehouse.
  --> Skips first row of csv as contains the title: item number,description,price.
  --> Saves csv rows into variables,validates them and save them into instance of 
      class Item using constructor.
  --> Append class instance to selected warehouse list.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - csv name
  --> IN and OUT (Reference Parameters):
      - warehouse object
'''
def load_csvs(csv_name,warehouse):
    
      #local variables
      discarded_item=0
      junk_items =[]

      try:
          #opens csv file and read data using variable reader
          with open(csv_name) as csv_file:
                  reader = csv.reader(csv_file)
                  next(reader,None) #skips header of csv
                  for itemnumber,itemdescription,itemprice in reader:
                      item_not_rejected = [True]
                      #validate csv data and return false if price is over warehouse insurance
                      itemnumber = remove_special_characters_from_numbers(itemnumber)
                      itemprice = get_correct_price(warehouse,itemprice,item_not_rejected)
                      m = Item(itemnumber,itemdescription,itemprice)
                      #append rejected item to discarded list if false otherwise append to warehouse list
                      if item_not_rejected[0] == False:
                          junk_items.append(m)
                          discarded_items.warehouse_contents.append(m)
                          discarded_item+=1
                      else:    
                         warehouse.warehouse_contents.append(m)
                         warehouse.decrease_warehouse_insurance(itemprice)

      except FileNotFoundError:#throws error if csv file not found
          print(FileNotFoundError)
      #displays discarded items to user
      if discarded_item > 0:
         print("\nThe following items were not added to %s"%warehouse.warehouse_name)   
         print_records(junk_items)
         input("Press any key to continue")
  
      return

'''
Function Name: 
  --> main()

Function Description:
  --> First function to be called when program is executed.
  --> Contains global instances of Warehouse class which will then be manipulated
      during the execution of program.
  --> Checks and read file into program if exist.
  --> Displays menu of the program.
  --> Returns None and exit program if user choice is exit.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def main():

    #local variables
     saved_items_read =0
     menuchoice = 0

     #global variables
     global w1
     global w2
     global w3
     global w4
     global allwarehouses
     global discarded_items

     #Warehouse class instances
     w1 = Warehouse("A",2000000000)
     w2 = Warehouse("B",2000000000)
     w3 = Warehouse("C",2000000000)
     w4 = Warehouse("D",2000000000)
     discarded_items = Warehouse("Discarded",0)

     #copy all warehouses instance into a list
     allwarehouses = copy_all_warehouse_objects()
     #checks if theres file to be loaded
     saved_items_read = read_file()
     
     if saved_items_read <=0:
        read_csvs_to_warehouse_object()#reads csv file into warehouse if saved_items_read<=0

     #clear screen and display menu until user choice is 7
     while(menuchoice!=7):
      os.system('cls')
      menu()
      print("\n --->  Input your choice(1-7): ")
      menuchoice =get_correct_integer_input(1,7)
      make_menu_choice(menuchoice)

'''
Function Name: 
  --> menu()

Function Description:
  --> Displays main menu of the system

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def menu():
    print("\n\n                                     MAIN MENU                    ")
    print("                                     ---------")
    print("   1.  --->  Add an item to Warehouse")
    print("   2.  --->  Display Warehouse items")
    print("   3.  --->  Move Warehouse Items")
    print("   4.  --->  Remove warehouse Items")
    print("   5.  --->  Restore Discarded Items")
    print("   6.  --->  Search an Item")
    print("   7.  --->  EXIT PROGRAM")

'''
Function Name: 
  --> make_menu_choice(menu_choice)

Function Description:
  --> Receives user input from main and executes function based on user choice.
  --> Saves any changes made by user into a binary file calling function save_records_to_file()
  
User Interface Variables:
  --> OUT(Return Values):
      - menu_choice
  --> IN(Value Parameters):
      - menu_choice
  --> IN and OUT (Reference Parameters):
      - None
'''
def make_menu_choice(menu_choice):

       #Action user-selected menu item
      if menu_choice==1:
         select_warehouse_to_add_records()
         save_records_to_file()#saves any changes to binary file
      elif menu_choice ==2:
         display_warehouse_contents()
      elif menu_choice== 3:
         move_warehouse_items()
         save_records_to_file()
      elif menu_choice ==4:
         remove_warehouse_items()
         save_records_to_file()
      elif menu_choice ==5:
         restore_discarded_items()
         save_records_to_file()
      elif menu_choice ==6:
          search_item()
      elif menu_choice ==7:
          print("\nQuitting program!!!!!")
          return 0  
      return menu_choice 

'''
Function Name: 
  --> select_warehouse()

Function Description:
  --> Displays warehouse selection to user
  
User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def select_warehouse():

      print("  1.  --->  A")
      print("  2.  --->  B")
      print("  3.  --->  C")
      print("  4.  --->  D")
      print("  5.  --->  EXIT")
  
      return

'''
Function Name: 
  --> select_warehouse_to_add_records()

Function Description:
  --> Allows user to add a new item to a warehouse
  --> Displays warehouse selection and prompts for input
  --> If user input matches a warehouse index in allwarehouses list,call add records function.
  --> If wrong input dislays wrong selection to user an repeat input.
  --> Returns to main menu if choice is 5
  --> Repeats select_warehouse_to_add_records() function if user input 'Y'.
  
User Interface Variables:
  --> OUT(Return Values):
      - choice if 5
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def select_warehouse_to_add_records():

    #local variables
    choice=0
    repeat_add_records='Y'
   
    #repeats action if repeat_add_records='Y' 
    while repeat_add_records=='Y':
        #clear screen, display warehouses info and selection
        os.system('cls')
        print("\n                         ADD ITEM TO WAREHOUSE MENU")
        print("                         --------------------------")
      
        warehouses_details(allwarehouses)
        select_warehouse()
        print("\n--->  Select a Warehouse(1-5): ")
        choice = get_correct_integer_input(1,5)
       
        os.system('cls')
        if choice ==5:
            return
        #iterates over the warehouses and if choice matches an index run add_records()
        
        add_records(allwarehouses[choice-1])
                   
        print(" ---> Would you like to add another record?(Y/N): ")
        repeat_add_records = get_valid_yes_or_no()

    return

'''
Function Name: 
  --> add_records(selected_warehouse)

Function Description:
  --> Prints warehouse information and ask user for details of new item to be added.
  --> Validates item number to avoid duplicates.
  --> Checks if the warehouse insurance can cover the item price:
      - Discards item if insufficient warehouse insurance.
      - Request item description and add item to warehouse if sufficient warehouse insurance.
      - Decrease warehouse remaining insurance.
  
User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - selected_warehouse
'''
def add_records(selected_warehouse):

    #local variables
    allwarehouses_contents=[]
    item_not_discarded =[True]
    #Item class instance
    s = Item()
    #copies all 4 warehouses contents to check item number exist
    allwarehouses_contents = copy_all_warehouses_contents()

    printwarehouseinfo(selected_warehouse)

    #user input fields
    print("\n  ---> Input item number: (0-99999): ")
    s.item_number= check_id_existence(allwarehouses_contents,True)
    print("\n  ---> Input item price: (1-2000000000): ")
    s.item_price = get_correct_integer_input(1,2000000000)
    s.item_price = get_correct_price(selected_warehouse,s.item_price,item_not_discarded)
    
    #accepts and request item description if item not discarded
    if item_not_discarded[0]==True:
       s.item_description = get_valid_item_description()
       selected_warehouse.warehouse_contents.append(s)
       selected_warehouse.decrease_warehouse_insurance(s.item_price)
       printwarehouseinfo(selected_warehouse)
       print("\nItem successfully added!!!")
       
    return

'''
Function Name: 
  --> select_warehouse_to_add_records()

Function Description:
  --> Displays a warehouse based on user input.
  --> Displays warehouse name, remaining insurance and warehouse contents.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def display_warehouse_contents():

    choice =0
    repeat ='Y'
    
    while repeat=='Y':

        #clear screen, display warehouses info and selection
        os.system('cls')
        print("         VIEW WAREHOUSE         ")
        print("        ---------------         ")
        warehouses_details(allwarehouses)
        select_warehouse()

        print("\n--->  Select a Warehouse to view(1-5): ")
        choice = get_correct_integer_input(1,5)#prompts and validate user input
        if choice ==5:
            return
        else:
            if len(allwarehouses[choice-1].warehouse_contents)==0:
                print("\n ---> Warehouse empty,there are no items to be displayed")
            else:    
                printwarehouseinfo(allwarehouses[choice-1])#displays selected warehouse
                    
        print("\nDisplay another warehouse?(Y/N): ")
        repeat =get_valid_yes_or_no()

    return

'''
Function Name: 
  --> move_warehouse_items()

Function Description:
  --> Moves items from a selected warehouse to a destination warehouse.
  --> Set restore items and to false move items flag to True
  --> Display all warehouses info and prompts user for a choice.
  --> If correct input is provided will then call pick_items function.
  --> If input is 5 then returns to main menu

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def move_warehouse_items():

    restore_items = False
    move_items = True
    repeat = 'Y'
    while repeat=='Y':
        #clear screen, display warehouses info and selection
        os.system('cls')
        print("                   MOVE ITEMS MENU")
        print("                   ---------------")
        warehouses_details(allwarehouses)
        select_warehouse()

        print(" \n ---> Select a warehouse to choose item/s from(1-5): ")
        choice = get_correct_integer_input(1,5)#prompts and validate user input
        if choice==5:return
        if len(allwarehouses[choice-1].warehouse_contents)==0:
            print("\n ---> Warehouse empty, there are no items to be moved")
        else:      
            pick_items(choice,move_items,restore_items)#function which allows user to pick warehouse items
        print(" ---> Move more items?(Y/N): ")
        repeat = get_valid_yes_or_no()


'''
Function Name: 
  --> remove_warehouse_items()

Function Description:
  --> Removes items from a selected warehouse.
  --> Set restore items and move items flag to false
  --> Display all warehouses info and prompts user for a choice.
  --> If correct input is provided will then call pick_items function.
  --> If input is 5 then returns to main menu

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def remove_warehouse_items():

    restore_items = False
    move_items = False
    repeat = 'Y'
    while repeat=='Y':
        #clear screen, display warehouses info and selection
        os.system('cls')
        print("                   REMOVE ITEMS MENU")
        print("                   ---------------")
        warehouses_details(allwarehouses)
        select_warehouse()

        print(" \n ---> Select a warehouse to choose item/s from(1-5): ")
        choice = get_correct_integer_input(1,5)#function which allows user to pick warehouse items
        if choice==5:return
        if len(allwarehouses[choice-1].warehouse_contents)==0:
            print("\n ---> Warehouse empty, there are no items to be removed")
        else:    
            pick_items(choice,restore_items, move_items)#function which allows user to pick warehouse items
        print(" ---> Remove more items?(Y/N): ")
        repeat = get_valid_yes_or_no()

'''
Function Name: 
  --> search_item()

Function Description:
  --> Prompts user to search for an item across all 4 warehouses
  --> Display item and warehouse position if found.
  --> Display item not found if item non-existent and reduce attemps by 1

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def search_item():

    #makes attempts variable static
    search_item.attemps = getattr(search_item,'attemps',3)
    again ='Y'
    while again=='Y' and search_item.attemps >0:
      
        os.system('cls')
        print("\n\n                   SEARCH AN ITEM MENU")
        print("                   -------------------")

        flag = True
        allwarehouses_contents = copy_all_warehouses_contents()#copy all warehouses contents
        print("\n\n--->  Attemps: %s"%(search_item.attemps))
        print("--->  Input item id: (%s-%s)"%(allwarehouses_contents[0].item_number,allwarehouses_contents[-1].item_number))
        #validate user input
        id = get_correct_integer_input(allwarehouses_contents[0].item_number,allwarehouses_contents[-1].item_number)
        #iterate across all 4 warehouses
        for i in range(0,len(allwarehouses)):
            temp=[]
            #sort currently searched warehouse  
            #return item index, and print item at warehouse position
            allwarehouses[i].warehouse_contents = mergeSort(allwarehouses[i].warehouse_contents)
            index = interpolation_search(allwarehouses[i].warehouse_contents,id)
            if index is not False:
                print("\nWAREHOUSE POSITION : %s"%(allwarehouses[i].warehouse_name))
                print("------------------   -")
                temp.append(allwarehouses[i].warehouse_contents[index])
                print_records(temp)
                flag =False
                break

        if flag ==True:#print item not found if flag unchanged and reduce attempts
            print("\nItem not found !!!")
            search_item.attemps-=1
        print("\nWould you like to search again?(Y/N): ")
        again = get_valid_yes_or_no()
        #resets static variable
    if search_item.attemps==0:
       search_item.attemps =3
    return

'''
Function Name: 
  --> pick_items(selected_warehouse,move_items,restore_items)

Function Description:
  --> User selects items to move to other warehouses
      with the function, select_items.
  --> Prompt user to select a destination warehouse if move_items is true
      - Append items to selected warehouse and view changes afterwards.
      - Returns item to selected warehouse if destination warehouse has insufficient
        warehouse insurance.

  --> Appends selected items to discarded items warehouse if move_items is false.
      -Delete picked items afterwards.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - selected_warehouse,move_items,restore_items
  --> IN and OUT (Reference Parameters):
      - None
'''
def pick_items(selected_warehouse,move_items,restore_items):

    #local variable
     picked_items =[]

     #checks if restore_items flag is false 
     if restore_items==False:
         #iterates over all warehouses and select the appropriate base on user input
                    picked_items = select_items(allwarehouses[selected_warehouse-1],False)
                    
     else:
         picked_items = select_items(discarded_items,True)
     if move_items==True:
          #clear screen and display warehouses info
          os.system('cls')
          print("\nALREADY SELECETED ITEMS : ")
          print("-------------------------")
          print_records(picked_items)#display list of picked items
          print("\n")
          warehouses_details(allwarehouses)
          select_warehouse()
          print("\n---> Select destination warehouse: ")
          destination = get_correct_integer_input(1,5)#validates user destination input

          while destination == selected_warehouse:
                print("You cannot move items to the same warehouse,select another warehouse(1-5): ")
                destination = get_correct_integer_input(1,5)
          select_destination_warehouse(destination,selected_warehouse,picked_items,restore_items)
          if restore_items==False:
            if destination ==5:
                print("\nNo changes were made as you quitted!!!")
            else:
                view_changes(selected_warehouse,False)
                print("\nItems successfully moved from selected warehouse!!!")
                input("Press any key to continue")
                view_changes(destination,False)
                print("\nItems successfully moved to destination warehouse!!!")
     else:
          #add selected items to discarded warehouse and delete them
          discarded_items.warehouse_contents.extend(picked_items)
          del picked_items[:]
          if restore_items==False:
            view_changes(selected_warehouse,False)
          print("\n ---> Item/s successfully deleted") 
     input("Press any key to continue")

'''
Function Name: 
  --> select_items(selected_warehouse,restore_items)

Function Description:
  --> This function allows the user to select warehouse items to be moved or deleted
  --> It first sorts the items by price in ascending order and prompts user to select 
      the desired items by item number.
  --> It then increases the selected warehouse insurance by the price of the selected item 
      if restore items flag is false

User Interface Variables:
  --> OUT(Return Values):
      - selected items list
  --> IN(Value Parameters):
      - selected_warehouse,restore_items
  --> IN and OUT (Reference Parameters):
      - selected_warehouse
'''
def select_items(selected_warehouse,restore_items):

    #local variables
    repeat ='Y'
    selected_items = []
    index_of_selected_item=0
    descending_order = False

    while repeat=='Y' and len(selected_warehouse.warehouse_contents)>0:
 
        os.system('cls')
        #sort warehouse contents by price in ascending order
        selected_warehouse.warehouse_contents = insertion_sort(selected_warehouse.warehouse_contents,descending_order)
        print("\nWAREHOUSE ITEMS: ")
        print("-----------------")
        print_records(selected_warehouse.warehouse_contents)

       
        print("\nALREADY SELECETED ITEMS : ")
        print("-------------------------")
        print_records(selected_items)

        #display warehouse info
        print("\nWAREHOUSE INFORMATION: ")
        print("----------------------")
        print("  ---> Warehouse Name : %s"%selected_warehouse.warehouse_name )
        print("  ---> Total elements : %s"%len(selected_warehouse.warehouse_contents))
        print("  ---> Remaining Insurance: £%s"%(selected_warehouse.remaining_insurance))
        print("\n")

        print(" ---> Select items by (item number): ")
    
        #sorts warehouse contents by id
        selected_warehouse.warehouse_contents = mergeSort(selected_warehouse.warehouse_contents)
        #prompts user to input item id and check if exists
        item_id = check_id_existence(selected_warehouse.warehouse_contents,False)
        #get index of selected item 
        index_of_selected_item = [i.item_number for i in selected_warehouse.warehouse_contents].index(item_id)
        #add item to selected items list 
        selected_items.append(selected_warehouse.warehouse_contents[index_of_selected_item])
        del selected_warehouse.warehouse_contents[index_of_selected_item]
        #increase warehouse insurance by value of selected item
        selected_items_worth = selected_items[-1].item_price
        if restore_items==False:
            selected_warehouse.increase_warehouse_insurance(selected_items_worth)
        os.system('cls')
        print("\nWAREHOUSE ITEMS: ")
        print("-----------------")
        print_records(selected_warehouse.warehouse_contents)
        print("\nALREADY SELECETED ITEMS : ")
        print("-------------------------")
        print_records(selected_items)
        print("\n---> Select more items?(Y/N): ")
        repeat = get_valid_yes_or_no()
     
    return selected_items


'''
Function Name: 
  --> warehouses_details(whouse)

Function Description:
  --> This function displays the details of all 4 warehouses.
  --> Details include:
      - Warehouse name
      - Total elements in warehouse
      - Remaining insurance

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - selected_warehouse
  --> IN and OUT (Reference Parameters):
      - None
'''
def warehouses_details(whouse):

        print("\nWAREHOUSES INFORMATION: ")
        print("----------------------")
        print("\nWarehouse Name       Total Elements    Remaing Insurance")
        print("--------------       -------------     -----------------")
        #iterate over all warehouses and print name,number of items and insurance
        for i in range(0,len(whouse)):
            print("%-20s %-17s %s"%(whouse[i].warehouse_name,len(whouse[i].warehouse_contents),whouse[i].remaining_insurance))
        print("\n")

'''
Function Name: 
  --> restore_discarded_items()

Function Description:
  --> This function displays all the items discarded by user or by the program itself
  --> Displays theres no item to be restored if warehouse is empty.
  --> Allow user to select items and restore them by call pick_items function.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def restore_discarded_items():

    repeat = 'Y'
    print("RESTORE DISCARDED ITEMS MENU")
    print("----------------------------")
    #checks if theres any discarded items
    if len(discarded_items.warehouse_contents)==0:
        print("\nThere is no item to be restored")
        input("Press any key to continue")
    else:
        #pick items and display final changes to user
       while repeat=='Y' and len(discarded_items.warehouse_contents) >0 :
           pick_items(discarded_items,True,True)
           view_changes(0,True)
           print("Item moved!!!")
           print("Move more items?(Y/N): ")
           repeat = get_valid_yes_or_no()
    return


'''
Function Name: 
  --> select_destination_warehouse(destination_warehouse,selected_warehouse,picked_items,restore_items)

Function Description:
  --> This function appends the selected items to the destination warehouse.
  --> It first calculates the worth of selected items,checks if the destination warehouse
      insurance is sufficient to accomodate items and appends items the warehouse if it has.
      -If insufficent warehouse insurance, returns selected items to selected warehouse.
      -If user quits returns items to selected warehouse.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - destination_warehouse,selected_warehouse,picked_items,restore items bool
  --> IN and OUT (Reference Parameters):
      - None
'''
def select_destination_warehouse(destination_warehouse,selected_warehouse,picked_items,restore_items):
    #calculates selected items worth
    selected_items_worth = calculate_picked_items_worth(picked_items)
    items_not_rejected=[True]
    
    
    #returns items to selected warehouse if user quits
    if destination_warehouse==5:
             return_items_to_warehouse(selected_warehouse,picked_items,selected_items_worth,restore_items) 
             if restore_items==False:
                view_changes(selected_warehouse,False)
             print("  --> Items successfully returned to the warehouse!!!")
    else:
        #iterates over all warehoues and selected appropriate warehouse
               #checks if warehouse has enough insurance
               get_correct_price(allwarehouses[destination_warehouse-1],selected_items_worth,items_not_rejected)
               if items_not_rejected[0]==True:
                   #adds items to destination warehouse and decrease insurance
                  allwarehouses[destination_warehouse-1].warehouse_contents.extend(picked_items)
                  allwarehouses[destination_warehouse-1].decrease_warehouse_insurance(selected_items_worth)
               else:
                   #return items to selected warehouse if insufficient insurance
                  return_items_to_warehouse(selected_warehouse,picked_items,selected_items_worth,restore_items)
                 
    return

'''
Function Name: 
  --> return_items_to_warehouse(selected_warehouse,picked_items,selected_items_worth,restore_items)

Function Description:
  --> This function appends picked items to selected warehouse if:
      - Destination warehouse has insufficent warehouse insurance.
      - If user quits returns items to selected warehouse.
      - If restore_items bool is true then returns items to discarded_items warehouse
  --> It then decreases the selected warehouse insurance by items worth

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - picked_items,restore items bool,selected_items_worth
  --> IN and OUT (Reference Parameters):
      - selected_warehouse
'''
def return_items_to_warehouse(selected_warehouse,picked_items,selected_items_worth,restore_items):
     os.system('cls')
     print("\n\nThis item/s will return to the original warehouse: \n")
     print_records(picked_items)
     flag = True

     if restore_items==False:
         
           #returns items to selected warehouse and decrease insurance
           allwarehouses[selected_warehouse-1].warehouse_contents.extend(picked_items)
           allwarehouses[selected_warehouse-1].decrease_warehouse_insurance(selected_items_worth)
           flag = False
                 
     #returns items to discared items warehouse if flag unchanged
     if flag ==True:
         discarded_items.warehouse_contents.extend(picked_items)
     return

'''
Function Name: 
  --> printwarehouseinfo(warehouse)

Function Description:
  --> This function prints warehouse info such as:
      - Warehouse Name
      - Total elements
      - Remaining insurance
      - Remaining insurance across the 4 warehouses
  --> It then prints all the items of the particular warehouse selected

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - selected warehouse
  --> IN and OUT (Reference Parameters):
      - None
'''
def printwarehouseinfo(warehouse):

    #clear screen and display warehouse info
    os.system('cls')
    print("\nWAREHOUSE INFORMATION: ")
    print("---------------------")
    print("  ---> Warehouse Name : %s"%warehouse.warehouse_name )
    print("  ---> Total elements : %s"%len(warehouse.warehouse_contents))
    print("  ---> Remaining Insurance: £%s"%(warehouse.remaining_insurance))
    print("  ---> Remaining Overall Warehouse Insurance: £%s"%(Warehouse.overall_insurance))
    #sorts warehouse items in ascending order and displays thems
    warehouse.warehouse_contents = insertion_sort(warehouse.warehouse_contents,False)
    print_records(warehouse.warehouse_contents)


'''
Function Name: 
  --> print_records(warehouse)

Function Description:
  --> This function prints details of a selected warehouse item such as:
      - Item number
      - Item description
      - Item price

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - selected warehouse
  --> IN and OUT (Reference Parameters):
      - None
'''
def print_records(warehouse):
    
    print("\nItem Number  Item Description \t\t\t\t   Item Price")
    print("-----------  ----------------   \t\t\t   -----------\n")
    for i in range(len(warehouse)):
        #iterate over warehouse items and prints them on screen
        print(warehouse[i])

'''
Function Name: 
  --> view_changes(selected_warehouse,restore_items)

Function Description:
  --> This function will display the new state of a selected warehouse
      after uses makes changes to it

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - selected warehouse,restore items bool
  --> IN and OUT (Reference Parameters):
      - None
'''
def view_changes(selected_warehouse,restore_items):

    if restore_items==True:
        printwarehouseinfo(discarded_items)
        
    else:
        printwarehouseinfo(allwarehouses[selected_warehouse-1])
                
    return

'''
Function Name: 
  --> calculate_picked_items_worth(picked_items)

Function Description:
  --> This function calculates the worth of the items picked by user
  --> It then returns the sum of picked items

User Interface Variables:
  --> OUT(Return Values):
      - sum
  --> IN(Value Parameters):
      - picked_items
  --> IN and OUT (Reference Parameters):
      - None
'''
def calculate_picked_items_worth(picked_items):
    sum=0
    #iterate over list of picked items and calculate the sum
    for i in picked_items:
        sum+=i.item_price
    return sum

'''
Function Name: 
  --> copy_all_warehouses_contents()

Function Description:
  --> This function copies the contents of all 4 warehouses into a single list.
  --> This list is then used to avoid duplicate item numbers.
  --> It then returns a list of all warehouses items.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - container list
'''
def copy_all_warehouses_contents():

      #copies all 4 warehouses cotents
      container = w1.warehouse_contents[:]
      container.extend(w2.warehouse_contents)
      container.extend(w3.warehouse_contents)
      container.extend(w4.warehouse_contents)
      #sort list by item number 
      container = mergeSort(container)
      return container 

'''
Function Name: 
  --> copy_all_warehouse_objects()

Function Description:
  --> This function copies all the instances of Warehouses class into one list.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - container list
'''
def copy_all_warehouse_objects():
    #local variable
    container =[]

    #copies all warehouses objects
    container.append(w1)
    container.append(w2)
    container.append(w3)
    container.append(w4)

    return container

'''
Function Name: 
  --> remove_special_characters_from_numbers(number)

Function Description:
  --> This function remove string characters from a number.
  --> It first store the user input into a list object.
  --> It checks if any string character is available and removes it.
  --> It then converts the list into a valid integer value and returns it.

User Interface Variables:
  --> OUT(Return Values):
      - valid_number
  --> IN(Value Parameters):
      - number(user input)
  --> IN and OUT (Reference Parameters):
      - None
'''
def remove_special_characters_from_numbers(number):
   
     #split user input into a list
     container =list(number)
     
     #iterate over list and remove special characters
     for i in container:
         if i.isdigit():
             pass
         else:
             container.remove(i)
     #converts list into integer and return
     valid_number =''.join(str(x)for x in container)
     valid_number = int(valid_number)
     return valid_number


'''
Function Name: 
  --> check_id_existence(warehouses_contents,add_records)

Function Description:
  --> This function checks if an item number exists already across all 4 warehouse
  --> If add_records is true:
      If an item number exists already, it willl prompt user to try a different value.
  --> If add record is false or item non existent then return id.

User Interface Variables:
  --> OUT(Return Values):
      - id
  --> IN(Value Parameters):
      - warehouse_contents,add_records bool
  --> IN and OUT (Reference Parameters):
      - None
'''
def check_id_existence(warehouses_contents,add_records):

    #local variables
    item_exist_already =True
    id =0

    #repeats while item already exist
    while item_exist_already==True:
        item_non_existent =[True]
        id = get_correct_integer_input(1,99999)#validate user input
        #checks for item id existence
        binary_search(warehouses_contents,0,len(warehouses_contents)-1,id,item_non_existent)
        
        #sets items_exist already flag to true and ask user to reinput item number
        if item_non_existent[0]==False:
            if add_records==False:
                item_exist_already = True
                print("Input item number: ")
            else:
                item_exist_already=False 
        else:
            #if add_records is true then display message and repeat otherwise return id
            if add_records==True:
              print("An item with the id '%d' exist,try again: "%(id))
              item_exist_already=True 
            if add_records==False:
              item_exist_already= False

    return id 


'''
Function Name: 
  --> binary_search(warehouse,start,end,value,item_non_existent)

Function Description:
  --> This function looks for item number by comparing it to the middle index value.
  --> If item number is greater than middle index value then set start index to midde index+1
      and recursively call the function
  --> If item number is less than middle index value then set last index value to middle index -1
      and recursively call the function
  --> If start index is greater than end index then set item_non_existent to False and return
  --> If item is found then print item.

User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - warehouse_contents,item_non_existent list,value
  --> IN and OUT (Reference Parameters):
      - start index,end index
'''
def binary_search(warehouse,start,end,value,item_non_existent):
    
    #repeat while end index is greater than start
    #end = lenght of warehouse contentes
    #start = 0
     if end>=start:
         #find middle value and convert to integer
         middle = start+(end-start)/2
         middle = int(middle)
         #displays found item
         if value==warehouse[middle].item_number:
            return
         else:
            #recursively call function with different start and end indexes
           if warehouse[middle].item_number>value:
                binary_search(warehouse,start,middle-1,value,item_non_existent)
           else : 
               binary_search(warehouse,middle+1,end,value,item_non_existent)
     else:
         #display item not found message
          print("An item with the id '%s' does not exits in the records..."%value)
          item_non_existent[0]=False
          return 

'''
Function Name: 
  --> interpolation_search(warehouse,id)

Function Description:
      It Calculates position to start searching by using the formula:
       position = int(start+(float((end-start)
      /(warehouse[end].item_number-warehouse[start].item_number))*(id-warehouse[start].item_number)))
  --> if item number at index position is == id, return position.
  --> if id is greater than item number at index position then set start index to position+1
      otherwise set end index to position+1.
  --> returns false if item not found.
     
User Interface Variables:
  --> OUT(Return Values):
      - item index postion,False if item not found
  --> IN(Value Parameters):
      - warehouse_contents,item id
  --> IN and OUT (Reference Parameters):
      - None
'''
def interpolation_search(warehouse,id):

    #calculates lenght of warehouse contents
    lenght= len(warehouse)
    #indexes
    start =0
    end = lenght-1
    #return false if warehouse contents is empty
    if end ==-1:
        return False
    
    #repeat while start index is less than end index and item number not found
    while ((start<end) <=id and (id >=warehouse[start].item_number)and (id <=warehouse[end].item_number)):
          try:
            position = int(start+(float((end-start)
           /(warehouse[end].item_number-warehouse[start].item_number))*(id-warehouse[start].item_number)))
          except ZeroDivisionError:#ignores error if only an item in warehouse contents
              return 0
          if warehouse[position].item_number ==id:#returns item position
              return position
          #reset start and end indexes 
          if id >warehouse[position].item_number:
              start = position+1 
          else:
               end = position-1
    return False


'''
Function Name: 
  -->  get_correct_integer_input(minimum,maximum)

Function Description:
  --> Prompts user to input a valid integer value.
  --> It then check the maximum and minimum values.
     
User Interface Variables:
  --> OUT(Return Values):
      - valid integer number
  --> IN(Value Parameters):
      - minimum value and maximum value
  --> IN and OUT (Reference Parameters):
      - None
'''
def get_correct_integer_input(minimum,maximum):

        #sets flag
        flag =True
        while flag == True:
             number= input("")
             #checks if input is valid integer
             try:
                if number.isdigit:
                   number = int(number)
             except ValueError:
                   print('You didnt input an input an integer,try again: (%d-%d))' % (minimum,maximum))
             else:
                 #checks if input is out of range
                 if number < minimum or number >maximum:
                    print('The entered number is out of range, try again: (%d-%d))' % (minimum,maximum))
                 else:
                    flag = False       
        return number

'''
Function Name: 
  -->  get_valid_yes_or_no()

Function Description:
  --> Prompts user to input a choice which is either Y or N
  --> Display error message if incorrect character is inputted
     
User Interface Variables:
  --> OUT(Return Values):
      - Y or N
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def get_valid_yes_or_no():

    flag =True
    #prompts user to input Y or N
    while flag:
        yes_or_no = input(" ")
        if yes_or_no.upper() == 'Y' or yes_or_no.upper() == 'N':
           return yes_or_no.upper()
        else:
          print("Wrong input,enter Y OR N: ")

'''
Function Name: 
  -->  get_correct_price(warehouse,itemprice,item_not_discarded)

Function Description:
  --> Validates item price and checks if it is out of range.
      - If item price is less than 1 and greater than 2 billion then rejects items and
        set item_not_discarded to false
      - If item price is greater than selected warehouse insurance then display algorithm
        option to user.
     
User Interface Variables:
  --> OUT(Return Values):
      - valid price
  --> IN(Value Parameters):
      - warehouse,itemprice
  --> IN and OUT (Reference Parameters):
      - item_not_discarded
'''
def get_correct_price(warehouse,itemprice,item_not_discarded):
 
    #local variables
    flag =True
    validprice =0

    while flag ==True:
        #validate item price
         try:
            validprice = int(itemprice)
         except ValueError:
            itemprice = remove_special_characters_from_numbers(itemprice)
            validprice = int(itemprice)
     
          #checks if item price out of range
         if validprice < 1 or validprice > 2000000000:
             if validprice < 1:
                 print("Item rejected, the item price is less than the minimum insurance £1")
             else:
                 print("Item rejected, the item price is greater than total warehouse insurance £2000000000")
             flag =False
             item_not_discarded[0]=False

         #checks if item price greater than warehouse remaining insurance
         elif validprice > warehouse.remaining_insurance :
              if validprice > Warehouse.overall_insurance:
                  print("Item rejected,")
                  print('The price is greater than overall remaining insurance "£%s"'%(Warehouse.overall_insurance))
                  print("Applying algorithm will discard some items to free space, proceed?(Y/N): ")
              else:
                  print("Item rejected,")
                  print('The price is greater than warehouse remaining insurance "£%s"'%(warehouse.remaining_insurance))
                  print("Apply algorithm to free up space?: (Y/N)")
              answer = get_valid_yes_or_no()

              if answer== "Y":
                  #algorithm to free space for new item
                 if algorithm(warehouse,validprice):
                     pass
                 else:
                    print("Item discarded")
                    flag =False
                    item_not_discarded[0]=False
              else:
                 print("Item discarded")
                 flag =False
                 item_not_discarded[0]=False
              input("Press any key to continue")
         else:    
             flag =False
    return validprice


'''
Function Name: 
  -->  algorithm(warehouse,itemprice)

Function Description:
  --> This function displays a list of items that could be moved for the new item to be accomodated.
  --> It sorts the warehouses in allwarehouses_objects list in ascending order
  --> Compares selected warehouse name to objects in allwarehouses_objects list and removes it.
  --> It then calls the function move_items_around_to_increase_insurance(warehouse,allwarehouses_objects,itemprice)
     
User Interface Variables:
  --> OUT(Return Values):
      - bool True or False
  --> IN(Value Parameters):
      - warehouse,itemprice
  --> IN and OUT (Reference Parameters):
      - None
'''
def algorithm(warehouse,itemprice):
    #display suggested items
    if suggest_moveable_items(warehouse,itemprice):

        #copy all warehouses objects and sort in ascending order
        allwarehouses_objects = copy_all_warehouse_objects()
        allwarehouses_objects = insertion_sort_objects(allwarehouses_objects,False)

        for i in range(0,len(allwarehouses)):
            #compares selected warehouse name and removes it from list
            if allwarehouses_objects[i].warehouse_name==warehouse.warehouse_name:
                allwarehouses_objects.remove(allwarehouses_objects[i])
                break
        move_items_to_increase_insurance(warehouse,allwarehouses_objects,itemprice)
        return True

    else:
        return False

'''
Function Name: 
  --> move_items_to_increase_insurance(current_warehouse,allwarehouses_objects,itemprice)

Function Description:
  --> This functions checks if there's space across the warehouses for an item of the selected item to be accomodated.
  --> It recursively call itself while item price is greater than the selected warehouse insurance.
  --> If there's no space across all the remaining warehouses then make a backup of their items,
      empty them and reset remaining insurance to 2billion.
  --> It then redistribute the backup items along with selected warehouse items until there's enought insurance
      to cover new item's price.
  
User Interface Variables:
  --> OUT(Return Values):
      - valid price
  --> IN(Value Parameters):
      - warehouse,itemprice
  --> IN and OUT (Reference Parameters):
      - item_not_discarded
'''    
def move_items_to_increase_insurance(current_warehouse,allwarehouses_objects,itemprice):

    #local variables
    flag =False
    backup_of_items=[]
    #static variable redistribute items
    move_items_to_increase_insurance.redistribute_items= getattr(move_items_to_increase_insurance,'redistribute_items',False)
  
    while itemprice > current_warehouse.remaining_insurance and move_items_to_increase_insurance.redistribute_items==False:

        for i in range(0,len(allwarehouses_objects)):
            #append selected warehouse item to warehouse with more insurance remaining
            if allwarehouses_objects[i].remaining_insurance > current_warehouse.warehouse_contents[0].item_price:
                move_item_to_warehouse(allwarehouses_objects[i],current_warehouse)
                move_items_to_increase_insurance(current_warehouse,allwarehouses_objects,itemprice)
                flag = True
            if current_warehouse.remaining_insurance >= itemprice:
               break
               
        if flag==False:  
            #sort warehouses in descending order
            allwarehouses_objects = insertion_sort_objects(allwarehouses_objects,True)
            for i in range(0,len(allwarehouses_objects)):
                #make backup of warehouse items and reset insurance
                backup = emptywarehouse(allwarehouses_objects[i])
                backup_of_items+= backup
            #move items from current warehouse until enough insurance to cover new item price
            copy_current_warehouse_items_to_backup(itemprice,backup_of_items,current_warehouse)
            #sets static variable redistribute_items to True
            move_items_to_increase_insurance.redistribute_items=True

    if move_items_to_increase_insurance.redistribute_items==True:
        #redistribute backup items to warehouses
        redistribute(backup_of_items,itemprice,allwarehouses_objects)
        move_items_to_increase_insurance.redistribute_items =False
   
    return


'''
Function Name: 
  --> copy_current_warehouse_items_to_backup(itemprice,backup_of_items,current_warehouse)

Function Description:
  --> This fucntion removes items from the selected warehouse until enough insurance is reached
  --> Items removed are appended to a backup list, the selected warehouse insurance
      is then incremented and the item is deleted from the selected warehouse.
  
User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - itemprice
  --> IN and OUT (Reference Parameters):
      - current_warehouse,backup_of_items
'''
def copy_current_warehouse_items_to_backup(itemprice,backup_of_items,current_warehouse):

    #sorts selected warehouse items in ascending order
    current_warehouse.warehouse_contents = insertion_sort(current_warehouse.warehouse_contents,False)
    #backup items,increase insurance and delete item
    while itemprice>current_warehouse.remaining_insurance:
        backup_of_items.append(current_warehouse.warehouse_contents[0])
        current_warehouse.increase_warehouse_insurance(current_warehouse.warehouse_contents[0].item_price)
        del current_warehouse.warehouse_contents[0]
 
'''
Function Name: 
  -->  move_item_to_warehouse(destination_warehouse,current_warehouse)

Function Description:
  --> This function appends items of current selected warehouse to the seleceted
      destination warehouse.
  --> It increases and decreases the current and destination selected warehouse by the appended item price.
  --> It then deletes the item from the current selected warehouse.
  
User Interface Variables:
  --> OUT(Return Values):
      - None
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - destination_warehouse,current_warehouse
'''        
def move_item_to_warehouse(destination_warehouse,current_warehouse):

    itemprice =0
    #appends item to destination warehouse
    destination_warehouse.warehouse_contents.append(current_warehouse.warehouse_contents[0])
    itemprice = current_warehouse.warehouse_contents[0].item_price
    #increase and descrease warehouses insurance
    current_warehouse.increase_warehouse_insurance(itemprice)
    destination_warehouse.decrease_warehouse_insurance(itemprice)
    print("Item %s    moved to warehouse %s"%(current_warehouse.warehouse_contents[0],destination_warehouse.warehouse_name))
    #delete item from warehouse
    del current_warehouse.warehouse_contents[0]


'''
Function Name: 
  -->  suggest_moveable_items(warehouse,itemprice)

Function Description:
  --> This function suggests a list of items that could be moved in order for the new highly
      priced item to be accomodated
  
User Interface Variables:
  --> OUT(Return Values):
      - bool: True or False
  --> IN(Value Parameters):
      - warehouse,itemprice
  --> IN and OUT (Reference Parameters):
      - None
'''     
def suggest_moveable_items(warehouse,itemprice):

    #local variables
  
    suggested_items=[]
    i=0
    #gets remaining insurance 
    sum_of_suggested_items= warehouse.remaining_insurance
    number_of_items = len(warehouse.warehouse_contents)
   
    #adds items to suggested list while itemprice is greater than insurance
    while itemprice>sum_of_suggested_items:
        if i == number_of_items:
            break
        suggested_items.append(warehouse.warehouse_contents[i])
        sum_of_suggested_items+=warehouse.warehouse_contents[i].item_price
        i+=1
    
    #warns user if new item to be added
    #is worth less than less expensive item in warehouse
    if warehouse.warehouse_contents[0].item_price>itemprice:
      
        printwarehouseinfo(warehouse)
        print("\nLEAST EXPENSIVE SUGGESTED ITEM")
        print("-------------------------------- ")
        print_records(suggested_items)
        print("\nThe item you're adding is worth less than the least expensive item in the warehouse")
        print("Proceed?(Y/N): ")
        choice = get_valid_yes_or_no()
        if choice=='Y':
           return True
        else:
           return False
    #prints warehouse info and suggested list
    printwarehouseinfo(warehouse)
    print("\n\nSUGGESTED LIST OF ITEMS     ")
    print("-----------------------      ")
    print_records(suggested_items)
    print("\nThe following items could be moved to free up space,would you like to move them?(Y/N): ")
    choice = get_valid_yes_or_no()
  
    if choice=='Y':
        return True
    else:
        return False

'''
Function Name: 
  --> redistribute(backup_of_items,itemprice,allwarehouses_objects)

Function Description:
  --> This function redistributes the backed-up items to the emptied warehouses.
  --> It appends an item to discarded warehouse if insuffient space around all warehouses.
  
User Interface Variables:
  --> OUT(Return Values):
      - bool: None
  --> IN(Value Parameters):
      -backup_of_items,itemprice
  --> IN and OUT (Reference Parameters):
      - allwarehouses_objects
''' 
def redistribute(backup_of_items,itemprice,allwarehouses_objects):
    descending = True
    #sorts backup items in descending order
    backup_of_items = insertion_sort(backup_of_items,descending)

    lenght = len(backup_of_items)
    
    #iterates over all warehouses and destribute items 
    for i in range(0,lenght):
        for j in range(0,len(allwarehouses_objects)):
            if allwarehouses_objects[j].remaining_insurance >= backup_of_items[i].item_price:
               allwarehouses_objects[j].warehouse_contents.append(backup_of_items[i])
               allwarehouses_objects[j].decrease_warehouse_insurance(backup_of_items[i].item_price)
               print("Item %s moved to warehouse %s"%(backup_of_items[i],allwarehouses_objects[j].warehouse_name))
               break

        else:
            #append item to discarded warehouse
            print("Item '%s' with value '%s' discarded"%(backup_of_items[i].item_number,backup_of_items[i].item_price))
            discarded_items.warehouse_contents.append(backup_of_items[i])

'''
Function Name: 
  --> emptywarehouse(warehouse)

Function Description:
  --> This function makes a deep copy of a selected warehouses contents.
  --> It then deletes the contents of the selected warehouse
      decreases overall insurance by the selected warehouse insurance and resets its insurance to maximum.
  
User Interface Variables:
  --> OUT(Return Values):
      - bool: return backup_of_items
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - warehouse
'''          
def emptywarehouse(warehouse):
    #deep backup items
    backup_of_items = copy.deepcopy(warehouse.warehouse_contents)
    del warehouse.warehouse_contents[:]#deletes contents from warehouse

    #decrease overall insurance and reset selected warehouse insurance
    Warehouse.overall_insurance-=warehouse.remaining_insurance
    warehouse.remaining_insurance=0
    warehouse.increase_warehouse_insurance(2000000000) 
    return backup_of_items

'''
Function Name: 
  --> mergeSort(selected_warehouse)

Function Description:
  --> This function is a divide and conquer algorithm.
  --> It first finds the middle point of the list, and recursively divide the list
      until at the bottom there are only two elements left.
      It compares the elements and swap their indexes.
  --> It returns te sorted list once the lenght is less than or 1   
  
User Interface Variables:
  --> OUT(Return Values):
      - merge(lefthalf,righthalf)
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - selected_warehouse
'''    
def mergeSort(selected_warehouse):
    #returns sorted selected warehouse items
        if len(selected_warehouse)<=1:
            return selected_warehouse
        #get middle value
        mid = int(len(selected_warehouse)/2)
        #sorts each halve of selected warehouse items
        lefthalf,righthalf = mergeSort(selected_warehouse[:mid]),mergeSort(selected_warehouse[mid:])
        return merge(lefthalf,righthalf)


'''
Function Name: 
  --> merge(left,right)

Function Description:
  --> This function compares the left index value to the right index value and appends
      the values to result_container list in ascending order.
  --> If leftindex or rightindex variable is above the lenght of left or right list then copy
      the remaining values to result_container.  

User Interface Variables:
  --> OUT(Return Values):
      - result_container
  --> IN(Value Parameters):
      - left half and right half of selected warehouse
  --> IN and OUT (Reference Parameters):
      - None
'''              
def merge(left,right):

    #local variables
    result_container=[]
    leftindex=rightindex=0

    while leftindex<len(left) and rightindex <len(right):
        #appends item to result_container list and increase index
         if left[leftindex].item_number<right[rightindex].item_number:
            result_container.append(left[leftindex])
            leftindex+=1
         else:
           result_container.append(right[rightindex])
           rightindex+=1
    #copy remaining elements of a half into result_container
    result_container.extend(left[leftindex:])
    result_container.extend(right[rightindex:])
   
    return result_container

'''
Function Name: 
  --> insertion_sort(selected_warehouse,descending)

Function Description:
  --> This function sorts a warehouse by item price in ascending or descending order.
  --> Assuming its sorting in ascending order:
     1 - It begins by asssuming that th element at position 0 is already sorted.
     2 - It compares element at position j to element at position i and swaps them if j is greater
     3 - It then compares the new element at position j to j-1 and swap the elements until we reacha smaller
         element at the beginning of the warehouse list.
       - It then repeats the above 3 steps until the warehouse list is finally sorted.
    
User Interface Variables:
  --> OUT(Return Values):
      - selected_warehouse
  --> IN(Value Parameters):
      - selected_warehouse,bool descending
  --> IN and OUT (Reference Parameters):
      - None
''' 
def insertion_sort(selected_warehouse,descending):

    #local variables
    j=0
    swap_list=[]

    for i in range(1,len(selected_warehouse)):
        #inserts element at position 1 to swap list
        swap_list.insert(0,selected_warehouse[i])
        j =i-1
        if descending:
            #compares item price of swap list to selected warehouse and swap is smaller
            while swap_list[0].item_price > selected_warehouse[j].item_price and j>=0:
                selected_warehouse[j+1] = selected_warehouse[j]#keeps swapping until it meets a greater value
                j=j-1
            selected_warehouse[j+1] = swap_list[0]
        #sorts warehouse_objects in ascending order    
        else:
            while swap_list[0].item_price < selected_warehouse[j].item_price and j>=0:
                selected_warehouse[j+1] = selected_warehouse[j]
                j=j-1
            selected_warehouse[j+1] = swap_list[0]
    return selected_warehouse


'''
Function Name: 
  --> insertion_sort_objects(warehouse_objects,descending)

Function Description:
  --> This function sorts a warehouse by item price in ascending or descending order.
  --> Assuming its sorting in ascending order:
     1 - It begins by asssuming that th element at position 0 is already sorted.
     2 - It compares element at position j to element at position i and swaps them if j is greater
     3 - It then compares the new element at position j to j-1 and swap the elements until we reacha smaller
         element at the beginning of the warehouse list.
       - It then repeats the above 3 steps until the warehouse list is finally sorted.
    
User Interface Variables:
  --> OUT(Return Values):
      - warehouse_objects
  --> IN(Value Parameters):
      - warehouse_objects,bool descending
  --> IN and OUT (Reference Parameters):
      - None
''' 
def insertion_sort_objects(warehouse_objects,descending):

    temp =[]

    for i in range(1,len(warehouse_objects)):
        #inserts element at position 1 to swap list
        temp.insert(0,warehouse_objects[i])
        j =i-1
        if descending:
            #compares warehouses remaining insurance of swap list to selected warehouse and swap is smaller
            while temp[0].remaining_insurance>=warehouse_objects[j].remaining_insurance and j>=0:
                warehouse_objects[j+1] = warehouse_objects[j]#keeps swapping until it meets a warehouse with greater value
                j=j-1
            warehouse_objects[j+1] = temp[0]
        #sorts warehouse_objects in ascending order
        else:
            while temp[0].remaining_insurance<=warehouse_objects[j].remaining_insurance and j>=0:
                warehouse_objects[j+1] = warehouse_objects[j]
                j=j-1
            warehouse_objects[j+1] = temp[0]

    return warehouse_objects

'''
Function Name: 
  --> get_valid_item_description()

Function Description:
  --> This function prompts the user for an item description
  --> Rejects item description if less than 1 or greater than 45
  --> Returns valid item description if inputted.
    
User Interface Variables:
  --> OUT(Return Values):
      - description
  --> IN(Value Parameters):
      - None
  --> IN and OUT (Reference Parameters):
      - None
'''
def get_valid_item_description():

  flag = True
  while flag== True:  
      #propmpts item decription
      description = input(" ---> \nInput item description: ")
      #checks description lenght
      if len(description) > 45:
          print("Item description too long(max lenght: '45'),try again: ")
      elif len(description) < 1:
          print("Item description too short(min lenght: '1'),try again: ")
      else:
         flag = False
         return description

main()  
