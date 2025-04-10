import sys  # System functions for exit handling
import re  # Regular expressions for input validation
from typing import List, Dict, Union, Optional  # Type hints for code clarity

# =============================================
# BASE ENTITY CLASS
# =============================================
class Entity:
    """Base class for all library entities"""

    def __init__(self, entity_id: int, name: str):
        self.entity_id = entity_id  # Unique numeric identifier
        self.name = name  # Display name/title

    def display_info(self) -> str:
        """Basic entity information string"""
        return f"ID: {self.entity_id}, Name: {self.name}"


# =============================================
# BOOK CLASS
# =============================================
class Book(Entity):
    """Represents a library book with tracking features"""

    def __init__(self, book_id: int, title: str, author: str, copies: int):
        super().__init__(book_id, title)
        self.author = author  # Author's full name
        self.copies = copies  # Available copies counter
        self.borrow_history = []  # Transaction history log

    def display_info(self) -> str:
        """Formatted book details with availability"""
        return (
            f"ID: {self.entity_id}, Title: {self.name}, "
            f"Author: {self.author}, Available Copies: {self.copies}"
        )

    def add_to_history(self, action: str, member_name: str) -> None:
        """Record transaction in book's history"""
        self.borrow_history.append(f"{member_name} {action} this book")


# =============================================
# MEMBER CLASS
# =============================================
class Member(Entity):
    """Represents a library member with borrowing capabilities"""

    def __init__(self, member_id: int, name: str):
        super().__init__(member_id, name)
        self.borrowed_books: List[Book] = []  # Currently checked-out books
        self.history: List[str] = []  # Member activity log

    def borrow_book(self, book: Book) -> str:
        """Check out a book if available"""
        if book.copies > 0:
            book.copies -= 1  # Decrement available count
            self.borrowed_books.append(book)
            self.history.append(f"Borrowed '{book.name}'")
            book.add_to_history("borrowed", self.name)
            return f"{self.name} borrowed '{book.name}'"
        return "Book is not available"

    def return_book(self, book: Book) -> str:
        """Return a borrowed book to library"""
        if book in self.borrowed_books:
            book.copies += 1  # Restore available count
            self.borrowed_books.remove(book)
            self.history.append(f"Returned '{book.name}'")
            book.add_to_history("returned", self.name)
            return f"{self.name} returned '{book.name}'"
        return "This book was not borrowed by the member"

    def display_info(self) -> str:
        """Member details with current borrows"""
        borrowed_titles = [book.name for book in self.borrowed_books]
        borrowed_str = ", ".join(borrowed_titles) if borrowed_titles else "None"
        return (
            f"Member ID: {self.entity_id}, Name: {self.name}, "
            f"Borrowed Books: {borrowed_str}"
        )


# =============================================
# LIBRARY MANAGEMENT CLASS
# =============================================
class Library:
    """Core library system handling inventory and transactions"""

    def __init__(self):
        self.books: Dict[int, Book] = {}  # Book storage by ID
        self.members: Dict[int, Member] = {}  # Member storage by ID

    def add_book(self, book: Book) -> str:
        """Add new book to inventory"""
        if book.entity_id in self.books:
            return "Book ID already exists"
        self.books[book.entity_id] = book  # Add to storage
        return "Book added successfully"

    def remove_book(self, book_id: int) -> str:
        """Remove book if not currently borrowed"""
        if book_id not in self.books:
            return "Book not found"

        # Check all members' borrowed books
        for member in self.members.values():
            for book in member.borrowed_books:
                if book.entity_id == book_id:
                    return "Cannot remove - book is currently borrowed"

        del self.books[book_id]  # Remove from storage
        return "Book removed successfully"

    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
        copies: Optional[int] = None,
    ) -> str:
        """Modify book details with validation"""
        if book_id not in self.books:
            return "Book not found"

        book = self.books[book_id]  # Get existing book reference

        if title:
            book.name = title  # Update title

        if author:
            # Validate name format: letters, spaces, . ' -
            if not re.fullmatch(r"[A-Za-z .'-]+", author):
                return "Invalid author name"
            book.author = author

        if copies is not None:
            # Validate numeric input
            if not isinstance(copies, int) or copies < 0:
                return "Copies must be a positive integer"

            # Calculate currently borrowed copies
            borrowed_count = sum(
                1
                for member in self.members.values()
                for b in member.borrowed_books
                if b.entity_id == book_id
            )
            if copies < borrowed_count:
                return f"Cannot set copies to {copies} as {borrowed_count} are currently borrowed"

            book.copies = copies  # Update available count

        return "Book updated successfully"

    def add_member(self, member: Member) -> str:
        """Register new library member"""
        if member.entity_id in self.members:
            return "Member ID already exists"
        self.members[member.entity_id] = member  # Add to registry
        return "Member added successfully"

    def remove_member(self, member_id: int) -> str:
        """Remove member account if no active borrows"""
        if member_id not in self.members:
            return "Member not found"

        if self.members[member_id].borrowed_books:
            return "Cannot remove member with borrowed books"

        del self.members[member_id]  # Remove from registry
        return "Member removed successfully"

    def update_member(self, member_id: int, name: Optional[str] = None) -> str:
        """Update member profile information"""
        if member_id not in self.members:
            return "Member not found"

        if not name:
            return "No changes made"

        # Validate name format: letters, spaces, . ' -
        if not re.fullmatch(r"[A-Za-z .'-]+", name):
            return "Invalid name"

        self.members[member_id].name = name  # Update member name
        return "Member updated successfully"

    def display_books(self) -> List[str]:
        """List all books in inventory"""
        return (
            [book.display_info() for book in self.books.values()]
            if self.books
            else ["No books available"]
        )

    def display_members(self) -> List[str]:
        """List all registered members"""
        return (
            [member.display_info() for member in self.members.values()]
            if self.members
            else ["No members available"]
        )

    def issue_book(self, member_id: int, book_id: int) -> str:
        """Process book checkout"""
        if member_id not in self.members:
            return "Member not found"
        if book_id not in self.books:
            return "Book not found"
        return self.members[member_id].borrow_book(self.books[book_id])

    def return_book(self, member_id: int, book_id: int) -> str:
        """Process book return"""
        if member_id not in self.members:
            return "Member not found"
        if book_id not in self.books:
            return "Book not found"
        return self.members[member_id].return_book(self.books[book_id])

    def search_books(self, keyword: str) -> List[str]:
        """Search books by title or author"""
        keyword = keyword.lower()
        results = []
        for book in self.books.values():
            if keyword in book.name.lower() or keyword in book.author.lower():
                results.append(book.display_info())
        return results if results else ["No matching books found"]

    def member_history(self, member_id: int) -> Union[List[str], str]:
        """Retrieve member's borrowing history"""
        if member_id not in self.members:
            return "Member not found"
        return self.members[member_id].history or ["No activity yet"]

    def book_history(self, book_id: int) -> Union[List[str], str]:
        """Retrieve book's transaction history"""
        if book_id not in self.books:
            return "Book not found"
        return self.books[book_id].borrow_history or ["No activity yet"]


# =============================================
# COMMAND LINE INTERFACE
# =============================================
class LibraryCLI:
    """Text-based user interface for library system"""

    def __init__(self):
        self.library = Library()  # Core library instance
        # Menu command mapping
        self.menu_options = {
            "1": self.add_book,
            "2": self.update_book,
            "3": self.remove_book,
            "4": self.add_member,
            "5": self.update_member,
            "6": self.remove_member,
            "7": self.issue_book,
            "8": self.return_book,
            "9": self.display_books,
            "10": self.display_members,
            "11": self.search_books,
            "12": self.member_history,
            "13": self.book_history,
            "14": self.exit_system,
        }

    def run(self):
        """Main CLI execution loop"""
        print("\nWelcome to the Library Management System!")
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-14): ").strip()
            action = self.menu_options.get(choice)
            if action:
                action()  # Execute selected command
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        """Display main menu options"""
        print("\n--- Library Menu ---")
        print("1. Add Book\t\t2. Update Book\t\t3. Remove Book")
        print("4. Add Member\t\t5. Update Member\t6. Remove Member")
        print("7. Issue Book\t\t8. Return Book\t\t9. Display Books")
        print("10. Display Members\t11. Search Books\t12. Member History")
        print("13. Book History\t14. Exit")

    def get_valid_input(
        self, prompt: str, input_type: type = str, validation: callable = None
    ) -> Union[str, int]:
        """Generic input validation method"""
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
        """Validate names using regex pattern"""
        return bool(re.fullmatch(r"[A-Za-z .'-]+", name))

    def add_book(self):
        """Handle book addition workflow"""
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
        """Handle book update workflow"""
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
        """Handle book removal workflow"""
        print("\n--- Remove Book ---")
        book_id = self.get_valid_input("Book ID to remove: ", int)
        if book_id not in self.library.books:
            print("Book not found.")
            return

        result = self.library.remove_book(book_id)
        print(result)

    def add_member(self):
        """Handle member registration workflow"""
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
        """Handle member update workflow"""
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
        """Handle member removal workflow"""
        print("\n--- Remove Member ---")
        member_id = self.get_valid_input("Member ID to remove: ", int)
        if member_id not in self.library.members:
            print("Member not found.")
            return

        result = self.library.remove_member(member_id)
        print(result)

    def issue_book(self):
        """Handle book checkout workflow"""
        print("\n--- Issue Book ---")
        member_id = self.get_valid_input("Member ID: ", int)
        book_id = self.get_valid_input("Book ID: ", int)

        if None in (member_id, book_id):
            print("Both fields are required.")
            return

        result = self.library.issue_book(member_id, book_id)
        print(result)

    def return_book(self):
        """Handle book return workflow"""
        print("\n--- Return Book ---")
        member_id = self.get_valid_input("Member ID: ", int)
        book_id = self.get_valid_input("Book ID: ", int)

        if None in (member_id, book_id):
            print("Both fields are required.")
            return

        result = self.library.return_book(member_id, book_id)
        print(result)

    def display_books(self):
        """Display all books in inventory"""
        print("\n--- All Books ---")
        for book_info in self.library.display_books():
            print(book_info)

    def display_members(self):
        """Display all registered members"""
        print("\n--- All Members ---")
        for member_info in self.library.display_members():
            print(member_info)

    def search_books(self):
        """Handle book search workflow"""
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
        """Display member's borrowing history"""
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
        """Display book's transaction history"""
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
        """Exit the application"""
        print("\nThank you for using the Library Management System. Goodbye!")
        sys.exit(0)


# =============================================
# MAIN EXECUTION
# =============================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        cli = LibraryCLI()
        cli.run()
    else:
        print("Usage: python Library_Management_System.py cli")
