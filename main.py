import os
import pickle
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def __str__(self):
        return f"{self.title} ({self.author})".lower()


class Person(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def poluchit_info(self):
        pass


class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.borrowed_books = []

    def poluchit_info(self):
        return f"Книг на руках: {len(self.borrowed_books)}".lower()

    def vzyat_knigu(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book.title)
            return True
        return False

    def vernut_knigu(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            return True
        return False


class Librarian(Person):
    def poluchit_info(self):
        return "Библиотекарь".lower()


class Library:
    def __init__(self):
        self._books = []
        self._users = {}
        self._librarians = set()

    def dobavit_knigu(self, title, author):
        if not any(b.title == title for b in self._books):
            self._books.append(Book(title, author))
            return True
        return False

    def udalit_knigu(self, title):
        book = self.nayti_knigu(title)
        if book and book.available:
            self._books.remove(book)
            return True
        return False

    def dostupnye_knigi(self):
        return [b for b in self._books if b.available]

    def vse_knigi(self):
        return self._books

    def nayti_knigu(self, title):
        for book in self._books:
            if book.title == title:
                return book
        return None

    def registrirovat_usera(self, name):
        if name not in self._users:
            self._users[name] = User(name)
            return True
        return False

    def poluchit_usera(self, name):
        return self._users.get(name)

    def vse_usery(self):
        return list(self._users.values())

    def eto_librarian(self, name):
        return name in self._librarians

    def registrirovat_librarian(self, name):
        self._librarians.add(name)

    def sohranit_dannye(self):
        with open('library.pkl', 'wb') as f:
            pickle.dump(self, f)


def zagruzit_library():
    if os.path.exists('library.pkl'):
        try:
            with open('library.pkl', 'rb') as f:
                return pickle.load(f)
        except Exception:
            print("Ошибка загрузки, создается новая библиотека")
    return Library()


library = zagruzit_library()

library.registrirovat_librarian("админ")
library.registrirovat_librarian("библиотекарь")

SECRET_CODE = "1234"
main_running = True

while main_running:
    print("1. Библиотекарь")
    print("2. Читатель")
    print("3. Зарегистрировать библиотекаря")
    print("4. Выход")

    choice = input("> ")

    if choice == '1':
        name = input("Имя: ")

        if library.eto_librarian(name):
            librarian_running = True

            while librarian_running:
                print("1. Добавить книгу")
                print("2. Удалить книгу")
                print("3. Добавить читателя")
                print("4. Список читателей")
                print("5. Список книг")
                print("6. Назад")

                choice = input("> ")

                if choice == '1':
                    title = input("Название: ")
                    author = input("Автор: ")
                    if library.dobavit_knigu(title, author):
                        print("книга добавлена")
                    else:
                        print("книга уже существует")

                elif choice == '2':
                    title = input("Название: ")
                    if library.udalit_knigu(title):
                        print("книга удалена")
                    else:
                        print("удаление невозможно")

                elif choice == '3':
                    name = input("Имя читателя: ")
                    if library.registrirovat_usera(name):
                        print("читатель добавлен")
                    else:
                        print("читатель уже существует")

                elif choice == '4':
                    users = library.vse_usery()
                    for user in users:
                        print(f"{user.name} ({user.poluchit_info()})")

                elif choice == '5':
                    books = library.vse_knigi()
                    for book in books:
                        status = "свободна" if book.available else "выдана"
                        print(f"{book} - {status}")

                elif choice == '6':
                    librarian_running = False
        else:
            print("доступ запрещен")

    elif choice == '2':
        name = input("Имя: ")
        user = library.poluchit_usera(name)

        if not user:
            library.registrirovat_usera(name)
            user = library.poluchit_usera(name)

        user_running = True

        while user_running:
            print("1. Доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("5. Назад")

            choice = input("> ")

            if choice == '1':
                books = library.dostupnye_knigi()
                for book in books:
                    print(book)

            elif choice == '2':
                title = input("Название книги: ")
                book = library.nayti_knigu(title)
                if book and user.vzyat_knigu(book):
                    print("книга выдана")
                else:
                    print("книга недоступна")

            elif choice == '3':
                title = input("Название книги: ")
                if user.vernut_knigu(title):
                    book = library.nayti_knigu(title)
                    if book:
                        book.available = True
                    print("книга возвращена")
                else:
                    print("у вас нет этой книги")

            elif choice == '4':
                for title in user.borrowed_books:
                    print(title)

            elif choice == '5':
                user_running = False

    elif choice == '3':
        name = input("имя нового библиотекаря: ")
        code = input("введите код для регистрации: ")
        if code == SECRET_CODE:
            library.registrirovat_librarian(name)
            print("библиотекарь успешно зарегистрирован")
        else:
            print("неверный код")

    elif choice == '4':
        library.sohranit_dannye()
        print("данные сохранены")
        main_running = False