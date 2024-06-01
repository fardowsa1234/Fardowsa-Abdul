import tkinter as tk
from tkinter import messagebox
import sqlite3

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x500")

        # Database connection
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Styling
        self.root.configure(bg="lightblue")

        # GUI elements
        self.title_label = tk.Label(root, text="LIBRARY MANAGEMENT SYSTEM", font=("Arial", 24), fg="blue", bg="lightblue")
        self.title_label.pack(pady=20)

        self.id_label = tk.Label(root, text="Book ID", font=("Arial", 12), fg="green", bg="lightblue")
        self.id_label.pack()
        self.id_entry = tk.Entry(root, font=("Arial", 12))
        self.id_entry.pack()

        self.title_label = tk.Label(root, text="Title", font=("Arial", 12), fg="green", bg="lightblue")
        self.title_label.pack()
        self.title_entry = tk.Entry(root, font=("Arial", 12))
        self.title_entry.pack()

        self.author_label = tk.Label(root, text="Author", font=("Arial", 12), fg="green", bg="lightblue")
        self.author_label.pack()
        self.author_entry = tk.Entry(root, font=("Arial", 12))
        self.author_entry.pack()

        self.year_label = tk.Label(root, text="Year", font=("Arial", 12), fg="green", bg="lightblue")
        self.year_label.pack()
        self.year_entry = tk.Entry(root, font=("Arial", 12))
        self.year_entry.pack()

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book, font=("Arial", 12), fg="white", bg="green")
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View Books", command=self.view_books, font=("Arial", 12), fg="white", bg="green")
        self.view_button.pack()

        self.update_button = tk.Button(root, text="Update Book", command=self.update_book, font=("Arial", 12), fg="white", bg="green")
        self.update_button.pack()

        self.delete_button = tk.Button(root, text="Delete Book", command=self.delete_book, font=("Arial", 12), fg="white", bg="green")
        self.delete_button.pack()

        self.books_listbox = tk.Listbox(root, width=80, height=10, font=("Arial", 12))
        self.books_listbox.pack(pady=20)

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS books
               (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)'''
        )
        self.conn.commit()

    def add_book(self):
        book_id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if book_id and title and author and year:
            self.cursor.execute(
                "INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?)",
                (book_id, title, author, year)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "All fields are required!")

    def view_books(self):
        self.books_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        for book in books:
            self.books_listbox.insert(tk.END, book)

    def update_book(self):
        book_id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if book_id and title and author and year:
            self.cursor.execute(
                "UPDATE books SET title=?, author=?, year=? WHERE id=?",
                (title, author, year, book_id)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Book updated successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_book(self):
        book_id = self.id_entry.get()

        if book_id:
            self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Book ID is required!")

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
