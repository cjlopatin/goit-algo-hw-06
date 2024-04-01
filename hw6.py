# Python Core
# Модуль 6
# домашнє завдання 
# Лопатін Євген


from collections import UserDict

class Field:
    def __init__(self, value):
        if self.__is_valid(value):
            self.value = value
        else:
            raise ValueError
        
    def __is_valid(value):
        return True

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу з обробкою помилок

    def __init__(self, value):
        if self.__is_valid(value):
            self.value = value
        else:
            raise ValueError

    def __is_valid(self, value):
        if len(value)>=1:
            return True
        raise ValueError('Імя має бути від 1 букви')

class Phone(Field):
    # Реалізовано валідацію номера телефону (перевірка на 10 цифр).

    def __init__(self, value):
        if self.__is_valid(value):
            self.value = value
        else:
            raise ValueError

    def __is_valid(self, value):
        if value.isdigit() and len(value) == 10:
            return True
        raise ValueError('Телефон має бути з 10 цифр')
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Реалізовано зберігання об'єкта Name в окремому атрибуті.
# Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.

    def add_phone(self, phone): # метод додавання телефону
        my_phone = Phone(phone)
        self.phones.append(my_phone)

    def remove_phone(self, phone): # метод видалення телефону
        f = Phone(phone)
        for user_phone in self.phones:
            if user_phone.value == f.value:
                del self.phones[self.phones.index(user_phone)]

    def edit_phone(self, old_phone, new_phone): # метод редагування телефону
        phone_old = Phone(old_phone)
        phone_new = Phone(new_phone)
        self.remove_phone(phone_old.value)
        self.add_phone(phone_new.value)

    def find_phone(self, phone): # метод пошуку телефону
        f = Phone(phone)
        for user_phone in self.phones:
            if f.value == user_phone.value:
                return user_phone            
        return None

 
class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        for user_name, record in self.data.items():
            if user_name.value == name:
                return record
        return None

    def delete(self, name):
        for user_name, record in self.data.items():
            if user_name.value == name:
                del self.data[record.name]
                break

book = AddressBook()    
# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")