from datetime import datetime, timedelta
from rich.console import Console
import re
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

class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження']

        # Встановлення автодоповнення на основі доступних команд
        self.command_completer = WordCompleter(self.commands)

    def is_valid_phone(self, phone):
        # Перевірка правильності формату номера телефону
        # Допустимі формати: +380501234567, 050-123-45-67, 0501234567, (050)123-45-67
        phone_pattern = re.compile(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
        return bool(re.match(phone_pattern, phone))

    def is_valid_email(self, email):
        # Перевірка правильності формату електронної пошти
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))

    def add_contact(self, name, address, phone, email, birthday):
        # Перевірка правильності формату номера телефону та електронної пошти
        if not self.is_valid_phone(phone):
            console.print("[bold red]Помилка:[/bold red] Некоректний номер телефону.")
            return

        if not self.is_valid_email(email):
            console.print("[bold red]Помилка:[/bold red] Некоректна електронна пошта.")
            return

        # Перевірка наявності контакту з таким номером телефону в книзі контактів
        existing_contact = next((contact for contact in self.contacts if contact['phone'] == phone), None)

        if existing_contact:
            console.print(f"[bold red]Помилка:[/bold red] Контакт з номером телефону {phone} вже існує.")
            return

        # Додавання нового контакту до книги контактів
        new_contact = {
            'name': name,
            'address': address,
            'phone': phone,
            'email': email,
            'birthday': birthday
        }

        self.contacts.append(new_contact)
        console.print(f"[green]Контакт {name} успішно доданий до книги контактів.[/green]")
        
    def add_contact_from_console(self):
            console.print("[bold]Додавання нового контакту:[/bold]")

            name = input("Ім'я: ")
            address = input("Адреса: ")
            phone = input("Телефон: ")
            email = input("Електронна пошта: ")
            birthday = input("Дата народження (день-місяць-рік): ")

            self.add_contact(name, address, phone, email, birthday)
            
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


    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        upcoming_birthdays = [contact for contact in self.contacts if today < self.get_next_birthday(contact) <= today + timedelta(days)]
        if not upcoming_birthdays:
            print(f'There are no upcoming birthdays in {days} days.')
        else:
            print(f'Upcoming birthdays in {days} days: ')
            for contact in upcoming_birthdays:
                remaining_days = (self.get_next_birthday(contact) - today).days
                print(f"Name: {contact.name}, Birth date: {self.get_next_birthday(contact).strftime('%d.%m.%Y')}, Remaining days: {remaining_days}")

    def get_next_birthday(self, contact):
        today = datetime.today().date()
        next_birthday = contact.birth_date.replace(year=today.year)
        if today > datetime(today.year, next_birthday.month, next_birthday.day).date():
            next_birthday = next_birthday.replace(year=today.year + 1)
        return next_birthday


    def search_contacts(self, query=None):
        if query is None:
            query = input("Введіть запит для пошуку контактів: ")

        matching_contacts = [contact for contact in self.contacts if query.lower() in contact['name'].lower()]
        
        if matching_contacts:
            console.print(f"[bold green]Результати пошуку:[/bold green]")
            for contact in matching_contacts:
                console.print(contact)
        else:
            console.print(f"[red]Немає результатів пошуку для запиту: {query}[/red]")

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
                assistant.upcoming_birthdays(7)
            else:
                console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")

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
        if 0 <= note_index < len(self.notes):
            # Оновлення нотатки із зазначеним індексом
            self.notes[note_index].text = text
            self.notes[note_index].tags = tags
            console.print(f"[green]Нотатка {note_index} успішно відредагована.[/green]")
        else:
            console.print("[bold red]Помилка:[/bold red] Невірний індекс нотатки.")

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
            console.print("[green]Пропоную вам додати новий контакт. Використайте команду add_contact.[/green]")
        elif "список контактів" in normalized_input:
            console.print("[green]Для виведення списку контактів використайте команду list_contacts.[/green]")
        elif "пошук контактів" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        else:
            console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")

assistant = PersonalAssistant()

while True:
    user_input = input("Введіть команду: ")
    assistant.analyze_user_input(user_input)

    # Перевірка команд і виклик відповідного методу
    if "додати контакт" in user_input.lower():
        assistant.add_contact_from_console()
    elif "список контактів" in user_input.lower():
        assistant.list_contacts()
    elif "пошук контактів" in user_input.lower():
        assistant.search_contacts()
    elif "дні народження" in user_input.lower():
        assistant.upcoming_birthdays(7)
    else:
        console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]") 
      