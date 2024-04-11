# Python Core
# Модуль 8
# домашнє завдання
# Лопатін Євген

from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
import pickle

file_path = Path('addressbook.pkl')

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field): # створюємо клас телефону та перевіряємо його на вміст 10 цифр)
        def __init__(self, value):
            if len(value)==10 and value.isdigit():
                super().__init__(value)
            else:
                raise ValueError("The phone number must be a string and consist of 10 digits")
        
class Birthday(Field): # створюємо клас дня народження
    def __init__(self, value):
        try:
            # Додаємо перевірку формату даних та перетворюємо рядок на об'єкт datetime
            date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record: # створюємо клас Record
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    
    def add_phone(self,phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
      
    def edit_phone(self, new_phone):
            self.add_phone(new_phone)      

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("A date of birth already exists for this contact")
        self.birthday = Birthday(birthday)


class AddressBook(UserDict): # створюємо клас Record з наслідованням словника
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
        
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days = 7): # функція майбутніх днів народження під тиждень
        
        upcoming_birthdays=[]
        today = datetime.today().date()
        
        def find_next_weekday(d, weekday: int):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return d + timedelta(days = days_ahead)        

        for user in self.data.values():   
            if user.birthday is None: continue
            birthday:datetime = user.birthday.value
            birthday_this_year = datetime(today.year, birthday.month, birthday.day).date()
            
            if birthday_this_year < today:  # Якщо дата народження вже пройшла цього року
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)  # Переносимо наступний рік

            if 0 <= (birthday_this_year - today).days <= days:  # Якщо день народження в межах вказаного періоду
                if birthday_this_year.weekday() >= 5:  # Якщо день народження випадає на суботу або неділю
                    birthday_this_year = find_next_weekday(birthday_this_year, 0)  # Знаходимо наступний понеділок

        
                upcoming_birthdays.append({'name': user.name.value,
                        'congratulation date': birthday_this_year.strftime('%d.%m.%Y')})

            return upcoming_birthdays
        
    def __str__(self):
        return "\n".join(str(user) for user in self.data.values())
    
def input_error(func):  # створюємо декоратор механізмy виключень
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and / or 10 digit phone number / or birthday in dd.mm.yyyy format, please"
        except KeyError:
            return "No such name found"
        except IndexError:
            return "There is no such a command"
        except Exception as e:
            return f"Error: {e}"

    return inner

# функції з минулих завдань  обгортаємо декоратором
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday)
    return 'Birthday added'
   

@input_error
def change_contact(args, book: AddressBook):
    name, new_phone = args
    record = book.find(name)
    record.edit_phone(new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    phone = args[0]
    record = book.find(phone)
    return '; '.join(str(phone) for phone in record.phones)

@input_error   
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return record.birthday

@input_error
def show_all(book: AddressBook):
    return book

def show_all_birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()

def save_data(book, filename="addressbook.pkl"): # сериалізація книги
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"): # десериалізація книги
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()          



# лист доступних команд
commands_list = """
Here is the list of available commands:
1. input command: hello - to receive a greeting from the bot
2. input command: add [name] [phone] - to add a new contact with name and phone of 10 digits
3. input command: change [name] [new phone] - to change 10 digits phone number of given contact.
4. input command: phone [name] - to show the phone number of given contact.
5. input command: all - to show all contacts.
6. input command: add-birthday [name] [date of birth in formad dd.mm.yyyy] - to add the date of birth for given contact.
7. input command: show-birthday [name] - to show the contacts birthday.
8. input command: birthdays - to show upcoming birthdays for next 7 days.
9. input commands: close or exit - to Quit the program.
0. input command: commands - to see the full list of commands.
"""

# основна функція
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    print(commands_list)
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_all_birthdays(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))
        
        elif command == "commands":
            print(commands_list)  
          
    

        else:
            print("Invalid command.")

    save_data(book)
    
    
if __name__ == "__main__":
    main()