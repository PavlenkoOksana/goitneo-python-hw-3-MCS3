import pickle
from collections import UserDict
from collections import defaultdict
from datetime import datetime
from datetime import timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
 

class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def valid_phone(self, phone):
        if len(phone) != 10 or phone.isdigit() == False:
            print("\033[31m{}\033[0m".format("The number must consist of 10 digits. try again"))
        else:
            return phone


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}"

    def valid_birthday(self, birthday):
        try:
            birthday_to_data = datetime.strptime(birthday, '%d.%m.%Y').date()
            self.birthday = birthday_to_data.strftime("%d.%m.%Y")
            return self.birthday
        except:
            print("\033[31m{}\033[0m".format("Enter the date in the format DD.MM.YYYY"))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if Phone(phone).valid_phone(phone):
            self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        if self.birthday == None and Birthday(birthday).valid_birthday(birthday):
           birthday_to_data = datetime.strptime(birthday, '%d.%m.%Y')
           self.birthday = birthday_to_data.strftime("%d.%m.%Y")
           return "\033[32m{}\033[0m".format(f"{self.name}'s birthday added.")
        elif self.birthday != None: 
            return "\033[31m{}\033[0m".format(f"The contact's {self.name} <birthday> field is already filled in") 
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
               
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def edit_phone(self, old_phone, new_phone):
        if Phone(new_phone).valid_phone(new_phone):
            for p in self.phones:
                if p.value == old_phone:
                    p.value = new_phone
                    return "\033[32m{}\033[0m".format("Contact changed.")
                else:
                    return "\033[31m{}\033[0m".format("Please enter a correct phone.")


class AddressBook(UserDict):    
    def add_record (self, record):
        self.data[record.name.value] = record

    def find(self, name):
        name = name.lower()
        for cont in self.data:
            if str(cont).lower() == name:
                return self.data.get(cont)
        else:
            raise KeyError
        
    def delete(self, name):
        cont_for_del=""
        for cont in self.data:
            if str(cont) == name:
                cont_for_del = cont             
        self.data.pop(cont_for_del)
    
    def get_birthdays_per_week(self):
        birthdays_per_week = {}
        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()    
        for record in self.data.values():
            if not record.birthday:
                continue
            name = record.name.value
            birthday = datetime.strptime(record.birthday, '%d.%m.%Y').date()
            birthday_this_year: datetime = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year = today.year + 1)
            if today <= birthday_this_year <= today + timedelta(7) :
                wd = birthday_this_year.weekday()
                if wd in (5, 6):
                    birthdays_per_week["Monday"].append(name)
                else:
                    birthdays_per_week[birthday_this_year.strftime("%A")].append(name)      
        if len(birthdays_per_week) == 0:
            return "No birthdays next week."
        else:
            print("birthdays_per_week",birthdays_per_week)
            for weekday, user in birthdays_per_week.items():                
                print("\033[36m{}".format(weekday)+"\033[30m{}".format(": " + ", ".join(user)))
            return "\033[1m\033[36m{}\033[0m".format("Don't forget to wish your colleagues a happy birthdays!")

    def close(self):
        self.fh.close()

    def save_to_file(self):
        with open('address_book_txt.txt', "wb") as fh:
            pickle.dump(self, fh)
        return "\033[32m{}\033[0m".format("Phone book saved to file: 'address_book_txt.txt'.")  
                    
    def read_from_file(self):
      with open('address_book_txt.txt', "rb") as fh:
        unpacked = pickle.load(fh)
      print ("\033[32m{}\033[0m".format("The phone book was loaded from a file: 'address_book_txt.txt'.")) 
      return unpacked
 

def parse_input(user_input):
    if not user_input:
        return "unknown", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "\033[31m{}\033[0m".format("Give me name and phone please.")
        except IndexError:
            return "\033[31m{}\033[0m".format("Give me name please.")
        except KeyError:
            return "\033[31m{}\033[0m".format("Please enter a correct name.")
        except:
            return "\033[31m{}\033[0m".format("Oops, something went wrong, try again.")
    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    rec = Record(name)
    rec.add_phone(phone)
    book.add_record(rec)
    return "\033[32m{}\033[0m".format("Contact added.")


@input_error
def change_username_phone(args, book):
    name, old_phone, new_phone = args
    name = name.lower()
    if Phone(new_phone).valid_phone(new_phone):
        if book.find(name) != None:
            rez = book.find(name)
            return rez.edit_phone(old_phone, new_phone)
        else:
            raise KeyError    
       

@input_error
def phone_username(args, book):
    name = args
    name[0] = name[0].lower()
    res = book.find(name[0])
    return res.phones[0].value
    

@input_error
def all_phone_print(book):
    for name, record in book.data.items():
        print(record)


@input_error
def add_birthday(args, book):
    name, birthday = args
    name = name.lower()
    res = book.find(name)
    return res.add_birthday(birthday)
     

@input_error
def show_birthday(args, book):
    name = args
    name[0] = name[0].lower()
    res = book.find(name[0])
    return res.birthday


@input_error
def birthdays(book):
    return book.get_birthdays_per_week()


@input_error
def main():
    book = AddressBook()
    print("\033[1m\033[34m{}\033[0m".format("Welcome to the assistant bot!"))
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("\033[34m{}\033[0m".format("Good bye!"))
            break
        elif command == "hello":
            print("\033[34m{}\033[0m".format("How can I help you?"))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_username_phone(args, book))
        elif command == "phone":
            print(phone_username(args, book)) 
        elif command == "all":
            all_phone_print(book)  
        elif command == "add-birthday":
            print(add_birthday(args, book))   
        elif command == "show-birthday":
            print(show_birthday(args, book))   
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "dump":
            print (book.save_to_file())  
        elif command == "load":
            book = book.read_from_file()                      
        elif user_input == "" or command == "":
            print("\033[31m{}\033[0m".format("You did not enter the command, please try again."))
        else:
            print("\033[31m{}\033[0m".format("Invalid command, please try again."))


if __name__ == "__main__":
    main()

