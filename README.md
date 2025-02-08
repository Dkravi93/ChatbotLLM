# Chatbot Project

This project is a chatbot API built with FastAPI, LangGraph, and PostgreSQL. It allows users to query product and supplier information, with added features like user authentication, analytics tracking, and recommendations.

## Features

- **User Authentication**: JWT-based authentication for secure and personalized interactions.
- **Product and Supplier Queries**: Users can query product and supplier data, with responses generated using an LLM.
- **Analytics Dashboard**: Tracks and visualizes user queries and popular products.
- **Recommendation System**: Suggests related products or suppliers based on user queries.

## Project Structure

/chatbot_project
│── /app
│ ├── /models # Database models
│ │ ├── product.py
│ │ ├── supplier.py
│ │ ├── user.py
│ │ ├── analytics.py
│ ├── /schemas # Pydantic schemas
│ │ ├── query.py
│ │ ├── user.py
│ ├── /services # Business logic and services
│ │ ├── query_service.py
│ │ ├── analytics.py
│ │ ├── recommendation.py
│ ├── /database # Database connection
│ │ ├── connection.py
│ ├── /routes # API routes
│ │ ├── query.py
│ │ ├── user.py
│ │ ├── analytics.py
│ │ ├── recommendation.py
│ ├── /utils # Utility functions
│ │ ├── logger.py
│ │ ├── auth.py
│ ├── main.py # FastAPI entry point
│── .env # Environment variables (including DB credentials)
│── requirements.txt # Python dependencies
│── README.md # Project documentation



## Setup Instructions

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/chatbot_project.git
cd chatbot_project
```

### 2. Set up the environment:

Create a `.env` file in the root of the project with the following variables:

```
DATABASE_URL=postgresql+asyncpg://postgres:<your_password>@localhost/chatbot_db
GROQ_API_KEY=<your_groq_api_key>
SECRET_KEY=<your_jwt_secret_key>
ALGORITHM=HS256
```

### 3.Install dependencies:

```
pip install -r requirements.txt

```

### 4. Run the application:

```
uvicorn app.main:app --reload

```


## Endpoints

### Authentication

* **POST** `/api/users/register`: Register a new user.
* **POST** `/api/users/login`: Login and receive a JWT token.

### Queries

* **POST** `/api/query`: Submit a query for products or suppliers and get a response.

### Analytics

* **GET** `/api/analytics`: View analytics data on user queries.

### Recommendations

* **GET** `/api/recommendations`: Get product recommendations based on user queries.
