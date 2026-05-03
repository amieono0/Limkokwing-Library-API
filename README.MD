# Library Management System API

## Overview
This is a simple Library Management System API built using Python for Limkokwing University.  
It allows users to borrow, return, and check library books, as well as track overdue books and fines.

The system also demonstrates asynchronous programming to simulate multiple users interacting at the same time.

## Features
- View available books  
- Borrow books  
- Return books  
- View borrowed books per user  
- Check overdue books and calculate fines  
- Simulate multiple users using async programming  


##  Technologies Used
- Python  
- asyncio  
- datetime module  
- Dictionary-based data storage  

 
## How It Works
Users interact with the system through a menu. The system processes requests such as borrowing and returning books, updates records, and calculates overdue fines when necessary. Async functions are used to simulate multiple users working at the same time.


##  How to Run
```bash
python main.py