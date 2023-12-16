
from rich.console import Console

console = Console()

class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження', 'редагувати контакт', 'видалити контакт', 'видалити нотатки' ]

        # Редагування контакту
    def edit_contact(self, contact_index, name=None, address=None, phone=None, email=None, birthday=None):
        if contact_index < len(self.contacts):
            print("Введіть нові дані або натисніть Enter, щоб залишити старі дані.")
            # Редагування імені
            if name is not None:
                new_name = input("Введіть нове ім'я:")
                if new_name != "":
                    self.contacts[contact_index]['name'] = new_name
                    while True:
                        choice = input("Продовжити редагування? (так/ні): ").lower()
                        if choice == 'ні':
                            return
                        elif choice == 'так':
                            break
                        else:
                            print("Будь ласка, введіть 'так' або 'ні'.")
            # Редагування адреси        
            if address is not None:
                print("Введіть нові дані або натисніть Enter, щоб залишити старі дані.")
                new_address = input("Введіть нову адресу: ")
                if new_address != "":
                    self.contacts[contact_index]['address'] = new_address
                    while True:
                        choice = input("Продовжити редагування? (так/ні): ").lower()
                        if choice == 'ні':
                            return
                        elif choice == 'так':
                            break
                        else:
                            print("Будь ласка, введіть 'так' або 'ні'.")
            # Редагування номеру телефону
            if phone is not None:
                print("Введіть нові дані або натисніть Enter, щоб залишити старі дані.")
                new_phone = input("Введіть новий телефон контакту: ")
                if new_phone != "":
                    if self.is_valid_phone(new_phone):
                        self.contacts[contact_index]['phone'] = new_phone
                        while True:
                            choice = input("Продовжити редагування? (так/ні): ").lower()
                            if choice == 'ні':
                                return
                            elif choice == 'так':
                                break
                            else:
                                print("Будь ласка, введіть 'так' або 'ні'.")
                    else:
                        console.print("Error: Некоректний номер телефону.")
            # Редагування пошти             
            if email is not None:
                print("Введіть нові дані або натисніть Enter, щоб залишити старі дані.")
                new_email = input("Введіть нову пошту: ")
                if new_email != "":
                    if self.is_valid_email(email):
                        self.contacts[contact_index]['email'] = new_email
                        while True:
                            choice = input("Продовжити редагування? (так/ні): ").lower()
                            if choice == 'ні':
                                return
                            elif choice == 'так':
                                break
                            else:
                                print("Будь ласка, введіть 'так' або 'ні'.")
                    else:
                        console.print("Error: Некоректна електронна пошта.")
            # Редагування дня народження
            if birthday is not None:
                print("Введіть нові дані або натисніть Enter, щоб залишити старі дані.")
                new_birthday = input("Введіть новий день народження: ")
                if new_birthday != "":
                    self.contacts[contact_index]['birthday'] = new_birthday
            console.print(f"[green]Контакт {self.contacts[contact_index]['name']} успішно відредаговано.[/green]")
        else:
            console.print("[red]Error: Контакт з таким індексом не існує.[/red]")

        # Видалення контакту
    def delete_contact(self, contact_index):
        if contact_index < len(self.contacts):
            deleted_contact = self.contacts.pop(contact_index)
            console.print(f"[green]Контакт {deleted_contact['name']} успішно видалено.[/green]")
        else:
            console.print("[red]Error: Контакт з таким індексом не існує.[/red]")


    def delete_note(self, note_index):
        # Видалення нотатки
        if note_index < len(self.notes):
            deleted_note = self.notes.pop(note_index)
            console.print(f"[green]Нотаток {deleted_note['name']} успішно видалений.[/green]")
        else:
            console.print("[red]Error: нотаток з таким індексом не існує.[/red]")


    def analyze_user_input(self, user_input):
        normalized_input = user_input.lower()
        if "додати контакт" in normalized_input:
            console.print("[green]Пропоную вам додати новий контакт. Використайте команду add_contact.[/green]")
        elif "список контактів" in normalized_input:
            console.print("[green]Для виведення списку контактів використайте команду list_contacts.[/green]")
        elif "пошук контактів" in normalized_input:
            console.print("[green]Ви можете використовувати команду search_contacts для пошуку контактів.[/green]")
        elif "редагувати контакт" in normalized_input:
            console.print("[blue]Для редагування контактів використайте команду edit_contact.[/blue]")
        elif "видалити контакт" in normalized_input:
            console.print("[blue]Для видалення контактів використайте команду delete_contact_contact.[/blue]")


assistant = PersonalAssistant()

while True:
    user_input = input("Введіть команду: ")
    assistant.analyze_user_input(user_input)
    if "вихід" in user_input.lower():
        break
    
    # Перевірка команд і виклик відповідного методу

    elif "редагувати контакт" in user_input.lower():
        contact_index = int(input("Введіть індекс контакту, який ви хочете редагувати. Наприклад 0: "))
        assistant.edit_contact(contact_index, name="Нове ім'я", address="Нова адреса", phone="Новий телефон", email="Нова пошта", birthday="Новий день народження")
    elif "видалити контакт" in user_input.lower():
        contact_index = int(input("Введіть індекс контакту, який ви хочете видалити: "))
        assistant.delete_contact(contact_index)
    elif "видалити нотатки" in user_input.lower():
        note_index = int(input("Введіть індекс нотатку, який ви хочете видалити: "))
        assistant.delete_note(note_index)


      