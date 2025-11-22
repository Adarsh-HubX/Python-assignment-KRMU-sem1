# --------------------------------------------------------------------
# Name        : Adarsh Rathore
# Roll No     : <2501410014>
# Course      : B.Tech CSE (Cyber Security)
# Semester    : 1st Semester
# Subject     : Programming for Problem Solving Using Python
# File        : main.py
# Project     : Library Inventory Manager
# --------------------------------------------------------------------


from library_manager.book import Book
import os
import json
import logging

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LibraryInventory:
    def __init__(self):
        self.books = []
        self.file = "data.json"
        self.load_data()

    def add_book(self, book):
        try:
            for b in self.books:
                if b.isbn == book.isbn:
                    logging.error("Duplicate ISBN found while adding a book.")
                    raise ValueError("Book with this ISBN already exists.")

            self.books.append(book)
            self.save_data()
            logging.info(f"Book added: {book.title}, {book.author}, {book.isbn}")

        except Exception as e:
            logging.error(f"Error adding book: {e}")
            print("Error:", e)

    def search_title(self, name):
        name = name.lower()
        results = []

        for item in self.books:
            if name in item.title.lower():
                results.append(item)

        logging.info(f"Title search performed for: {name}")
        return results

    def search_isbn(self, number):
        for item in self.books:
            if item.isbn == number:
                logging.info(f"ISBN search found: {number}")
                return item

        logging.warning(f"ISBN search failed for: {number}")
        return None

    def show_all(self):
        output = []
        for i, item in enumerate(self.books, start=1):
            output.append(f"{i}) {item}")
        return output


    def save_data(self):
        try:
            data = [b.to_dict() for b in self.books]

            with open(self.file, "w") as f:
                json.dump(data, f)

            logging.info("Data saved successfully.")

        except Exception as e:
            logging.error(f"Error saving data: {e}")
            print("Error saving file:", e)

    def load_data(self):
        if not os.path.exists(self.file):
            logging.warning("Data file not found. Starting with empty list.")
            self.books = []
            return

        try:
            with open(self.file, "r") as f:
                data = json.load(f)

            for item in data:
                book_obj = Book(
                    item["title"],
                    item["author"],
                    item["isbn"],
                    item["status"]
                )
                self.books.append(book_obj)

            logging.info("Data loaded successfully.")

        except json.JSONDecodeError:
            logging.error("Data file corrupted. Fresh list created.")
            print("File corrupted. Starting fresh.")
            self.books = []

        except Exception as e:
            logging.error(f"Unexpected error loading file: {e}")
            print("Error loading file:", e)
            self.books = []

