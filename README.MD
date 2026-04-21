# Limkokwing Library API

## Project Description
A FastAPI-based library management system for Limkokwing University. This API allows users to search for books, borrow/return books, and track overdue fines.

## Features
- Search books by title, author, or category
- Borrow and return books with async support
- Track overdue books and calculate fines ($0.50/day)
- Multiple user support

## Technologies Used
- Python 3.13
- FastAPI
- Uvicorn

## Installation & Running

```bash
pip install fastapi uvicorn
python -m uvicorn main:app --reload --port 5000