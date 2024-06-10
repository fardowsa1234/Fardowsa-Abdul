# Library Management System

## Description
This is a library management system built using Python with a graphical user interface (GUI) using Tkinter and a command-line interface (CLI) using argparse. The project uses SQLAlchemy for ORM and SQLite as the database.

## Features
- Add and manage library members.
- Add and manage books borrowed by members.
- Interact with the system using both GUI and CLI.

## Dependencies
- Python 3.8+
- SQLAlchemy
- Tkinter (comes with Python standard library)


## Technologies Used

- Python
- Tkinter (for the graphical user interface)
- SQLite (for the database)

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/fardowsa1234/Fardowsa-Abdul-library-management-system.git
    cd Fardowsa-Abdul-library-management-system
    ```

2. **Create a virtual environment and activate it (optional but recommended):**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install tkinter
    pip install pipenv
    pipenv install --ignore-pipfile

    ```
Tkinter: Standard GUI library for Python.
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
datetime: Standard library for manipulating dates and times.


4. **Run the application:**

    ```bash
    python library.py
    ```

## Usage

1. **Add a Book:**
   - Enter the Book ID, Title, Author, and Year in the respective fields.
   - Click on the "Add Book" button to add the book to the database.

2. **View Books:**
   - Click on the "View Books" button to see a list of all books in the library.
  # For the update part i am encoutering an error message and unable to fix it.
3. **Update a Book:**
   - Enter the Book ID of the book you want to update.
   - Enter the new Title, Author, and Year.
   - Click on the "Update Book" button to update the book details.

4. **Delete a Book:**
   - Enter the Book ID of the book you want to delete.
   - Click on the "Delete Book" button to remove the book from the database.

    ## Code Explanation
SQLAlchemy Setup
The SQLAlchemy library is used to handle database operations with ORM:

Member: A class representing the members table.
Book: A class representing the books table.
GUI Setup
The Tkinter library is used for the GUI:

LibraryManagementSystem: A class representing the main application window and its components.
Methods
add_data(): Adds new member and book records to the database.
display_data(): Fetches and displays all records from the database.
delete_data(): Deletes selected records from the database.
clear_data(): Clears input fields.
get_cursor(): Fetches data from the selected record in the display.


## Screenshots

![Library Management System](/home/fardowsa123/Fardowsa-Abdul/Screenshot.png)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# Acknowledgements
I would like to express my gratitude to the following individuals and resources that made this project possible:

Instructors and Mentors: For their invaluable guidance and support throughout the development of this project.

Python Documentation: For comprehensive documentation and resources on Python, Tkinter, and SQLAlchemy.

