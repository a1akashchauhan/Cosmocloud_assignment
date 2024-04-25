# FastAPI Application with Redis Rate Limiting and MongoDB

This FastAPI application provides CRUD operations for managing student records, with rate limiting implemented using Redis and data storage handled by MongoDB.

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker
- Python 3.x

## Setting up Redis with Docker

You can use Docker to quickly set up a Redis instance:

```bash
docker run -d --name redis-instance -p 6379:6379 redis
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd <project-directory>
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the FastAPI application, run the following command:

```bash
uvicorn main:app --reload
```

The application will start and be accessible at `http://localhost:8000`.

## Endpoints

- `POST /students`: Create a new student record.
- `GET /students`: Retrieve a list of students based on optional query parameters.
- `GET /students/{id}`: Retrieve details of a specific student by ID.
- `PATCH /students/{id}`: Update details of a specific student by ID.
- `DELETE /students/{id}`: Delete a student record by ID.

## Rate Limiting

Rate limiting is implemented using Redis to restrict the number of requests per user. The rate limit is set to 5 requests per user per day.

## Add these URI/PORT

- `MONGO_URI`: MongoDB connection URI.
- `REDIS_HOST`: Redis host address.
- `REDIS_PORT`: Redis port number.

## Usage

To use the application, ensure you include the `user_id` header in your requests. This header is used for rate limiting purposes.

```http
GET /students
user_id: <user-id>
```

