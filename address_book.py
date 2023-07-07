from datetime import datetime, timedelta
import pickle
import os


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not str(new_value).isdigit():
            raise ValueError(
                "Invalid phone number. Phone number must be numeric.")


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid birthday format. Birthday must be in the format YYYY-MM-DD.")
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if old_phone in str(phone.value):
                self.phones[i] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            next_birthday = datetime.strptime(
                self.birthday.value, "%Y-%m-%d").replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        result = f"Name: {self.name}\n"
        if self.birthday.value:
            result += f"Birthday: {self.birthday}\n"
        if self.phones:
            result += "Phones:\n"
            for phone in self.phones:
                result += f"- {phone}\n"
        return result


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if record.name.value in self.data:
            existing_record = self.data[record.name.value]
            existing_record.phones.extend(record.phones)
        else:
            self.data[record.name.value] = record
        self.save_to_file('address_book.pkl')

    def delete_record(self, name):
        del self.data[name]
        self.save_to_file('address_book.pkl')

    def search_by_name(self, name):
        result = []
        for record in self.data.values():
            if name.lower() in record.name.value.lower():
                result.append(record)
        return result

    def search_by_phone(self, phone):
        result = []
        for record in self.data.values():
            for p in record.phones:
                if phone in str(p):
                    result.append(record)
                    break
        return result

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        else:
            print(f"File '{filename}' does not exist.")

    def __iter__(self):
        self.index = 0
        self._records = list(self.data.values())
        return self

    def __next__(self):
        if self.index >= len(self._records):
            raise StopIteration
        record = self._records[self.index]
        self.index += 1
        return str(record)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return wrapper


address_book = AddressBook()


@input_error
def add_contact(name, phone, birthday=None):
    record = Record(name)
    correct_phone = phone.replace("-", "").replace(" ", "")
    if len(correct_phone) == 13 and correct_phone.startswith("+380") and (all(not char. isalpha() for char in correct_phone[1:])):
        record.add_phone(correct_phone)
    else:
        return "You entered the wrong number! The number must start with '+380' and contain all digits!"
    if birthday:
        try:
            record.birthday.value = birthday
        except ValueError as e:
            return str(e)
    address_book.add_record(record)
    return f"Contact '{name}' with phone '{correct_phone}' and birthday '{birthday}' has been added."


@input_error
def change_phone(name, old_phone, new_phone):
    correct__old_phone = old_phone.replace("-", "").replace(" ", "")
    correct_new_phone = new_phone.replace("-", "").replace(" ", "")
    if name not in address_book.data:
        return f"!!! Contact '{name}' does not exist !!!"
    if len(correct_new_phone) == 13 and correct_new_phone.startswith("+380") and (all(not char. isalpha() for char in correct_new_phone[1:])):
        record = address_book.data[name]
        record.edit_phone(correct__old_phone, correct_new_phone)
        return f"The phone number for contact '{name}' has been changed to '{correct_new_phone}'."
    else:
        return "You entered the wrong number! The number must start with '+380' and contain all digits!"


@input_error
def remove_contact(name):
    if name not in address_book.data:
        return f"!!! Contact '{name}' does not exist !!!"
    address_book.delete_record(name)
    return f"Contact '{name}' has been removed."


@input_error
def get_phone(name):
    if name not in address_book.data:
        return f"Contact '{name}' does not exist."
    record = address_book.data[name]
    phones = ", ".join([str(phone) for phone in record.phones])
    return f"The phone number(s) for contact '{name}' is/are: {phones}"


@input_error
def get_days_to_birthday(name):
    if name not in address_book.data:
        return f"Contact '{name}' does not exist."
    record = address_book.data[name]
    days_left = record.days_to_birthday()
    if days_left:
        return f"The number of days until {name}'s next birthday: {days_left}"
    else:
        return f"{name}'s birthday is today! Happy birthday!"


def next_birthday(days):
    result = []
    if days >= 1:
        for k, v in address_book.data.items():
            _ = datetime.strptime(
                address_book.data[k].birthday.value, "%Y-%m-%d")
            dt = datetime(year=datetime.now().year, month=_.month, day=_.day)
            td = datetime.now() + timedelta(days=days)
            if _.month < datetime.now().month:
                dt += timedelta(weeks=52)
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{address_book.data[k].birthday.value}, {k}'s birthday through {(dt - datetime.now()).days} days!")
            elif _.month == datetime.now().month and _.day < datetime.now().day:
                dt += timedelta(weeks=52)
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{address_book.data[k].birthday.value}, {k}'s birthday through {(dt - datetime.now()).days} days!")
            else:
                if (dt - datetime.now()).days <= days:
                    result.append(
                        f"{k}:{address_book.data[k].birthday.value}, {k}'s birthday through {(dt - datetime.now()).days} days!")
        return result
    else:
        return "The number of days must be greater than 0"


def show_all_contacts():
    if not address_book.data:
        return "The contact list is empty."
    result = "Contacts:\n"
    for record in address_book.data.values():
        result += str(record) + "\n"
    return result


command_text = 'Hello, Add, Change, Remove, Phone, Next birthday,Birthday list, Search, Show all, Good bye, Close or Exit'


def main():
    address_book.load_from_file('address_book.pkl')
    print(f"Enter command: {command_text}")
    while True:
        command = input("Enter command > ").lower()
        if command == "hello":
            print(f"How can I help you?")
        elif command == "add":
            try:
                name = str(input("Enter Name > "))
                phone = input("Enter Phone > ")
                birthday = input(
                    "Enter Birthday in the format YYYY-MM-DD (optional) > ")
                print(add_contact(name, phone, birthday))
            except ValueError:
                print("Invalid input. Name -> String. Phone -> Number")
        elif command == "change":
            try:
                name, old_phone = input(
                    "Enter Name and Old Phone > ").lower().split()
                new_phone = input("Enter New Phone > ")
                print(change_phone(name, old_phone, new_phone))
            except ValueError:
                print("Invalid input.")
        elif command == "remove":
            name = input("Enter Name > ")
            print(remove_contact(name))
        elif command == "phone":
            name = input("Enter Name > ")
            print(get_phone(name))
        elif command == "next birthday":
            name = input("Enter Name > ")
            print(get_days_to_birthday(name))
        elif command == "birthday list":
            num = input("Enter the number of days: ")
            try:
                days = int(num)
                print(next_birthday(days))
            except ValueError:
                print("The number of days must be an integer!")
        elif command == "search":
            inp = input("Enter Name or Phone > ")
            contacts = []
            if inp.isdigit():
                contacts = address_book.search_by_phone(inp)
            else:
                contacts = address_book.search_by_name(inp)
            if contacts:
                result = "Results:\n"
                for record in contacts:
                    result += str(record) + "\n"
                print(result)
            else:
                print("No contacts found.")
        elif command == "show all":
            print(show_all_contacts())
        elif command == "good bye" or command == "close" or command == "exit":
            print("Good bye!")
            break
        else:
            print(f"Unknown command. Available commands: {command_text}")
    address_book.save_to_file('address_book.pkl')


if __name__ == "__main__":
    main()
