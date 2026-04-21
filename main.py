from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncio

app = FastAPI(title="Limkokwing Library API", description="API for library management system")

#  DATA MODELS  
class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    available: bool
    borrowed_by: Optional[str] = None
    due_date: Optional[str] = None

class User(BaseModel):
    username: str
    fines: float = 0.0

# SAMPLE DATABASE  
books: List[Book] = [
    Book(id=1, title="Python Programming", author="John Doe", category="Programming", available=True, borrowed_by=None, due_date=None),
    Book(id=2, title="Data Science 101", author="Jane Smith", category="Data Science", available=True, borrowed_by=None, due_date=None),
    Book(id=3, title="Web Development", author="Mark Lee", category="Web", available=True, borrowed_by=None, due_date=None),
]

users: List[User] = [
    User(username="student1", fines=0.0),
    User(username="student2", fines=0.0),
]

# HELPER FUNCTIONS  
def calculate_fine(due_date_str: str) -> float:
    """Calculate fine at $0.50 per day overdue"""
    due_date = datetime.fromisoformat(due_date_str)
    if datetime.now() > due_date:
        days_overdue = (datetime.now() - due_date).days
        return days_overdue * 0.50
    return 0.0

#  ENDPOINTS 

# Home route
@app.get("/")
async def home() -> dict:
    return {"message": "Welcome to Limkokwing Library API", "status": "running"}

# Search books by title, author, or category
@app.get("/books")
async def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
) -> List[Book]:
    results = books
    
    if title:
        results = [b for b in results if title.lower() in b.title.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.lower()]
    if category:
        results = [b for b in results if category.lower() in b.category.lower()]
    
    if not results:
        raise HTTPException(status_code=404, detail="No books found")
    
    return results

# Borrow a book
@app.post("/borrow")
async def borrow_book(username: str, book_id: int) -> dict:
    """Borrow a book"""
    
    await asyncio.sleep(0.1)
    
    # Find the book
    book = next((b for b in books if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if available
    if not book.available:
        raise HTTPException(status_code=400, detail="Book already borrowed")
    
    # Find user
    user = next((u for u in users if u.username == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check fines
    if user.fines > 0:
        raise HTTPException(status_code=400, detail=f"User has outstanding fines: ${user.fines}")
    
    # Borrow the book
    due_date = datetime.now() + timedelta(days=14)
    book.available = False
    book.borrowed_by = username
    book.due_date = due_date.isoformat()
    
    return {
        "message": "Book borrowed successfully",
        "book_title": book.title,
        "borrowed_by": username,
        "due_date": book.due_date
    }

# Return a book
@app.post("/return")
async def return_book(book_id: int, username: str) -> dict:
    """Return a book"""
    
    await asyncio.sleep(0.1)
    
    book = next((b for b in books if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.available:
        raise HTTPException(status_code=400, detail="Book is not borrowed")
    
    if book.borrowed_by != username:
        raise HTTPException(status_code=400, detail="This book was borrowed by another user")
    
    # Calculate fine if overdue
    fine = calculate_fine(book.due_date) if book.due_date else 0.0
    
    if fine > 0:
        user = next((u for u in users if u.username == username), None)
        if user:
            user.fines += fine
    
    # Return the book
    book.available = True
    book.borrowed_by = None
    book.due_date = None
    
    return {
        "message": "Book returned successfully",
        "fine_applied": fine,
        "total_fines_owed": next((u.fines for u in users if u.username == username), 0)
    }

# Get overdue books
@app.get("/overdue")
async def get_overdue_books() -> List[dict]:
    overdue_books = []
    
    for book in books:
        if not book.available and book.due_date:
            fine = calculate_fine(book.due_date)
            if fine > 0:
                overdue_books.append({
                    "book_id": book.id,
                    "title": book.title,
                    "borrowed_by": book.borrowed_by,
                    "due_date": book.due_date,
                    "fine": fine
                })
    
    return overdue_books

# Get user fines
@app.get("/fines/{username}")
async def get_user_fines(username: str) -> dict:
    user = next((u for u in users if u.username == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"username": username, "total_fines": user.fines}