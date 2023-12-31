# Theatre Service API Service

Theatre API Service is a Django-based RESTful API for managing plays, performances, actors and more. It provides endpoints for creating, updating, and retrieving thatre-related data, as well as user registration and order management.


## Introduction

Theatre API Service is designed to streamline the management of theatre-related data and user interactions. Whether you're developing an app for theatre, building a play reservation system, or just exploring Django REST APIs, this project provides a solid foundation.

### Features:
- CRUD operations for performances, plays, actors, genres, theatre halls and orders.
- Ticket validation based on cargo and seat availability.

## Installation

1. Clone the repository:

   ```
   https://github.com/maccarets/theatre-api-service.git
   ```
2. Create .env file and define environmental variables following .env.example.


3. Run command:
   ```
   docker-compose up --build
   ```
4. App will be available at: ```127.0.0.1:8000```

## Endpoints
   ```
   "theatre" : 
                "http://127.0.0.1:8000/api/theatre/genres/"
                "http://127.0.0.1:8000/api/theatre/actors/"
                "http://127.0.0.1:8000/api/theatre/plays/"
                "http://127.0.0.1:8000/api/theatre/theatre_halls/"
                "http://127.0.0.1:8000/api/theatre/performances/"
                "http://127.0.0.1:8000/api/theatre/reservations/"
   "user" : 
                "http://127.0.0.1:8000/api/user/register/"
                "http://127.0.0.1:8000/api/user/me/"
                "http://127.0.0.1:8000/api/user/token/"
                "http://127.0.0.1:8000/api/user/token/verify/"
                "http://127.0.0.1:8000/api/user/token/refresh/"
   "documentation": 
                "http://127.0.0.1:8000/api/swagger-ui/"
                "http://127.0.0.1:8000/api/redoc/"
   ```

## Schema
![img.png](img.png)

## Presentation
![img_1.png](img_1.png)