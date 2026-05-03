import asyncio
from typing import Dict, List
from datetime import datetime, timedelta

books: Dict[int, Dict[str, object]] = {
    1: {"title": "Half of a Yellow Sun", "available": True},
    2: {"title": "Things Fall Apart", "available": True},
    3: {"title": "The Concubine", "available": True},
}

borrowed_books: Dict[int, List[Dict[str, object]]] = {}

FINE_PER_DAY: int = 500


def show_books() -> None:
    print("\nBOOK LIST")

    for book_id, info in books.items():
        status = "Available" if info["available"] else "Not Available"
        print(f"{book_id}. {info['title']} - {status}")


def show_user_books(user_id: int) -> None:
    print(f"\nUSER {user_id} BOOKS")

    user_books = borrowed_books.get(user_id, [])

    if not user_books:
        print("No borrowed books")
        return

    for book in user_books:
        print(f"{book['title']} | Due: {book['due_date']}")


async def borrow_book(user_id: int, book_id: int) -> str:
    await asyncio.sleep(1)

    if book_id not in books:
        return "Book not found"

    if not books[book_id]["available"]:
        return "Book not available"

    books[book_id]["available"] = False

    due_date = datetime.now() + timedelta(days=7)

    record = {
        "book_id": book_id,
        "title": books[book_id]["title"],
        "due_date": due_date.strftime("%Y-%m-%d")
    }

    borrowed_books.setdefault(user_id, []).append(record)

    return f"Borrowed: {record['title']} (Due: {record['due_date']})"


async def return_book(user_id: int, book_id: int) -> str:
    await asyncio.sleep(1)

    user_books = borrowed_books.get(user_id, [])

    for book in user_books:
        if book["book_id"] == book_id:
            user_books.remove(book)
            books[book_id]["available"] = True
            return f"Returned: {book['title']}"

    return "Book not found in borrowed list"


def check_overdue(user_id: int) -> None:
    print(f"\nOVERDUE BOOKS - USER {user_id}")

    user_books = borrowed_books.get(user_id, [])
    today = datetime.now()

    found = False

    for book in user_books:
        due_date = datetime.strptime(book["due_date"], "%Y-%m-%d")

        if today > due_date:
            days = (today - due_date).days
            fine = days * FINE_PER_DAY

            print(f"{book['title']} | {days} days late | Fine: {fine} Le")
            found = True

    if not found:
        print("No overdue books")


async def simulate_users() -> None:
    print("\nSIMULATING MULTIPLE USERS")

    tasks = [
        borrow_book(101, 1),
        borrow_book(102, 1),
        borrow_book(103, 2)
    ]

    results = await asyncio.gather(*tasks)

    for r in results:
        print(r)


async def main() -> None:

    while True:
        print("\nLibrary System Menu")
        print("1. View Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View My Books")
        print("5. Check Overdue Books")
        print("6. Simulate Multiple Users")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            show_books()

        elif choice == "2":
            user_id = int(input("User ID: "))
            book_id = int(input("Book ID: "))
            print(await borrow_book(user_id, book_id))

        elif choice == "3":
            user_id = int(input("User ID: "))
            book_id = int(input("Book ID: "))
            print(await return_book(user_id, book_id))

        elif choice == "4":
            user_id = int(input("User ID: "))
            show_user_books(user_id)

        elif choice == "5":
            user_id = int(input("User ID: "))
            check_overdue(user_id)

        elif choice == "6":
            await simulate_users()

        elif choice == "7":
            print("Exiting system...")
            break

        else:
            print("Invalid choice")
            

if __name__ == "__main__":
    asyncio.run(main())