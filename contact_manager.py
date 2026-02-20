import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os

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
#   welcome title and display next upcoming bday
#-----------------------------------------------------------------------
print("")
print("Welcome to Contact Manager!")
# display contact with closest bday

upcoming_bdays = []
for contact in contacts:
    if contact['birthday'] != "N/A":
        today = date.today()
        
        bday_str = (contact['birthday'])
    
        # parse bday string to date object.
        bday_date = date.strptime(bday_str, "%Y-%m-%d")
        # class datetime.date(year, month, day) All arguments are required.        
                
        # convert bday object to this year for comparison to today.
        bday_this_year = date(today.year, bday_date.month, bday_date.day) 

        date_difference = bday_this_year - today
        # note subtracting two date objects returns a time.delta object.       
        
        days_away = {
            "name" : contact['name'],
            "days to birthday" : date_difference.days,
            "converted birthday" : bday_this_year
        }
        if bday_this_year == today or date_difference.days > 0:
            upcoming_bdays.append(days_away)
    else:
        continue
    
sorted_bdays = sorted(upcoming_bdays, key=lambda contact: contact["days to birthday"])
closest_bday = sorted_bdays[0] # note [0:N] creates a list not a dictionary

if closest_bday['days to birthday'] == 0:
    print(f"{closest_bday['name']}'s birthday is today!")
else:
    print(f"{closest_bday['name']}'s birthday is {closest_bday['days to birthday']} days away on {closest_bday['converted birthday'].month}/{closest_bday['converted birthday'].day}") 

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")    
    print("[0] Exit")
    print("[1] Add Contact")
    print("[2] View All Contacts")
    print("[3] Search Contacts")
    print("[4] Delete Contact")
    print("[5] Export to text file")   

#-----------------------------------------------------------------------
#   option [1] Add Contact
#-----------------------------------------------------------------------
def add_contact(): 

    while True:
        try:
            name = str(input("Enter contact name: ").lower())
            if name == "":
                print("Blank is invalid entry. Please try again.")
            else:
                break                
        except ValueError:
            print("Invalid entry. Please try again.")

    while True:        
        try:
            phone = input("Enter phone number: ")
            if phone == "":
                print("Blank is invalid entry. Please try again.")
            else:
                break          
        except ValueError:
            print("Invalid number. Please try again.")

    while True:
        try:
            email = input("Enter email: ").lower()
            if email == "":
                print("Blank is invalid entry. Please try again.")
            elif "@" not in email:
                print("Invalid email format. Please try again.")
            else:
                break        
        except ValueError:
            print("Invalid entry. Please try again.")
    
    while True:        
        try:
            bday = "N/A"
            choice = input("Do you want to enter a birthday, Yes or No: ").lower()
            if choice == "no":
                break
            elif choice == "":
                print("Blank is invalid entry. Please try again.")
            elif choice == "yes":
                bday = str(input("Enter birthday in (yyyy-mm-dd) format: "))
                break
            else:
                print("Invalid entry. Please try again.")
    
        except ValueError:
            print("Invalid number. Please try again.")

    contact_item = {
        "name": name,
        "phone": phone,
        "email": email,
        "birthday": bday
    }

    contacts.append(contact_item)
    print(f'Contact for {name} added.')

#-----------------------------------------------------------------------
#   option [2] View All Contacts
#-----------------------------------------------------------------------
def view_contacts():
    print("Displaying All Contacts:")
    print(tabulate(contacts, headers="keys", tablefmt="fancy_grid"))

#-----------------------------------------------------------------------
#  option [3] Search contacts by name
#-----------------------------------------------------------------------

def search_contacts():

    search_term = input("Enter search name: ").lower()

    searched_list = [contact for contact in contacts if search_term in contact['name'].lower()]

    if searched_list:
        print(tabulate(searched_list, headers="keys", tablefmt="fancy_grid"))
    else:
        print('No contacts found.')

#-----------------------------------------------------------------------
#  option [4] Delete Contact
#-----------------------------------------------------------------------

def delete_contact():
    view_contacts()
    
    while True:               
        try:
            choice = str(input("Enter name of contact to delete: ").lower())
            match = next((contact for contact in contacts if contact.get("name") == choice), None)
            if match:
                print(f'Contact information for {choice} removed')
                contacts.remove(match)
                break
            else:
                print('Name does not match existing contacts')
                break
                    
        except ValueError:
            print("Invalid entry. Please try again.")

#-----------------------------------------------------------------------
#  option [5] export to text file
#-----------------------------------------------------------------------
def export_text():
    with open('2026-02-3 contacts.txt', 'w') as file:
        json.dump(contacts, file, indent=4)
    
    file_path = os.path.abspath('2026-02-3 contacts.md')
    print(f"Text file exported to:\n{file_path}")
    
#-----------------------------------------------------------------------
#   function to write to contacts json
#-----------------------------------------------------------------------
def write_json():
    with open('contacts.json', 'w') as file:
        json.dump(contacts, file, indent=4)        

#-----------------------------------------------------------------------
#   while loop to get user input
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
    elif option == '4':
        delete_contact()
        write_json()
    elif option == '5':
        export_text()
    else:
        print("Invalid action. Please try again.")

