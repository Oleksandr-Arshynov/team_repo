from datetime import datetime, timedelta
from rich.console import Console
import re
import csv
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate
from rich.table import Table
from rich.text import Text

console = Console()


class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

    def __str__(self):
        table_format = "| {:<15} | {:<20} | {:<15} | {:<25} | {:<15} |"
        data_row = table_format.format(
            self.name, self.address, self.phone_number, self.email, self.birth_date)
        # self.birth_date('%d.%m.%Y')
        # return f"Name: {self.name}, Address: {self.address} Phone: {self.phone}, Email: {self.email}, Birth date: {self.birth_date})"
        return table_format.format(self.name, self.address, self.phone_number, self.email, self.birth_date)


class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags


class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.names = []
        self.commands = ['додати контакт', 'список контактів',
                         'пошук контактів', 'дні народження']

        # Встановлення автодоповнення на основі доступних команд
        self.command_completer = WordCompleter(self.commands)

    def is_valid_phone(self, phone):
        # Перевірка правильності формату номера телефону
        # Допустимі формати: +380501234567, 050-123-45-67, 0501234567, (050)123-45-67
        phone_pattern = re.compile(
            r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
        return bool(re.match(phone_pattern, phone))

    def is_valid_email(self, email):
        # Перевірка правильності формату електронної пошти
        email_pattern = re.compile(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))

    def add_contact_from_console(self):
        console.print("[bold]Додавання нового контакту:[/bold]")

        name = input("Ім'я: ")
        address = input("Адреса: ")
        phone = input("Телефон: ")
        email = input("Електронна пошта: ")
        birthday = input("Дата народження (день-місяць-рік): ")

        # Перевірка правильності формату номера телефону та електронної пошти
        if not self.is_valid_phone(phone):
            console.print(
                "[bold red]Помилка:[/bold red] Некоректний номер телефону.")
            return

        if not self.is_valid_email(email):
            console.print(
                "[bold red]Помилка:[/bold red] Некоректна електронна пошта.")
            return

        # Перевірка наявності контакту з таким номером телефону в книзі контактів
        existing_contact = next(
            (contact for contact in self.contacts if contact.phone == phone), None)

        if existing_contact:
            console.print(
                f"[bold red]Помилка:[/bold red] Контакт з номером телефону {phone} вже існує.")
            return

        # Додавання нового контакту до книги контактів
        new_contact = Contact(name, address, phone, email, birthday)

        self.contacts.append(new_contact)
        console.print(
            f"[green]Контакт {name} успішно доданий до книги контактів.[/green]")

    def dump(self):
        with open('addressbook.csv', 'w', newline='\n') as fh:
            field_names = ['name', 'address',
                           'phone', 'email', 'birth_date']
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            print(str(self.contacts))
            for contact in self.contacts:
                writer.writerow({'name': contact.name, 'address': contact.address,
                                 'phone': contact.phone, 'email': contact.email, 'birth_date': contact.birthday})

    def load(self):
        with open('addressbook.csv', newline='\n') as fh:
            reader = csv.DictReader(fh)
            address_book_disk = list()
            for row in reader:
                if row['name'] in self.names:
                    continue
                else:
                    name = row['name']
                    address = row['address']
                    phone = row['phone']
                    email = row['email']
                    birthday = row['birth_date']
                    new_contact = Contact(
                        name, address, phone, email, birthday)
                    self.contacts.append(new_contact)
            self.contacts = self.contacts + address_book_disk
            if self.contacts != []:
                print(str(self.contacts))

    def list_contacts(self):
        # Виведення списку контактів
        if not self.contacts:
            console.print("[red]У вас немає жодних контактів в книзі.[/red]")
        else:
            table = Table(title="Список контактів")
            table.add_column("[blue]Ім'я[/blue]")
            table.add_column("[green]Адреса[/green]")
            table.add_column("[yellow]Телефон[/yellow]")
            table.add_column("[cyan]Електронна пошта[/cyan]")
            table.add_column("[magenta]День народження[/magenta]")

            for contact in self.contacts:
                table.add_row(
                    Text(contact['name'], style="blue"),
                    Text(contact['address'], style="green"),
                    Text(contact['phone'], style="yellow"),
                    Text(contact['email'], style="cyan"),
                    Text(contact['birthday'], style="magenta")
                )

            console.print(table)

    def display_contacts(self):
        if not self.contacts:
            print('There are no contacts added.')
        else:
            table_format = "| {:<15} | {:<20} | {:<15} | {:<25} | {:<15} |"
            table_header = table_format.format(
                "name", "address", "phone_number", "email", "birth date")
            table_line = "-" * len(table_header)
            print("\n".join([table_line, table_header, table_line]))
            for contact in self.contacts:
                print(str(contact))
                print(table_line)

    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        upcoming_birthdays = [contact for contact in self.contacts if today <
                              self.get_next_birthday(contact) <= today + timedelta(days)]
        if not upcoming_birthdays:
            print(f'There are no upcoming birthdays in {days} days.')
        else:
            print(f'Upcoming birthdays in {days} days: ')
            for contact in upcoming_birthdays:
                remaining_days = (self.get_next_birthday(contact) - today).days
                print(
                    f"Name: {contact.name}, Birth date: {self.get_next_birthday(contact).strftime('%d.%m.%Y')}, Remaining days: {remaining_days}")

    def get_next_birthday(self, contact):
        today = datetime.today().date()
        next_birthday = contact.birth_date.replace(year=today.year)
        if today > datetime(today.year, next_birthday.month, next_birthday.day).date():
            next_birthday = next_birthday.replace(year=today.year + 1)
        return next_birthday

    def search_contacts(self, query=None):
        if query is None:
            query = input("Введіть запит для пошуку контактів: ")

        matching_contacts = [
            contact for contact in self.contacts if query.lower() in contact['name'].lower()]

        if matching_contacts:
            console.print(f"[bold green]Результати пошуку:[/bold green]")
            for contact in matching_contacts:
                console.print(contact)
        else:
            console.print(
                f"[red]Немає результатів пошуку для запиту: {query}[/red]")

        while True:
            user_input = input("Введіть команду: ")
            assistant.analyze_user_input(user_input)

            # Перевірка команд і виклики відповідних методів
            if "додати контакт" in user_input.lower():
                assistant.add_contact_from_console()
            elif "список контактів" in user_input.lower():
                assistant.list_contacts()
            elif "пошук контактів" in user_input.lower():
                assistant.search_contacts()
            elif "дн" in user_input.lower():
                assistant.upcoming_birthdays()
            else:
                console.print(
                    "[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")

    def edit_contact(self, contact_index, name, address, phone, email, birthday):
        # Редагування контакту
        pass

    def delete_contact(self, contact_index):
        # Видалення контакту
        pass

    def add_note(self, text, tags):
        # Додавання нової нотатки
        pass

    def list_notes(self):
        # Виведення списку нотаток
        pass

    def search_notes(self, query):
        # Пошук нотаток за запитом
        pass

    def edit_note(self, note_index, text, tags):
        # Редагування нотатки
        pass

    def delete_note(self, note_index):
        # Видалення нотатки
        pass

    def sort_notes_by_tags(self):
        # Сортування нотаток за тегами
        pass

    def categorize_files(self, folder_path):
        # Сортування файлів у зазначеній папці за категоріями
        pass

    def analyze_user_input(self, user_input):
        normalized_input = user_input.lower()
        if "додати контакт" in normalized_input:
            console.print(
                "[green]Пропоную вам додати новий контакт. Використайте команду add_contact.[/green]")
        elif "список контактів" in normalized_input:
            console.print(
                "[green]Для виведення списку контактів використайте команду list_contacts.[/green]")
        elif "пошук контактів" in normalized_input:
            console.print(
                "[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif 'дні народження' in normalized_input or 'дн' in normalized_input:
            console.print(
                "[green]Для виведення днів народження використайте команду birthday.[/green]")
        else:
            console.print(
                "[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")


assistant = PersonalAssistant()
assistant.load()

while True:
    user_input = input("Введіть команду: ")

    # Перевірка команд і виклик відповідного методу
    if user_input == 'exit' or user_input == 'вихід':
        assistant.dump()
        break
    elif "add" in user_input.lower() or "add_contact" in user_input.lower():
        assistant.add_contact_from_console()
    elif "list" in user_input.lower() or "list_contacts" in user_input.lower():
        assistant.list_contacts()
    elif "display" in user_input.lower() or "display_contacts" in user_input.lower():
        assistant.display_contacts()
    elif "search" in user_input.lower() or "search_contacts" in user_input.lower():
        assistant.search_contacts()
    elif "birthday" in user_input.lower():
        assistant.upcoming_birthdays()
    else:
        console.print(
            "[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")
        assistant.analyze_user_input(user_input)
