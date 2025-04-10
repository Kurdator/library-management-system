# Library Management System

A simple yet powerful Library Management System in Python that supports managing books and members, tracking borrow/return history, and enforcing essential business rules.

## Features

- **Book Management**
  - Add, remove, update books
  - Validate unique book IDs, valid metadata
  - Prevent removal of borrowed books

- **Member Management**
  - Add, remove, update members
  - Prevent removal of members with borrowed books

- **Transactions**
  - Borrow and return books
  - Maintain borrow limits based on availability
  - Prevent invalid transactions

- **Search and Display**
  - Search books by title or author (case-insensitive)
  - Display all books and members
  - Gracefully handles empty results

- **History Tracking**
  - Logs every borrow and return
  - View history per book or member

## Project Structure

```
library-management-system/
├── Library_Management_System.py   # Core implementation
├── test_library.py                # Unit tests using unittest
├── README.md                      # This file
```

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

Clone the repository:
```bash
git clone https://github.com/Kurdator/library-management-system.git
```

No external libraries are required—only the standard Python library.

### Running the Application

This project is currently a module with no GUI.
To run it with Command-Line Interface:
```bash
python .\Library_Management_System.py cli
```
You can import and use the classes (`Library`, `Book`, `Member`) in your own Python scripts.

### Running Tests

To run the test suite:

```bash
python test_library.py
```
To see exactly which tests are running and their status:

```bash
python test_library.py -v
```

You’ll see output like this:
```
test_add_book (__main__.TestLibrarySystem) ... ok
test_book_transactions (__main__.TestLibrarySystem) ... ok
test_display_methods (__main__.TestLibrarySystem) ... ok
test_history_tracking (__main__.TestLibrarySystem) ... ok
test_invalid_ids (__main__.TestLibrarySystem) ... ok
test_remove_book (__main__.TestLibrarySystem) ... ok
test_remove_member (__main__.TestLibrarySystem) ... ok
test_search_books (__main__.TestLibrarySystem) ... ok
test_update_book (__main__.TestLibrarySystem) ... ok
test_update_member (__main__.TestLibrarySystem) ... ok
...
----------------------------------------------------------------------
Ran 20 tests in 0.004s

OK
```

## Sample Usage

```python
from Library_Management_System import Library, Book, Member

library = Library()

# Add a book
book = Book(1, "Python Crash Course", "Eric Matthes", 2)
library.add_book(book)

# Add a member
member = Member(101, "Alice")
library.add_member(member)

# Issue and return books
library.issue_book(101, 1)
library.return_book(101, 1)

# Display
print(library.display_books())
print(library.display_members())
```

## Test Highlights

- Validates input data and operations
- Prevents duplicate IDs and invalid operations
- Covers:
  - Add/update/delete for books and members
  - Book transactions
  - History tracking
  - Display and search
  - Edge cases (e.g., borrowing unavailable books, invalid IDs)

## Author

- **Abdulla Hassam**
- GitHub: [@Kurdator](https://github.com/Kurdator)

---

**Happy Coding!**