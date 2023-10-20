from datetime import datetime

# current_datetime = datetime.now()

# future_month = (current_datetime.month % 12) + 1
# future_year = current_datetime.year + int(current_datetime.month / 12)
# future_datetime = datetime(future_year, future_month, 1)
# print(current_datetime.month % 12)
# print(int(current_datetime.month / 12))
# print(future_month)
# print (future_year)
# print(future_datetime)
# print(current_datetime < future_datetime)    # True

# seventh_day_2020 = datetime(year=2020, month=1, day=7, hour=14)
# print(seventh_day_2020.strftime('%A %d %B %Y')) # Tuesday 07 January 2020

# def get_days_from_today(date):
#   input_datetime=datetime.strptime(date, '%d.%m.%Y')
#   current_datetime = datetime.now()
#   print(input_datetime)
#   print(current_datetime)
#   difference = current_datetime - input_datetime
#   print(difference.days)
#   return difference.days  
# get_days_from_today('11.12.1955')

# def get_days_from_today(date):
#   input_datetime=datetime.strptime(date, '%d.%m.%Y')
#   current_datetime = datetime.now()
#   print(input_datetime)
#   print(current_datetime)
#   difference = current_datetime - input_datetime
#   print(difference.days)
#   return difference.days  
# get_days_from_today('09.10.2020')
# get_days_from_today('09.10.2021')

# str1 = '09.10.2020'

# input_datetime=datetime.strptime(str1, '%d.%m.%Y')
# str_out = input_datetime.strftime("%d.%m.%Y")
# print (str1, ">>>>>>>>>>>", input_datetime, ">>>>>>>>>>>",str_out)
# print(str1 == str_out)

# str2 = '09.01.2002'
# try:
#   input_datetime2=datetime.strptime(str2, '%d.%m.%Y').date()
#   print (str2, ">>>>>>>>>>>", input_datetime2, ">>>>>>>>>>>",input_datetime2.strftime("%d.%m.%Y"))
#   print()
  
# except:
#   print("\033[31m{}\033[0m".format("Enter the date in the format DD.MM.YYYY"))
# print(str2 == input_datetime2.strftime("%d.%m.%Y"))

# def get_days_from_today(date):
#   input_datetime=datetime.strptime(date, '%d.%m.%Y')
#   current_datetime = datetime.now()
#   print(input_datetime)
#   print(current_datetime)
#   difference = current_datetime - input_datetime
#   print(difference.days)
#   return difference.days  
# get_days_from_today('09.10.2020')
# get_days_from_today('09.10.2021')

tel = []
if tel == []:
    tel.append ("55555555")
else:
    tel[0] = "hello"
print(tel)