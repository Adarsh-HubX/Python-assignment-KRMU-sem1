# --------------------------------------------------------------------
# Name        : Adarsh Rathore
# Roll No     : <2501410014>
# Course      : B.Tech CSE (Cyber Security)
# Semester    : 1st Semester
# Subject     : Programming for Problem Solving Using Python
# File        : main.py
# Project     : Library Inventory Manager
# --------------------------------------------------------------------


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_manager.inventory import LibraryInventory
from library_manager.book import Book


def main():
    inv = LibraryInventory()
    
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Search by Title")
        print("5. Search by ISBN")
        print("6. Show All Books")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")

            try:
                book = Book(title, author, isbn)
                inv.add_book(book)
                print("Book added successfully!")
            except Exception as e:
                print("Error: ", e)
            
        elif choice == "2":   
            isbn = input("Enter ISBN to issue: ")
            book = inv.search_isbn(isbn)

            if book:
                if book.status == "available":
                    book.issue()
                    inv.save_data()
                    print("Book issued!")
                else:
                    print("Book already issued.")
            else:
                print("Book not found.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inv.search_isbn(isbn)

            if book:
                if book.status == "issued":
                    book.return_book()
                    inv.save_data()
                    print("Book returned!")
                else:
                    print("Book is not issued.")
            else:
                print("Book not found.")

        elif choice == "4":
            title = input("Enter title to search: ")
            books = inv.search_title(title)

            if books:
                for b in books:
                    print(b)
            else:
                print("No books found.")

        elif choice == "5":
            isbn = input("Enter ISBN to search: ")
            book = inv.search_isbn(isbn)

            if book:
                print(book)
            else:
                print("Book not found.")

        elif choice == "6":
            all_books = inv.show_all()
            for b in all_books:
                print(b)

        elif choice == "7":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
