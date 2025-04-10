import unittest
import sys
import re
from typing import List, Dict, Union, Optional

class Entity:
    """Base class for library entities with common attributes."""
    def __init__(self, entity_id: int, name: str):
        self.entity_id = entity_id
        self.name = name

    def display_info(self) -> str:
        """Display basic information about the entity."""
        return f"ID: {self.entity_id}, Name: {self.name}"


class Book(Entity):
    """Class representing a book in the library."""
    def __init__(self, book_id: int, title: str, author: str, copies: int):
        super().__init__(book_id, title)
        self.author = author
        self.copies = copies
        self.borrow_history = []

    def display_info(self) -> str:
        """Display detailed information about the book."""
        return (f"ID: {self.entity_id}, Title: {self.name}, "
                f"Author: {self.author}, Available Copies: {self.copies}")

    def add_to_history(self, action: str, member_name: str) -> None:
        """Record a transaction in the book's history."""
        self.borrow_history.append(f"{member_name} {action} this book")


class Member(Entity):
    """Class representing a library member."""
    def __init__(self, member_id: int, name: str):
        super().__init__(member_id, name)
        self.borrowed_books: List[Book] = []
        self.history: List[str] = []

    def borrow_book(self, book: Book) -> str:
        """Borrow a book if available."""
        if book.copies > 0:
            book.copies -= 1
            self.borrowed_books.append(book)
            self.history.append(f"Borrowed '{book.name}'")
            book.add_to_history("borrowed", self.name)
            return f"{self.name} borrowed '{book.name}'"
        return "Book is not available"

    def return_book(self, book: Book) -> str:
        """Return a borrowed book."""
        if book in self.borrowed_books:
            book.copies += 1
            self.borrowed_books.remove(book)
            self.history.append(f"Returned '{book.name}'")
            book.add_to_history("returned", self.name)
            return f"{self.name} returned '{book.name}'"
        return "This book was not borrowed by the member"

    def display_info(self) -> str:
        """Display member information with borrowed books."""
        borrowed_titles = [book.name for book in self.borrowed_books]
        borrowed_str = ", ".join(borrowed_titles) if borrowed_titles else "None"
        return (f"Member ID: {self.entity_id}, Name: {self.name}, "
                f"Borrowed Books: {borrowed_str}")


class Library:
    """Main class representing the library and its operations."""
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.members: Dict[int, Member] = {}

    def add_book(self, book: Book) -> str:
        """Add a new book to the library."""
        if book.entity_id in self.books:
            return "Book ID already exists"
        self.books[book.entity_id] = book
        return "Book added successfully"

    def remove_book(self, book_id: int) -> str:
        """Remove a book from the library."""
        if book_id not in self.books:
            return "Book not found"
        
        # Check if any member has borrowed this book
        for member in self.members.values():
            for book in member.borrowed_books:
                if book.entity_id == book_id:
                    return "Cannot remove - book is currently borrowed"
        
        del self.books[book_id]
        return "Book removed successfully"

    def update_book(self, book_id: int, title: Optional[str] = None, 
                   author: Optional[str] = None, copies: Optional[int] = None) -> str:
        """Update book details."""
        if book_id not in self.books:
            return "Book not found"
        
        book = self.books[book_id]
        
        if title:
            book.name = title
            
        if author:
            if not re.fullmatch(r"[A-Za-z .'-]+", author):
                return "Invalid author name"
            book.author = author
            
        if copies is not None:
            if not isinstance(copies, int) or copies < 0:
                return "Copies must be a positive integer"
            
            # Ensure we don't set available copies less than currently borrowed
            borrowed_count = sum(1 for member in self.members.values() 
                              for b in member.borrowed_books if b.entity_id == book_id)
            if copies < borrowed_count:
                return f"Cannot set copies to {copies} as {borrowed_count} are currently borrowed"
                
            book.copies = copies
        
        return "Book updated successfully"

    def add_member(self, member: Member) -> str:
        """Add a new member to the library."""
        if member.entity_id in self.members:
            return "Member ID already exists"
        self.members[member.entity_id] = member
        return "Member added successfully"

    def remove_member(self, member_id: int) -> str:
        """Remove a member from the library."""
        if member_id not in self.members:
            return "Member not found"
        
        if self.members[member_id].borrowed_books:
            return "Cannot remove member with borrowed books"
            
        del self.members[member_id]
        return "Member removed successfully"

    def update_member(self, member_id: int, name: Optional[str] = None) -> str:
        """Update member details."""
        if member_id not in self.members:
            return "Member not found"
        
        if not name:
            return "No changes made"
            
        if not re.fullmatch(r"[A-Za-z .'-]+", name):
            return "Invalid name"
            
        self.members[member_id].name = name
        return "Member updated successfully"

    def display_books(self) -> List[str]:
        """Return information about all books."""
        return [book.display_info() for book in self.books.values()] if self.books else ["No books available"]

    def display_members(self) -> List[str]:
        """Return information about all members."""
        return [member.display_info() for member in self.members.values()] if self.members else ["No members available"]

    def issue_book(self, member_id: int, book_id: int) -> str:
        """Issue a book to a member."""
        if member_id not in self.members:
            return "Member not found"
        if book_id not in self.books:
            return "Book not found"
        return self.members[member_id].borrow_book(self.books[book_id])

    def return_book(self, member_id: int, book_id: int) -> str:
        """Return a book from a member."""
        if member_id not in self.members:
            return "Member not found"
        if book_id not in self.books:
            return "Book not found"
        return self.members[member_id].return_book(self.books[book_id])

    def search_books(self, keyword: str) -> List[str]:
        """Search books by title or author."""
        keyword = keyword.lower()
        results = []
        for book in self.books.values():
            if (keyword in book.name.lower() or 
                keyword in book.author.lower()):
                results.append(book.display_info())
        return results if results else ["No matching books found"]

    def member_history(self, member_id: int) -> Union[List[str], str]:
        """Get borrowing history for a member."""
        if member_id not in self.members:
            return "Member not found"
        return self.members[member_id].history or ["No activity yet"]

    def book_history(self, book_id: int) -> Union[List[str], str]:
        """Get borrowing history for a book."""
        if book_id not in self.books:
            return "Book not found"
        return self.books[book_id].borrow_history or ["No activity yet"]


class LibraryCLI:
    """Command Line Interface for the Library Management System."""
    def __init__(self):
        self.library = Library()
        self.menu_options = {
            '1': self.add_book,
            '2': self.update_book,
            '3': self.remove_book,
            '4': self.add_member,
            '5': self.update_member,
            '6': self.remove_member,
            '7': self.issue_book,
            '8': self.return_book,
            '9': self.display_books,
            '10': self.display_members,
            '11': self.search_books,
            '12': self.member_history,
            '13': self.book_history,
            '14': self.exit_system
        }

    def run(self):
        """Run the CLI interface."""
        print("\nWelcome to the Library Management System!")
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-14): ").strip()
            action = self.menu_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        """Display the main menu."""
        print("\n--- Library Menu ---")
        print("1. Add Book\t\t2. Update Book\t\t3. Remove Book")
        print("4. Add Member\t\t5. Update Member\t6. Remove Member")
        print("7. Issue Book\t\t8. Return Book\t\t9. Display Books")
        print("10. Display Members\t11. Search Books\t12. Member History")
        print("13. Book History\t14. Exit")

    def get_valid_input(self, prompt: str, input_type: type = str, 
                       validation: callable = None) -> Union[str, int]:
        """Get and validate user input."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    return None
                
                if input_type == int:
                    user_input = int(user_input)
                    if user_input < 0:
                        print("Please enter a positive number.")
                        continue
                
                if validation and not validation(user_input):
                    print("Invalid input. Please try again.")
                    continue
                
                return user_input
            except ValueError:
                print("Invalid input. Please try again.")

    def validate_name(self, name: str) -> bool:
        """Validate names (for authors and members)."""
        return bool(re.fullmatch(r"[A-Za-z .'-]+", name))

    def add_book(self):
        """Add a new book to the library."""
        print("\n--- Add New Book ---")
        book_id = self.get_valid_input("Book ID: ", int)
        if book_id in self.library.books:
            print("Book ID already exists.")
            return
            
        title = self.get_valid_input("Title: ", str, lambda x: len(x) > 0)
        author = self.get_valid_input("Author: ", str, self.validate_name)
        copies = self.get_valid_input("Copies: ", int)
        
        if None in (book_id, title, author, copies):
            print("All fields except copies are required.")
            return
            
        result = self.library.add_book(Book(book_id, title, author, copies))
        print(result)

    def update_book(self):
        """Update an existing book's details."""
        print("\n--- Update Book ---")
        book_id = self.get_valid_input("Book ID to update: ", int)
        if book_id not in self.library.books:
            print("Book not found.")
            return
            
        print("Leave fields blank to keep current values.")
        title = self.get_valid_input("New Title: ", str, lambda x: len(x) > 0)
        author = self.get_valid_input("New Author: ", str, self.validate_name)
        copies = self.get_valid_input("New Copies: ", int)
        
        result = self.library.update_book(book_id, title, author, copies)
        print(result)

    def remove_book(self):
        """Remove a book from the library."""
        print("\n--- Remove Book ---")
        book_id = self.get_valid_input("Book ID to remove: ", int)
        if book_id not in self.library.books:
            print("Book not found.")
            return
            
        result = self.library.remove_book(book_id)
        print(result)

    def add_member(self):
        """Add a new member to the library."""
        print("\n--- Add New Member ---")
        member_id = self.get_valid_input("Member ID: ", int)
        if member_id in self.library.members:
            print("Member ID already exists.")
            return
            
        name = self.get_valid_input("Name: ", str, self.validate_name)
        if None in (member_id, name):
            print("All fields are required.")
            return
            
        result = self.library.add_member(Member(member_id, name))
        print(result)

    def update_member(self):
        """Update an existing member's details."""
        print("\n--- Update Member ---")
        member_id = self.get_valid_input("Member ID to update: ", int)
        if member_id not in self.library.members:
            print("Member not found.")
            return
            
        print("Leave field blank to keep current value.")
        name = self.get_valid_input("New Name: ", str, self.validate_name)
        
        result = self.library.update_member(member_id, name)
        print(result)

    def remove_member(self):
        """Remove a member from the library."""
        print("\n--- Remove Member ---")
        member_id = self.get_valid_input("Member ID to remove: ", int)
        if member_id not in self.library.members:
            print("Member not found.")
            return
            
        result = self.library.remove_member(member_id)
        print(result)

    def issue_book(self):
        """Issue a book to a member."""
        print("\n--- Issue Book ---")
        member_id = self.get_valid_input("Member ID: ", int)
        book_id = self.get_valid_input("Book ID: ", int)
        
        if None in (member_id, book_id):
            print("Both fields are required.")
            return
            
        result = self.library.issue_book(member_id, book_id)
        print(result)

    def return_book(self):
        """Return a book from a member."""
        print("\n--- Return Book ---")
        member_id = self.get_valid_input("Member ID: ", int)
        book_id = self.get_valid_input("Book ID: ", int)
        
        if None in (member_id, book_id):
            print("Both fields are required.")
            return
            
        result = self.library.return_book(member_id, book_id)
        print(result)

    def display_books(self):
        """Display all books in the library."""
        print("\n--- All Books ---")
        for book_info in self.library.display_books():
            print(book_info)

    def display_members(self):
        """Display all members in the library."""
        print("\n--- All Members ---")
        for member_info in self.library.display_members():
            print(member_info)

    def search_books(self):
        """Search books by title or author."""
        print("\n--- Search Books ---")
        keyword = input("Enter title or author keyword: ").strip()
        if not keyword:
            print("Please enter a search term.")
            return
            
        results = self.library.search_books(keyword)
        print("\nSearch Results:")
        for result in results:
            print(result)

    def member_history(self):
        """Display a member's borrowing history."""
        print("\n--- Member History ---")
        member_id = self.get_valid_input("Member ID: ", int)
        if member_id is None:
            print("Member ID is required.")
            return
            
        history = self.library.member_history(member_id)
        print("\nBorrowing History:")
        if isinstance(history, list):
            for entry in history:
                print(entry)
        else:
            print(history)

    def book_history(self):
        """Display a book's borrowing history."""
        print("\n--- Book History ---")
        book_id = self.get_valid_input("Book ID: ", int)
        if book_id is None:
            print("Book ID is required.")
            return
            
        history = self.library.book_history(book_id)
        print("\nBorrowing History:")
        if isinstance(history, list):
            for entry in history:
                print(entry)
        else:
            print(history)

    def exit_system(self):
        """Exit the Library Management System."""
        print("\nThank you for using the Library Management System. Goodbye!")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        cli = LibraryCLI()
        cli.run()
    else:
        print("Usage: python Library_Management_System.py cli")