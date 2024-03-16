# SHOPPING CART PROJECT


## Features

- User Registartion
- User login
- Create / update Product
- Inventory management
- checkout
- payment

## Technologies Used

- Django
- Django REST Framework
- Django REST Framework Simple JWT

## Installation

1. Clone the repository:

   `git clone <repository-url>`

2. Install dependencies:

    `pip install -r requirements.txt`

3. Run migrations to create database tables:

    `python manage.py migrate`

4. Create a superuser:

    `python manage.py createsuperuser`

5. Start the development server:

    `python manage.py runserver`

6. Visit http://localhost:8000/admin/ to access the admin panel.

## Usage

### Register (Signup) API
    Endpoint: api/v1/register/
    Method: POST
    Data Payload: 
    {
    "email": "jon@gmail.com",
    "password1": "User123#",
    "password2": "User123#",
    "first_name": "Jon",
    "last_name": "Doe"
    }

    Response:
    {
    "first_name": "Jon",
    "last_name": "Doe"
    "email": "jon@gmail.com"
    }
    

### Login API
    Endpoint: api/v1/login/
    Method: POST
    Data Payload: 
    {
    "email": "jon@gmail.com",
    "password1": "User123#"
    }

    Response:
    {
    "email": "jon@gmail.com",
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDY5NzM5MiwiaWF0IjoxNzEwNjEwOTkyLCJqdGkiOiIyNGNmMDUzNGFiMmU0NTA5OTE1NmQyY2IxNzY4NmJlYyIsInVzZXJfaWQiOjJ9.6pnxu1EMOVjLVb8cYcZwiFdCnVy2TJnPBKAIMS-nNaQ",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwNjExMjkyLCJpYXQiOjE3MTA2MTA5OTIsImp0aSI6ImMyOGEyNzA2YjBjNjQ5ZjVhMzc5NWUyODdiOWNlNGVkIiwidXNlcl9pZCI6Mn0.AivE1uvznc81OYYc2OX5VqB1buOedN7ohB89plGMQJQ"
    }
    }

### Products Listing API
    Endpoint: /api/v1/products/
    Method: GET
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Response: 
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "test product",
            "description": "lorem",
            "price": "100.00",
            "quantity_available": 98
        }
    ]
    }



### Products Retrieve API
    Endpoint: /api/v1/products/1/
    Method: GET
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Response: 
    {
    "id": 1,
    "name": "test product",
    "description": "lorem",
    "price": "100.00",
    "quantity_available": 98
    }


### Products Create API

Only user with `staff` permission can add a product.

    Endpoint: /api/v1/products/
    Method: POST
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "name": "product 1",
    "description": "new pro",
    "quantity_available": 100,
    "price": 10
    }
    Response: 
    {
    "id": 1,
    "name": "product 1",
    "description": "new pro",
    "price": "10.00",
    "quantity_available": 10
    }

### Products Update API
Only user with `staff` permission can edit a product.

    Endpoint: /api/v1/products/1/
    Method: PATCH
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "name": "product 1",
    "description": "new pro",
    "quantity_available": 10,
    "price": 100
    }
    Response: 
    
    {
    "name": "product 1",
    "description": "new pro",
    "quantity_available": 10
    "price": 100
    }


### Orders Listing API

    Endpoint: /api/v1/orders/
    Method: GET
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Response: 
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "order_status": "SUCCESS",
                "created_at": "2024-03-16T14:22:00.834306Z",
                "updated_at": "2024-03-16T17:56:01.748118Z",
                "total_amount": 200
            }
        ]
    }

### Orders Retrieve API

    Endpoint: /api/v1/orders/1/
    Method: GET
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Response: 
        {
            "id": 1,
            "order_status": "SUCCESS",
            "created_at": "2024-03-16T14:22:00.834306Z",
            "updated_at": "2024-03-16T17:56:01.748118Z",
            "total_amount": 200
        }

### Add products to cart

    Endpoint: /api/v1/order-item/
    Method: POST
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "product": 1,
    "quantity": 1
    }
    Response: 
    {
    "product": 1,
    "quantity": 1
    }
    

    
### Update the product in cart

    Endpoint: /api/v1/order-item/1/
    Method: PATCH
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "quantity": 3
    }
    
    Response: 
    {
    "product": 1,
    "quantity": 3
    }
    

### Checkout Order

    Endpoint: /api/v1/payments/
    Method: POST
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "order": "2",
    "payment_mode": "CREDIT_CARD"
    }

    Response: 
    {
        "id": 2,
        "total_amount": "300.00",
        "payment_mode": "CREDIT_CARD",
        "payment_status": "PENDING",
        "created_at": "2024-03-16T18:36:42.608804Z",
        "updated_at": "2024-03-16T18:36:42.608832Z",
        "order": 2
    }

    

### Marking Payment as sucess (This can be a Payment Gateway API)

    Endpoint: /api/v1/payments/1/
    Method: PATCH
    Request Headers: Authorization: Bearer <access_token> (Access token obtained from login API)
    Data Payload:
    {
    "payment_status": "SUCCESS",
    }
    Response: 
    {
        "id": 1,
        "total_amount": "246.00",
        "payment_mode": "CREDIT_CARD",
        "payment_status": "SUCCESS",
        "created_at": "2024-03-16T17:17:59.253554Z",
        "updated_at": "2024-03-16T18:38:27.175201Z",
        "order": 1
    }
