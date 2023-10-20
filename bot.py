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
        elif self.birthday != None: 
            print("\033[31m{}\033[0m".format(f"The contact's {self.name} <birthday> field is already filled in")) 

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        # if self.birthday == None:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        # else:
        #     birthday_in_ddmmyy = self.birthday.strftime("%d.%m.%Y")
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_in_ddmmyy}"
        
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


class AddressBook(UserDict):    
    # def __init__(self):
    #     self.data = UserDict()
    
    def add_record (self, record):
        self.data[record.name.value] = record

    def find(self, name):
        name = name.lower()
        for cont in self.data:
            if str(cont).lower() == name:
                return self.data.get(cont)
    
    # def change(self, name, new_phone):
    #     if Phone(new_phone).valid_phone(new_phone):
    #         for cont in self.data:
    #             if str(cont) == name:
    #                 print("...self.data.get(cont).....", self.data.get(cont).phones, type(self.data.get(cont)))
    #                 if self.data.get(cont).phones == []:
    #                     record = self.data.get(cont)
    #                     record.phones.append(new_phone)
    #                     print("...self.data.get(cont).....", self.data.get(cont).phones, type(self.data.get(cont)))
    #                     print(record)
    #                     #return record.phones[0].value
    #                 else:
    #                     record = self.data.get(cont)
    #                     record.phones[0].value = new_phone
    #                     print("record.phones[0].value",record.phones[0].value)
    #                     #return record.phones[0].value

              
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
            #birthday = record.birthday
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
            print("no birthdays next week")
        else:
            print("birthdays_per_week",birthdays_per_week)
            for weekday, user in birthdays_per_week.items():
                print("\033[36m{}".format(weekday)+"\033[30m{}".format(": " + ", ".join(user)))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


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
    name, phone = args
    name = name.lower()
    if Phone(phone).valid_phone(phone):
        if book.find(name) != None:
            rez = book.find(name)
            rez.phones[0].value = phone
            return "\033[32m{}\033[0m".format("Contact changed.")
        else:
            raise KeyError    
    


@input_error
def phone_username(args, contacts):
    name = args
    name[0] = name[0].lower()
    if name[0] in contacts:
        return contacts[name[0]]
    else:
        raise KeyError
    

@input_error
def all_phone_print(book):
    for name, record in book.data.items():
        print(record)
    #return str[:-1]  


@input_error
def main():
    book = AddressBook()
    contacts = {}
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
        # elif command == "phone":
        #     print(phone_username(args, contacts)) 
        elif command == "all":
            all_phone_print(book)             
        # elif user_input == "" or command == "":
        #     print("\033[31m{}\033[0m".format("You did not enter the command, please try again."))
        else:
            print("\033[31m{}\033[0m".format("Invalid command, please try again."))


if __name__ == "__main__":
    main()

