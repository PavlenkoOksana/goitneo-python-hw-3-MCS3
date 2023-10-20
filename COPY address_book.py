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
        for cont in self.data:
            if str(cont) == name:
                return self.data.get(cont)
       
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
        # for weekday, user in birthdays_per_week.items():
        #     print("\033[36m{}".format(weekday)+"\033[30m{}".format(": " + ", ".join(user)))
        
                 
            
if __name__ == '__main__':

    book = AddressBook()
    rec = Record("Bill")
    print(rec)
    rec.add_phone("1234567890")
    rec.add_phone("1111111111")
    rec.add_phone("2222222222")
    rec.add_birthday("22.10.1955")
    #rec.add_birthday("11-12-1955")
    print(rec)
    rec.add_birthday("20.10.2023")
    print(rec)
    rec.add_birthday("09.01.1980")
    print(rec)
    print(rec.birthday)
    # rec.remove_phone("1111111111")
    # print(rec)
    # found_phone = rec.find_phone("1234567890")
    # print(f"{rec.name}: {found_phone}")
    # rec.edit_phone("1234567890","0987654321")
    # print(rec)
    book.add_record(rec)



    rec1=Record("Sofi")
    rec1.add_phone("3333333333")
    rec1.add_phone("4444444444")
    rec1.add_phone("5555555555")
    rec1.add_birthday("23.10.1980")
    # rec1.edit_phone("5555555555","5555555551")
    # rec1.remove_phone("5555555551")
    book.add_record(rec1)
    # john = book.find("Bill")
    # print("johnjohnjohnjohnjohn",john)
    # john.edit_phone("0987654321", "1234567890")
    # print("johnjohnjohnjohnjohn",john)
    # for name, record in book.data.items():
    #     print("AddressBook:   ",record)
    # book.delete("Sofi")
    rec2=Record("Jan")
    rec2.add_phone("0000000000")
    rec2.add_phone("4444444444")
    rec2.add_phone("5555555555")
    rec2.add_birthday("27.10.1900")
    # rec1.edit_phone("5555555555","5555555551")
    # rec1.remove_phone("5555555551")
    book.add_record(rec2)
    rec3=Record("Georg")
    rec3.add_phone("0000000000")
    rec3.add_phone("4444444444")
    rec3.add_phone("5555555555")
    rec3.add_birthday("3.1.1900")
    # rec1.edit_phone("5555555555","5555555551")
    # rec1.remove_phone("5555555551")
    book.add_record(rec3)
    
    for name, record in book.data.items():
        print("AddressBook:   ",record)
    
    book.get_birthdays_per_week()

   





