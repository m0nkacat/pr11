import os
from abc import ABC, abstractmethod

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
    
    def __str__(self):
        return f"{self.title} ({self.author})"


class Person(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def get_info(self):
        pass


class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.borrowed_books = []
    
    def get_info(self):
        return f"Книг на руках: {len(self.borrowed_books)}"
    
    def take_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book.title)
            return True
        return False
    
    def return_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            return True
        return False


class Librarian(Person):
    def get_info(self):
        return "Библиотекарь"


class Library:
    def __init__(self):
        self._books = []
        self._users = {}
        self._librarians = set()
        self.load_data()
    
    def add_book(self, title, author):
        if not any(b.title == title for b in self._books):
            self._books.append(Book(title, author))
            return True
        return False
    
    def remove_book(self, title):
        book = self.find_book(title)
        if book and book.available:
            self._books.remove(book)
            return True
        return False
    
    def get_available_books(self):
        return [b for b in self._books if b.available]
    
    def get_all_books(self):
        return self._books
    
    def find_book(self, title):
        for book in self._books:
            if book.title == title:
                return book
        return None
    
    def register_user(self, name):
        if name not in self._users:
            self._users[name] = User(name)
            return True
        return False
    
    def get_user(self, name):
        return self._users.get(name)
    
    def get_all_users(self):
        return list(self._users.values())
    
    def is_librarian(self, name):
        return name in self._librarians
    
    def register_librarian(self, name):
        self._librarians.add(name)
    
    def save_data(self):
        with open('books.txt', 'w', encoding='utf-8') as f:
            for book in self._books:
                f.write(f"{book.title}|{book.author}|{book.available}\n")
        
        with open('users.txt', 'w', encoding='utf-8') as f:
            for user in self._users.values():
                books = ','.join(user.borrowed_books)
                f.write(f"{user.name}|{books}\n")
    
    def load_data(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        title, author, available = parts
                        book = Book(title, author)
                        book.available = available == 'True'
                        self._books.append(book)
        
        if os.path.exists('users.txt'):
            with open('users.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        name, borrowed = parts
                        user = User(name)
                        if borrowed:
                            user.borrowed_books = borrowed.split(',')
                        for book_title in user.borrowed_books:
                            book = self.find_book(book_title)
                            if book:
                                book.available = False
                        self._users[name] = (user)


library = Library()

library.register_librarian("админ")
library.register_librarian("библиотекарь")


while True:
    print("Главное меню")
    print("1. Войти как библиотекарь")
    print("2. Войти как читатель")
    print("3. Выход")
    
    choice = input("> ")
    
    if choice == '1':
        name = input("Введите имя: ")
        if library.is_librarian(name):
            librarian = Librarian(name)
            print(f"{librarian.name} ({librarian.get_info()})")
            
            while True:
                print("\n1. Добавить книгу")
                print("2. Удалить книгу")
                print("3. Добавить читателя")
                print("4. Список читателей")
                print("5. Список всех книг")
                print("6. Назад")
                
                choice = input("> ")
                
                if choice == '1':
                    title = input("Название: ")
                    author = input("Автор: ")
                    if library.add_book(title, author):
                        print(" Книга добавлена")
                    else:
                        print(" Книга уже есть")
                
                elif choice == '2':
                    title = input("Название: ")
                    if library.remove_book(title):
                        print(" Книга удалена")
                    else:
                        print(" Не удалось удалить")
                
                elif choice == '3':
                    name = input("Имя читателя: ")
                    if library.register_user(name):
                        print("Читатель добавлен")
                    else:
                        print("Читатель уже есть")
                
                elif choice == '4':
                    users = library.get_all_users()
                    if users:
                        for user in users:
                            print(f"- {user.name} ({user.get_info()})")
                    else:
                        print("Нет читателей")
                
                elif choice == '5':
                    books = library.get_all_books()
                    if books:
                        for i, book in enumerate(books, 1):
                            status = "свободна" if book.available else "выдана"
                            print(f"{i}. {book} - {status}")
                    else:
                        print("Нет книг")
                
                elif choice == '6':
                    break
        else:
            print("Доступ запрещен")
    
    elif choice == '2':
        name = input("Введите имя: ")
        user = library.get_user(name)
        
        if not user:
            print("Новый читатель. Регистрирую...")
            library.register_user(name)
            user = library.get_user(name)
        
        print(f" {user.name} ({user.get_info()})")
        
        while True:
            print("\n1. Доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("5. Назад")
            
            choice = input("> ")
            
            if choice == '1':
                books = library.get_available_books()
                if books:
                    for i, book in enumerate(books, 1):
                        print(f"{i}. {book}")
                else:
                    print("Нет свободных книг")
            
            elif choice == '2':
                title = input("Название книги: ")
                book = library.find_book(title)
                if book:
                    if user.take_book(book):
                        print("Книга выдана")
                    else:
                        print("Книга уже занята")
                else:
                    print("Книга не найдена")
            
            elif choice == '3':
                if user.borrowed_books:
                    print("Ваши книги:", ", ".join(user.borrowed_books))
                    title = input("Какую вернуть: ")
                    if user.return_book(title):
                        book = library.find_book(title)
                        if book:
                            book.available = True
                        print("Книга возвращена")
                    else:
                        print("У вас нет этой книги")
                else:
                    print("У вас нет книг")
            
            elif choice == '4':
                if user.borrowed_books:
                    for i, title in enumerate(user.borrowed_books, 1):
                        print(f"{i}. {title}")
                else:
                    print("У вас нет книг")
            
            elif choice == '5':
                break
    
    elif choice == '3':
        library.save_data()
        print("Данные сохранены. До свидания!")
        break