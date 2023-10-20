from collections import defaultdict
from datetime import datetime, timedelta


def get_birthdays_per_week(users):
    birthdays_per_week = {}
    birthdays_per_week = defaultdict(list)
    today = datetime.today().date()
    
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year: datetime = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year = today.year + 1)
        if today <= birthday_this_year <= today + timedelta(7) :
            wd = birthday_this_year.weekday()
            if wd in (5, 6):
                birthdays_per_week["Monday"].append(name)
            else:
                birthdays_per_week[birthday_this_year.strftime("%A")].append(name)            
    for weekday, user  in birthdays_per_week.items():
        print("\033[36m{}".format(weekday)+"\033[30m{}".format(": " + ", ".join(user)))
        

#if __name__ == "__main__":
          
get_birthdays_per_week([{"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Taras Svhevchenko", "birthday": datetime(1970, 10, 9)},
    {"name": "Lesja Ukrainka", "birthday": datetime(1971, 10, 10)},
    {"name": "Star Pol", "birthday": datetime(1900, 10, 11)},
    {"name": "Elvis Presly", "birthday": datetime(1912, 10, 12)},
    {"name": "Ben Cambr", "birthday": datetime(1913, 10, 13)},
    {"name": "Bill Gates1", "birthday": datetime(1955, 12, 11)},
    {"name": "Bill Gates2", "birthday": datetime(1955, 3, 3)},
    {"name": "Bill Gates3", "birthday": datetime(1944, 5, 20)},
    {"name": "Volodimir Zelensky", "birthday": datetime(1979, 10, 7)},
    {"name": "Alla Mazur", "birthday": datetime(1999, 10, 8)},
    {"name": "Name 11111", "birthday": datetime(1999, 10, 14)},
    {"name": "Name 22222", "birthday": datetime(1999, 10, 15)},
    {"name": "Getman Skoropadskiy", "birthday": datetime(1999, 10, 16)},
    {"name": "Arni Schwarzneger", "birthday": datetime(1955, 10, 13)}
])


