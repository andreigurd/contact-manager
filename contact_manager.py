import json
from tabulate import tabulate

#-----------------------------------------------------------------------
#   opening expenses json file
#-----------------------------------------------------------------------
try:
    with open('contacts.json', 'r') as file:
        contacts = json.load(file)
except FileNotFoundError:
    print("Contacts file not found. Blank list created.")
    contacts = [] # makes an empty list
except json.JSONDecodeError:
    print("Issue loading Contacts file. File empty or invalid JSON file. Blank Contacts list created.")
    contacts = []
except ValueError:
    print("Invalid Contact item. Blank list created.")
    contacts = []
except PermissionError:
    print("Need permission to access Contacts file. Blank Contacts list created.")
    contacts = []

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")
    print("Welcome to Contact Manager!")
    print("[0] Exit")
    print("[1] Add Contact")
    print("[2] View All Contacts")


#-----------------------------------------------------------------------
#   option [1] Add Contact
#-----------------------------------------------------------------------
def add_contact(): 

    while True:
        try:
            name = ("Enter name:").lower()
            break
        except ValueError:
            print("Invalid entry. Please try again.")

    while True:        
        try:
            phone = int(input("Enter phone number: "))
            break            

        except ValueError:
            print("Invalid number. Please try again.")

    while True:
        try:
            email = ("Enter email:").lower()
            break
        except ValueError:
            print("Invalid entry. Please try again.")

    contact_item = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact_item)
    print(f'Contact for {name} added.')

#-----------------------------------------------------------------------
#   function to write to contacts json
#-----------------------------------------------------------------------
def write_json():
    with open('contacts.json', 'w') as file:
        json.dump(contacts, file, indent=4)
        

#-----------------------------------------------------------------------
#   option [2] View All Contacts
#-----------------------------------------------------------------------
def view_contacts():
    print("All Contracts:")
    print(tabulate(contacts, headers="keys", tablefmt="fancy_grid"))

#-----------------------------------------------------------------------
#  option [3] Search contacts by name
#-----------------------------------------------------------------------

def search_contacts():

    search_term = input("Enter search name:").lower()

    searched_list = [contact for contact in contacts if search_term in contacts['name'].lower()]
    print(tabulate(contacts, headers="keys", tablefmt="fancy_grid"))

#-----------------------------------------------------------------------
#   # while loop to get user input
#-----------------------------------------------------------------------

while True:
    show_menu()
    option = input("\nSelect Option: ")
    if option == '0':        
        write_json()
        print("Goodbye.")
        break    
    elif option == '1':
        add_contact()
        write_json()
    elif option == '2':
        view_contacts()
    elif option == '3': 
        search_contacts()     

    else:
        print("Invalid action. Please try again.")