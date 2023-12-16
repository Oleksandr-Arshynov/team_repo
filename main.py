from datetime import datetime, date, timedelta
from rich.console import Console
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate
from rich.table import Table
from rich.text import Text
from dateutil import parser

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
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження', 
                         'додати нотатку', 'пошук нотаток', 'видалити нотатку', 'список нотаток', 
                         'редагувати нотатку', 'сортувати нотатки']

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

    def add_contact_from_console(self):
        console.print("[bold]Додавання нового контакту:[/bold]")

        name = input("Ім'я: ")
        address = input("Адреса: ")
        phone = input("Телефон: ")
        email = input("Електронна пошта: ")

        # Додатково: питаємо користувача про день народження і дозволяємо різні формати
        while True:
            try:
                birthday = input("Дата народження (день-місяць-рік): ")
                birthday_date = parser.parse(birthday).date()
                break  # Якщо парсинг відбувся успішно, виходимо з циклу
            except ValueError:
                console.print("[bold red]Помилка:[/bold red] Некоректний формат дати. Спробуйте ще раз.")

        self.add_contact(name, address, phone, email, birthday_date)

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
                # Перетворення дати народження в рядок
                birthday_str = contact['birthday'].strftime('%d-%m-%Y')
                
                table.add_row(
                    Text(contact['name'], style="blue"),
                    Text(contact['address'], style="green"),
                    Text(contact['phone'], style="yellow"),
                    Text(contact['email'], style="cyan"),
                    Text(birthday_str, style="magenta")
                )

            console.print(table)


    def upcoming_birthdays(self, days):
        today = datetime.today().date()
        upcoming_birthdays = [contact for contact in self.contacts if today < self.get_next_birthday(contact) <= today + timedelta(days)]
        if not upcoming_birthdays:
            console.print(f'[red]Немає наближених днів народження протягом {days} днів.[/red]')
        else:
            table = Table(title=f'Наближені дні народження протягом {days} днів')
            table.add_column("[blue]Ім'я[/blue]")
            table.add_column("[magenta]День народження[/magenta]")
            table.add_column("[green]Залишилось днів[/green]")
            table.add_column("[cyan]Вік[/cyan]")

            for contact in upcoming_birthdays:
                remaining_days = (self.get_next_birthday(contact) - today).days
                age = today.year - contact['birthday'].year - ((today.month, today.day) < (contact['birthday'].month, contact['birthday'].day))
                table.add_row(
                    Text(contact['name'], style="blue"),
                    Text(self.get_next_birthday(contact).strftime('%d.%m.%Y'), style="magenta"),
                    Text(str(remaining_days), style="green"),
                    Text(str(age), style="cyan")
                )

            console.print(table)
   

    def get_next_birthday(self, contact):
        today = datetime.today().date()

        # Перевірка, чи birth_date є рядком, і якщо так, конвертувати його у datetime.date
        if isinstance(contact['birthday'], str):
            birth_date = datetime.strptime(contact['birthday'], "%d-%m-%Y").date()
        else:
            birth_date = contact['birthday']

        next_birthday = birth_date.replace(year=today.year)

        if today > date(today.year, birth_date.month, birth_date.day):
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
        new_note = Note(text, tags)
        self.notes.append(new_note)
        console.print(f"[green]Нотатка успішно додана.[/green]")

    def add_notes_from_console(self):
        console.print("[bold]Додавання нових нотаток:[/bold]")

        while True:
            text = input("Текст нотатки (або введіть 'закінчити' для завершення): ")
            if text.lower() == 'закінчити':
                break

            tags = input("Теги (розділіть їх комою): ").split(',')
            self.add_note(text, tags)

    def list_notes(self):
        # Виведення списку нотаток
        if not self.notes:
            console.print("[red]У вас немає жодних нотаток.[/red]")
        else:
            table = Table(title="Список нотаток")
            table.add_column("[blue]Текст[/blue]")
            table.add_column("[cyan]Теги[/cyan]")

            for note in self.notes:
                table.add_row(
                    Text(note.text, style="blue"),
                    Text(", ".join(note.tags), style="cyan")
                )

            console.print(table)

    def search_notes(self, query):
        # Пошук нотаток за запитом
        matching_notes = [note for note in self.notes if query.lower() in note.text.lower()]

        if matching_notes:
            console.print(f"[bold green]Результати пошуку:[/bold green]")
            for note in matching_notes:
                console.print(note.text)
        else:
            console.print(f"[red]Немає результатів пошуку для запиту: {query}[/red]")

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
        elif "дн" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "додати нотатку" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "список нотаток" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "редагувати нотатку" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "сортувати нотатки" in normalized_input:
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
    elif "пошук нотаток" in user_input.lower():
        query = input("Введіть запит для пошуку нотаток: ")
        assistant.search_notes(query)
    elif "додати нотатку" in user_input.lower():
        assistant.add_notes_from_console()
    elif "видалити нотатку" in user_input.lower():
        assistant.delete_note_note()
    elif "список нотаток" in user_input.lower():
        assistant.list_notes()    
    elif "редагувати нотатку" in user_input.lower():
        assistant.edit_note()
    elif "сортувати нотатки" in user_input.lower():
        assistant.sort_notes_by_tags() 
      
    else:
        console.print("[red]Не можу розпізнати вашу команду. Спробуйте ще раз.[/red]") 
    #додати нотатку', 'пошук нотаток', 'видалити нотатку', 'список нотаток', 
    #'редагувати нотатку', 'сортувати нотатки'