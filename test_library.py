import unittest
from Library_Management_System import Library, Book, Member

class TestLibrarySystem(unittest.TestCase):
    """Comprehensive unit tests for the Library Management System."""
    
    def setUp(self):
        self.library = Library()
        self.book = Book(1, "Python Programming", "John Doe", 3)
        self.member = Member(101, "Alice")
        self.library.add_book(self.book)
        self.library.add_member(self.member)

    # Book Management Tests
    def test_add_book(self):
        self.assertEqual(self.library.add_book(Book(1, "Duplicate", "Author", 1)), 
                         "Book ID already exists")
        self.assertEqual(self.library.add_book(Book(2, "New Book", "Author", 1)), 
                         "Book added successfully")

    def test_remove_book(self):
    # Test book not found
        self.assertEqual(self.library.remove_book(999), "Book not found")
        
        # Test successful removal when book exists and isn't borrowed
        self.assertEqual(self.library.remove_book(1), "Book removed successfully")
        
        # Add the book back for the next test
        self.library.add_book(Book(1, "Python Programming", "John Doe", 3))
        
        # Test removal failure when book is borrowed
        self.library.issue_book(101, 1)  # Borrow the book first
        self.assertEqual(
            self.library.remove_book(1), 
            "Cannot remove - book is currently borrowed"
        )
    def test_update_book(self):
        # Test valid update
        self.assertEqual(self.library.update_book(1, title="New Title"), "Book updated successfully")
        # Test invalid author
        self.assertEqual(self.library.update_book(1, author="123Invalid"), "Invalid author name")
        # Test invalid copies
        self.assertEqual(self.library.update_book(1, copies=-1), "Copies must be a positive integer")
        # Test copies less than borrowed
        self.library.issue_book(101, 1)
        self.assertEqual(self.library.update_book(1, copies=0), 
                         "Cannot set copies to 0 as 1 are currently borrowed")

    # Member Management Tests
    def test_add_member(self):
        self.assertEqual(self.library.add_member(Member(101, "Bob")), "Member ID already exists")
        self.assertEqual(self.library.add_member(Member(102, "Bob")), "Member added successfully")

    def test_remove_member(self):
        # Test member not found
        self.assertEqual(self.library.remove_member(999), "Member not found")
        # Test remove with borrowed books
        self.library.issue_book(101, 1)
        self.assertEqual(self.library.remove_member(101), "Cannot remove member with borrowed books")
        # Test successful removal
        self.library.return_book(101, 1)
        self.assertEqual(self.library.remove_member(101), "Member removed successfully")

    def test_update_member(self):
        # Test valid update
        self.assertEqual(self.library.update_member(101, "Alicia"), "Member updated successfully")
        # Test invalid name
        self.assertEqual(self.library.update_member(101, "Alice2"), "Invalid name")
        # Test no changes
        self.assertEqual(self.library.update_member(101, None), "No changes made")

    # Transaction Tests
    def test_book_transactions(self):
        # Test successful borrow
        self.assertEqual(self.library.issue_book(101, 1), "Alice borrowed 'Python Programming'")
        # Test return
        self.assertEqual(self.library.return_book(101, 1), "Alice returned 'Python Programming'")
        # Test double return
        self.assertEqual(self.library.return_book(101, 1), "This book was not borrowed by the member")
        # Test borrow unavailable book
        self.library.update_book(1, copies=0)
        self.assertEqual(self.library.issue_book(101, 1), "Book is not available")

    # Search and Display Tests
    def test_search_books(self):
        # Test title search
        results = self.library.search_books("python")
        self.assertTrue(len(results) > 0)
        # Test author search
        results = self.library.search_books("doe")
        self.assertTrue(len(results) > 0)
        # Test no results
        results = self.library.search_books("nonexistent")
        self.assertEqual(results, ["No matching books found"])

    def test_history_tracking(self):
        # Test member history
        self.library.issue_book(101, 1)
        history = self.library.member_history(101)
        self.assertIn("Borrowed 'Python Programming'", history)
        
        # Test book history
        book_history = self.library.book_history(1)
        self.assertIn("Alice borrowed this book", book_history)

    # Edge Case Tests
    def test_invalid_ids(self):
        # Test non-existent IDs in transactions
        self.assertEqual(self.library.issue_book(999, 1), "Member not found")
        self.assertEqual(self.library.issue_book(101, 999), "Book not found")
        self.assertEqual(self.library.return_book(999, 1), "Member not found")
        self.assertEqual(self.library.return_book(101, 999), "Book not found")

    def test_display_methods(self):
        # Test empty displays
        empty_lib = Library()
        self.assertEqual(empty_lib.display_books(), ["No books available"])
        self.assertEqual(empty_lib.display_members(), ["No members available"])

if __name__ == '__main__':
    unittest.main()