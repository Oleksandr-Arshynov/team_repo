from datetime import datetime, date, timedelta
from rich.console import Console
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate
from rich.table import Table
from rich.text import Text
from dateutil import parser
from rich.live import Live
import csv

console = Console()

class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
            
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
                    birthday_str = contact.birthday.strftime('%d-%m-%Y')

                    table.add_row(
                        Text(contact.name, style="blue"),
                        Text(contact.address, style="green"),
                        Text(contact.phone, style="yellow"),
                        Text(contact.email, style="cyan"),
                        Text(birthday_str, style="magenta")
                    )

                # Встановлення відстані від верхнього краю екрану
                console.print("\n" * 10)
                console.print(table, justify="center")
                
    def dump(self):
            with open('addressbook.csv', 'w', newline='\n') as fh:
                field_names = ['name', 'address',
                            'phone', 'email', 'birthday']
                writer = csv.DictWriter(fh, fieldnames=field_names)
                writer.writeheader()
                print(str(self.contacts))
                for contact in self.contacts:
                    writer.writerow({'name': contact.get('name'), 'address': contact.get('address'),
                                    'phone': contact.get('phone'), 'email': contact.get('email'), 'birthday': contact.get('birthday')})

    def load(self):
        with open('addressbook.csv', newline='\n') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                name = row['name']
                address = row['address']
                phone = row['phone']
                email = row['email']
                
                # Перетворення рядка дати у об'єкт datetime.date
                birthday_str = row['birthday']
                birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                
                new_contact = Contact(
                    name, address, phone, email, birthday)
                self.contacts.append(new_contact)

        if self.contacts:
            print("Контакти успішно завантажені.")
        else:
            print("Не вдалося завантажити контакти або файл порожній.")
            
    def upcoming_birthdays(self, days):
            today = datetime.today().date()
            upcoming_birthdays = [contact for contact in self.contacts if today < self.get_next_birthday(contact) <= today + timedelta(days)]
            if not upcoming_birthdays:
                console.print(f'[yellow]У {days} днів немає найближчих днів народження.[/yellow]')
            else:
                table = Table(title=f'Дні народження у наступні {days} днів')
                table.add_column("[blue]Ім'я[/blue]")
                table.add_column("[magenta]Дата народження[/magenta]")
                table.add_column("[yellow]Залишилося днів[/yellow]")
                table.add_column("[green]Вік[/green]")

                for contact in upcoming_birthdays:
                    remaining_days = (self.get_next_birthday(contact) - today).days
                    birthday_str = contact['birthday'].strftime('%d-%m-%Y')

                    age = today.year - contact['birthday'].year + 1 - ((today.month, today.day) < (contact['birthday'].month, contact['birthday'].day))

                    table.add_row(
                    Text(contact['name'], style="blue"),
                    Text(birthday_str, style="magenta"),
                    Text(str(remaining_days), style="yellow"),
                    Text(str(age), style="green")
                    )
                # Встановлення відстані від верхнього краю екрану
                console.print("\n" * 10)
                console.print(table, justify="center")

    def get_next_birthday(self, contact):
            today = datetime.today().date()

            # Перевірка, чи birthday є рядком, і якщо так, конвертувати його у datetime.date
            if isinstance(contact['birthday'], str):
                birthday = datetime.strptime(contact['birthday'], "%d-%m-%Y").date()
            else:
                birthday = contact['birthday']

            next_birthday = birthday.replace(year=today.year)

            if today > date(today.year, birthday.month, birthday.day):
                next_birthday = next_birthday.replace(year=today.year + 1)

            return next_birthday
        
    def search_contacts(self, query=None):
            if query is None:
                query = input("Введіть запит для пошуку контактів: ")

            matching_contacts = [contact for contact in self.contacts if query.lower() in contact.name.lower()]

            if matching_contacts:
                console.print(f"[bold green]Результати пошуку:[/bold green]")

                # Виведення знайдених контактів в таблицю
                table = Table(title="Знайдені контакти")
                table.add_column("[blue]Ім'я[/blue]", justify="center")
                table.add_column("[green]Адреса[/green]", justify="center")
                table.add_column("[yellow]Телефон[/yellow]", justify="center")
                table.add_column("[cyan]Електронна пошта[/cyan]", justify="center")
                table.add_column("[magenta]День народження[/magenta]", justify="center")

                for contact in matching_contacts:
                    table.add_row(
                        Text(contact.name, style="blue"),
                        Text(contact.address, style="green"),
                        Text(contact.phone, style="yellow"),
                        Text(contact.email, style="cyan"),
                        Text(contact.birthday.strftime('%d-%m-%Y'), style="magenta")
                    )

                # Центрування таблиці
                console.print(table, justify="center")

                # Повернення першого знайденого контакту
                return matching_contacts[0] if matching_contacts else None
            else:
                console.print(f"[red]Немає результатів пошуку для запиту: {query}[/red]")
                return None

    def edit_contact(self, contact):
        if contact is None:
            console.print("[bold red]Помилка:[/bold red] Контакт не знайдено.")
            return

        console.print(f"[bold]Редагування контакту: {contact.name}[/bold]")

        # Редагування імені
        new_name = input(f"Теперішнє ім'я: {contact.name}\nВведіть нове ім'я (або Enter, щоб залишити без змін): ")
        if new_name:
            contact.name = new_name

        # Редагування адреси
        new_address = input(f"Теперішня адреса: {contact.address}\nВведіть нову адресу (або Enter, щоб залишити без змін): ")
        if new_address:
            contact.address = new_address

        # Редагування номеру телефону
        new_phone = input(f"Теперішній телефон: {contact.phone}\nВведіть новий телефон (або Enter, щоб залишити без змін): ")
        if new_phone:
            if self.is_valid_phone(new_phone):
                contact.phone = new_phone
            else:
                console.print("[bold red]Помилка:[/bold red] Некоректний номер телефону.")

        # Редагування пошти
        new_email = input(f"Теперішня електронна пошта: {contact.email}\nВведіть нову пошту (або Enter, щоб залишити без змін): ")
        if new_email:
            if self.is_valid_email(new_email):
                contact.email = new_email
            else:
                console.print("[bold red]Помилка:[/bold red] Некоректна електронна пошта.")

        # Редагування дня народження
        new_birthday = input(f"Теперішній день народження: {contact.birthday}\nВведіть новий день народження (або Enter, щоб залишити без змін): ")
        if new_birthday:
            contact.birthday = new_birthday

        console.print(f"[green]Контакт {contact.name} успішно відредаговано.[/green]")


        # Видалення контакту
    def delete_contact(self, contact=None):
        if contact is None:
            # Якщо contact не передано, спробуйте викликати search_contacts для вибору контакту
            contact = self.search_contacts()

        if contact in self.contacts:
            contact_name = contact.name
            self.contacts.remove(contact)
            console.print(f"[green]Контакт {contact_name} успішно видалено.[/green]")
        else:
            console.print("[red]Error: Контакт не знайдено або не вибрано для видалення.[/red]")