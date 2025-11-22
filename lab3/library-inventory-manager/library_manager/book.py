# --------------------------------------------------------------------
# Name        : Adarsh Rathore
# Roll No     : <2501410014>
# Course      : B.Tech CSE (Cyber Security)
# Semester    : 1st Semester
# Subject     : Programming for Problem Solving Using Python
# File        : main.py
# Project     : Library Inventory Manager
# --------------------------------------------------------------------


class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"Title: {self.title} | Author: {self.author} | ISBN: {self.isbn} | Status: {self.status}\n"


    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }
    
    def is_available(self):
        return self.status == "available"
    
    def issue(self):
        if not self.is_available():
            raise ValueError("This book is already issued.")
        self.status = "issued"
    
    def return_book(self):
        if self.is_available():
            raise ValueError("This book is not issued.")

        self.status = "available"
