from collections import UserDict
from datetime import datetime
import json
import os

class CustomException(Exception):
    pass

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please or "
        except IndexError:
            return "Enter contact name"
        except CustomException as e:
            return str(e)
    return wrapper

def hello_command(params):
    return "How can I help you?"

def iter_record(params):
    for addres in address_book:
        print(addres)
        print('------------------------------')
    
def find_command(params):
    if not params:
        return "Enter a word to search"
    return "\n".join(f" {result}" for result in address_book.search_by_content(params))        

@input_error
def add_command(params):
    list_param = params.split(' ')
    name = list_param[0]
    phone = list_param[1]
    birthday = None
    if len(list_param) == 3:
        birthday = list_param[2]
    record = address_book.search_record(name)
    record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    return f"Contact {name} added"

@input_error
def change_command(params):
    name, phone, new_phone = params.split(' ')
    record = address_book.search_record(name)
    record.edit_phone(phone, new_phone)
    return f"Phone number for {name} changed"

@input_error
def phone_command(params):
    name = params.strip()
    return address_book.search_records(name)

@input_error
def birthday_command(params):
    name = params.strip()
    return address_book.search_records(name)
    
def show_all_command(params):
    return address_book.show_all_records()

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_record(self, search_criteria):
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                return record
        record = Record(search_criteria)
        self.add_record(record)
        return record

    def search_records(self, search_criteria):
        results = []
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                results.append(record)
        return results
    
    def show_all_records(self):
        results = ''
        for record in self.data.values():
            results += "\n"+f"{record.name.value}:"+"".join(f" {phone.value}" for phone in record.phones)
            if record.birthday:
                results += ' birthday: '+ str(record.birthday.value.date())
        if not results:
            results = "Contact list is empty"
        return results

    def __iter__(self):
        self._iter_index = 0
        self._iter_chunk_size = 5
        return self

    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration

        chunk = list(self.data.values())[self._iter_index:self._iter_index + self._iter_chunk_size]
        self._iter_index += self._iter_chunk_size

        return "\n".join(str(record) for record in chunk)
    
    def save_to_file(self, file_path):
        data = {
            'records': [record.to_dict() for record in self.data.values()]
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, default=str)

    def load_from_file(self):
        file_path = os.path.join(os.getcwd(), "address_book.json")
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            for record_data in data['records']:
                record = Record.from_dict(record_data)
                self.add_record(record)
    
    def search_by_content(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                results.append(str(record))
            else:
                for phone in record.phones:
                    if search_string.lower() in phone.value.lower():
                        results.append(str(record))
                        break
        return results        

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            # 1988-08-11 00:00:00
            #birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d')
            birthday = self.birthday.value
            next_birthday = datetime(year=today.year, month=birthday.month, day=birthday.day).date()
            if today > next_birthday:
                next_birthday = datetime(year=today.year+1, month=birthday.month, day=birthday.day).date()
            days_left = (next_birthday - today).days
            return days_left
    
    def __str__(self):
        results = f"{self.name.value}: {' '.join(phone.value for phone in self.phones)}"
        if self.birthday:
                results += ' birthday: '+ str(self.birthday.value.date())
        return results
    
    def to_dict(self):
        return {
            'name': self.name.value,
            'birthday': str(self.birthday.value.date()) if self.birthday else None,
            'phones': [phone.value for phone in self.phones]
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data['name'], data['birthday'])
        for phone in data['phones']:
            record.add_phone(phone)
        return record

class Field:
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(self._validate_phone(value))
    
    @staticmethod
    def _validate_phone(phone):
        if not len(phone) == 10:
            raise CustomException("Phone number must have 10 digits")
        if not phone.isdigit():
            raise CustomException("Phone number should contain only digits")
        return phone

    @Field.value.setter
    def value(self, new_value):
        self._value = self._validate_phone(new_value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(self._validate_birthday(value))

    @staticmethod
    def _validate_birthday(value):
        if value == None:
            raise CustomException("Date of birth == None")
        if not len(value) == 10:
            raise CustomException("Date of birth must have 10 characters ""1988-08-11""")
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise CustomException("Date of birth should be ""1988-08-11""")        
        return value
    
    @Field.value.setter
    def value(self, new_value):
        self._value = self._validate_birthday(new_value)

def main():
    commands = {
        'hello': hello_command,
        'add': add_command,
        'change': change_command,
        'phone': phone_command,
        'show all': show_all_command,
        'iter rec': iter_record,
        'find': find_command,
    }

    while True:
        user_input = input("> ").lower()
        if user_input in ["good bye", "close", "exit"]:
            address_book.save_to_file(os.path.join(os.getcwd(), "address_book.json"))
            print("Good bye!")
            break
        
        for command, handler in commands.items():
            if user_input.startswith(command):
                params = user_input[len(command):].strip()
                result = handler(params)
                print(result)
                break
        else:
            print("Unknown command")

#contacts = {}
address_book = AddressBook()
address_book.load_from_file()

if __name__ == "__main__":
    main()
