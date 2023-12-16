from datetime import datetime
from rich.console import Console
import re
# from prompt_toolkit import prompt
# from prompt_toolkit.completion import WordCompleter
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
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження', 'додати нотатку', 'список нотаток']

        # Встановлення автодоповнення на основі доступних команд
        #self.command_completer = WordCompleter(self.commands)

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
        current_date = datetime.now()
        upcoming_birthday_contacts = []

        for contact in self.contacts:
            birthday = datetime.strptime(contact['birthday'], "%d-%m-%Y")       # конвертуємо рядок 'birthday' в об'єкт datetime
            birthday = birthday.replace(year=current_date.year)                 # змінюємо рік народження на поточний рік
            days_until_birthday = (birthday - current_date).days + 1            # розраховуємо різницю між днем народження і сьогоднішнім днем

            if days_until_birthday < 0:                                         # перевіряємо якщо день народження вже був у цьому році
                birthday = birthday.replace(year=current_date.year + 1)
                days_until_birthday = (birthday - current_date).days

            if 0 <= days_until_birthday <= days:                                # перевіряємо чи день народження припадає на вказану кількість днів (days)
                upcoming_birthday_contacts.append({
                    'name': contact['name'],
                    'birthday': contact['birthday'],
                    'days_until_birthday': days_until_birthday
                })

        if upcoming_birthday_contacts:
            upcoming_birthday_contacts = sorted(upcoming_birthday_contacts, key=lambda x: x['days_until_birthday'])    # sorting upcoming birthdays by day
            table = Table(title=f"Дні народження впродовж наступних {days} дні(в)")
            table.add_column("[blue]Ім'я[/blue]")
            table.add_column("[magenta]День народження[/magenta]")
            table.add_column("[cyan]Днів до дня народження[/cyan]")

            for contact in upcoming_birthday_contacts:
                table.add_row(
                    Text(contact['name'], style="blue"),
                    Text(contact['birthday'], style="magenta"),
                    Text(str(contact['days_until_birthday']), style="cyan")
                )

            console.print(table)
        else:
            console.print(f"[green]Немає контактів з днем народження через {days} дні(в).[/green]")

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

        # Delete!!!
        # while True:
        #     user_input = input("Введіть команду: ")
        #     assistant.analyze_user_input(user_input)
        #
        #     # Перевірка команд і виклики відповідних методів
        #     if "додати контакт" in user_input.lower():
        #         assistant.add_contact_from_console()
        #     elif "список контактів" in user_input.lower():
        #         assistant.list_contacts()
        #     elif "пошук контактів" in user_input.lower():
        #         assistant.search_contacts()
        #     elif "дн" in user_input.lower():
        #         assistant.upcoming_birthdays(7)
        #     else:
        #         console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")

    def edit_contact(self, contact_index, name, address, phone, email, birthday):
        # Редагування контакту
        pass

    def delete_contact(self, contact_index):
        # Видалення контакту
        pass

    # To be done by Ivan
    def add_note(self, text=None, tags=None):                           # text and tags are not necessary
        text = input("Введіть нотатку: ")
        tags_input = input("Введіть теги через кому: ").split(', ')
        tags_list = [f"#{tag.strip()}" for tag in tags_input if tag.strip()]
        new_note = Note(text, tags_list)   # instant of Note class
        self.notes.append(new_note)
        console.print("[green]Нотатка додана.[/green]")

    # To be done by Andrii
    def list_notes(self):
        if not self.notes:
            console.print("[red]У вас немає жодних нотаток в книзі.[/red]")
        else:
            table = Table(title="Список нотаток")
            table.add_column("[blue]Номер[/blue]")
            table.add_column("[green]Текст[/green]")
            table.add_column("[red]Теги[/red]")

            for num, note in enumerate(self.notes, start=1):
                # converting list of tags into a string
                tags_str = ' '.join(note.tags)
                table.add_row(Text(str(num), style="blue"), Text(note.text, style="green"), Text(tags_str, style="red"))

            console.print(table)

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
            console.print("[green]Пропоную вам додати новий контакт. Використайте команду add_contact.[/green]")
        elif "список контактів" in normalized_input:
            console.print("[green]Для виведення списку контактів використайте команду list_contacts.[/green]")
        elif "пошук контактів" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "дні народження" in normalized_input:
            console.print("[green]Ви можете використовувати команду upcoming_birthdays для відображення майбутніх днів народжень.[/green]")
        elif "додати нотатку" in normalized_input:
            console.print("[green]Ви можете використовувати команду add_notes для додавання нотаток.[/green]")
        elif "список нотаток" in normalized_input:
            console.print("[green]Ви можете використовувати команду list_notes для виведення нотаток.[/green]")
        elif "вихід" in normalized_input:
            console.print("Дякую за користування персональним помічником. До побачення!")
        # To be removed!!!
        # else:
        #     console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")


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
        days = int(input("Введіть кількість днів: "))
        assistant.upcoming_birthdays(days)
    elif "додати нотатку" in user_input.lower():
        assistant.add_note()
    elif "список нотаток" in user_input.lower():
        assistant.list_notes()
    elif "вихід" in user_input.lower():
        break
    else:
        console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]")
