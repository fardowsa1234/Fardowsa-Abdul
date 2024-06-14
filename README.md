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
    git clone https://github.com/fardowsa1234/library-management-system-Abdullahi.git
    cd library-management-system-abdullahi
    ```



2. **Install the required packages:**

    ```bash
    pip install tkinter
    pip install pipenv
    pipenv install --ignore-pipfile

    ```
Tkinter: Standard GUI library for Python.
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
datetime: Standard library for manipulating dates and times.


3. **Run the application:**

    ```bash
    python3 library.py
    python3 CLI.py
    ```


## Usage

### Graphical User Interface (GUI)

1. **Add Data**: Enter member and book details in the respective fields and click "Add Data" to add the records to the database.
2. **Display Data**: Click "Display Data" to view all records in the database.
3. **Clear Data**: Click "Clear Data" to clear all input fields.
4. **Update Data**: Select a record from the displayed data, modify the details, and click "Update Data" to update the record in the database.
5. **Delete Data**: Select a record from the displayed data and click "Delete Data" to remove the record from the database.
6. **Exit**: Click "Exit" to close the application.

### Command Line Interface (CLI)

In addition to the GUI, a CLI version of the library management system is also provided. This allows for similar operations through the command line.

1. **Add Data**: Use the following command to add a new member and book record:

    ```bash
    python library_cli.py add --membertype <type> --prnno <prn> --idno <id> --firstname <first> --lastname <last> --address1 <addr1> --address2 <addr2> --postcode <postcode> --mobile <mobile> --bookid <bookid> --title <title> --author <author> --dateborrowed <dd/mm/yyyy> --daysonbook <days> --dateoverdue <dd/mm/yyyy> --latereturnfine <fine>
    ```

2. **Display Data**: Use the following command to display all records:

    ```bash
    python library_cli.py display
    ```

3. **Update Data**: Use the following command to update an existing member and book record:

    ```bash
    python library_cli.py update --idno <id> --membertype <type> --prnno <prn> --firstname <first> --lastname <last> --address1 <addr1> --address2 <addr2> --postcode <postcode> --mobile <mobile> --bookid <bookid> --title <title> --author <author> --dateborrowed <dd/mm/yyyy> --daysonbook <days> --dateoverdue <dd/mm/yyyy> --latereturnfine <fine>
    ```

4. **Delete Data**: Use the following command to delete a member and book record:

    ```bash
    python library_cli.py delete --idno <id>
    ```

## Example

### GUI

1. Launch the application:

    ```bash
    python library_management_system.py
    ```

2. Use the GUI to manage member and book records.

### CLI

1. Add a new member and book record:

    ```bash
    python library_cli.py add --membertype "Student" --prnno "123456" --idno "ID001" --firstname "John" --lastname "Doe" --address1 "123 Main St" --address2 "Apt 4" --postcode "12345" --mobile "9876543210" --bookid "B001" --title "Python Programming" --author "Author Name" --dateborrowed "01/01/2023" --daysonbook "14" --dateoverdue "15/01/2023" --latereturnfine "$5"
    ```

2. Display all records:

    ```bash
    python library_cli.py display
    ```

3. Update an existing member and book record:

    ```bash
    python library_cli.py update --idno "ID001" --membertype "Faculty" --prnno "654321" --firstname "Jane" --lastname "Doe" --address1 "456 Elm St" --address2 "Suite 2" --postcode "54321" --mobile "1234567890" --bookid "B002" --title "Advanced Python" --author "Another Author" --dateborrowed "05/01/2023" --daysonbook "7" --dateoverdue "12/01/2023" --latereturnfine "$10"
    ```

4. Delete a member and book record:

    ```bash
    python library_cli.py delete --idno "ID001"

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# Acknowledgements
I would like to express my gratitude to the following individuals and resources that made this project possible:

Instructors and Mentors: For their invaluable guidance and support throughout the development of this project.

Python Documentation: For comprehensive documentation and resources on Python, Tkinter, and SQLAlchemy.

