# Expense Tracker API

This is a backend API built using Django and Django REST Framework for managing personal expenses. It supports secure authentication using JWT tokens and allows users to log in, create, view, filter, and analyze their expenses.

## Project Overview

Features included in this project:
- User login via JWT (token-based authentication)
- Create, update, and delete expense entries
- Filter expenses by date range
- Get analytics like total spending, category-wise summary, and daily/weekly/monthly trends

## Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT (for token-based login)
- SQLite

## How to Run the Project Locally

Step-by-step instructions to set up and run the project:

1. Clone the repository:
   git clone https://github.com/ayushanand1412/expense_tracker.git
   cd expense_tracker

2. Create a virtual environment and activate it:
   For Windows:
   python -m venv venv
   venv\Scripts\activate

   For macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Install all required Python packages:
   pip install -r requirements.txt

4. Apply database migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Create a superuser account to access the admin panel and also for login:
   python manage.py createsuperuser

6. Start the Django development server:
   python manage.py runserver

Now your project is running at:
http://127.0.0.1:8000/

## API Endpoints  

Authentication Endpoints:
- POST /api/login/ : Authenticate and receive access + refresh tokens
- POST /api/token/refresh/ : Get a new access token using a refresh token

Expense Management Endpoints:
- POST /api/expenses/ : Create a new expense 
- GET /api/expenses/ : Get all expenses for the logged-in user
- GET /api/expenses/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD : Get expenses filtered by date range
- PUT /api/expenses/<id>/ : Update an existing expense
- DELETE /api/expenses/<id>/ : Delete an expense

Analytics Endpoint:
- GET /api/expenses/analytics/ : Get expense analytics for the logged-in user
- GET /api/expenses/analytics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD : 
  Returns total expense, category-wise breakdown, and daily, weekly, monthly summaries.

## Sample API Call: POST /api/expenses/

In Headers:
  Authorization: Bearer <access_token>
  Content-Type: application/json

Body:
  {
    "amount": 500,
    "category": "FOOD",
    "date": "2025-06-20"
  }

## Notes

- All endpoints are protected and require authentication.
- Use the access token in the headers like this:
  Authorization: Bearer your_access_token_here
- SQLite is used for local development.
- Make sure to configure Django to use the custom user model defined in the project.

## Additional Notes

- Token Expiry:  
  Access tokens are valid for **30 minutes**. After that, use the refresh token at `/api/token/refresh/` to get a new one.

- Date Format:  
  All dates must be in the format `YYYY-MM-DD`.  
  Example: `2025-06-30`

- Allowed Categories for Expenses:  
  Only the following categories are valid (must be in **uppercase**):
  - FOOD
  - TRAVEL
  - BILLS
  - OTHER

- Authentication Header:
  All API endpoints require authentication using a JWT access token.  
  In Postman (or any API testing tool), include this in the Headers tab:
  Key: Authorization
  Value: Bearer <your_access_token>

- Recommended Tool for Testing:  
  Use **Postman** to test API endpoints. Make sure to:
  1. First, obtain your access and refresh token by calling `/api/login/`.
  2. Then, add the access token to the `Authorization` header as shown above.