# Python - Flask - FastAPI Tutorial

A beginner-friendly introduction to **APIs**, **backend communication**, **database access**, **endpoints**, and how Python frameworks such as **Flask** and **FastAPI** are used to build APIs.

---

## 1. What is an API?

**API** stands for:

> **Application Programming Interface**

An API is a communication interface that allows one software application to request data or perform actions through another software application without directly accessing its internal implementation or database.

### Simple Example: Restaurant Analogy

Think about a restaurant:

```text
Customer  →  Waiter  →  Chef
              API
```

- **Customer** = Frontend / Client
- **Waiter** = API
- **Chef** = Backend / Business Logic
- **Kitchen storage** = Database

Suppose a customer orders:

> "Give me a chicken burger."

The customer does not enter the kitchen and talk directly to the chef. Instead:

```text
Customer
   ↓
Places Order
   ↓
Waiter (API)
   ↓
Chef (Backend)
   ↓
Prepares Food
   ↓
Waiter (API)
   ↓
Customer
```

The waiter takes the customer's request to the chef and brings the result back to the customer.

In a software system, an API works in a similar way.

---

## 2. API and Database

A common backend architecture looks like this:

```text
Frontend / Client
       ↓
      API
       ↓
    Backend
       ↓
   Database
```

The frontend normally **does not directly access the database**.

Instead, it sends a request to an API. The backend receives the request, checks permissions, performs the required operation, communicates with the database, and returns a response.

### Why not allow the frontend to access the database directly?

Direct database access from a client would create serious security and design problems. The backend/API can instead control:

- Authentication
- Authorization
- Validation
- Business logic
- Database operations
- Error handling
- Data formatting
- Rate limiting and other security controls

Therefore, the database remains behind the backend/API layer.

---

# 3. What is an API Endpoint?

An **endpoint** is a specific URL exposed by an API for performing a particular operation.

For example:

```text
GET /users
GET /products
POST /orders
DELETE /users/10
```

Each endpoint represents a particular resource or task.

In a Flask or FastAPI application, an endpoint is commonly connected to a function that handles the incoming request.

Example conceptually:

```python
def view_users():
    # Get users from database
    # Return users to client
    pass
```

The function is associated with an API route, such as:

```text
GET /users
```

So, you can think of it as:

```text
API Endpoint → Function → Task
```

---

# 4. Common API Operations

Many web APIs follow the **CRUD** pattern.

CRUD means:

| Operation | Meaning | Common HTTP Method |
|---|---|---|
| Create | Add new data | `POST` |
| Read | View/retrieve data | `GET` |
| Update | Modify existing data | `PUT` / `PATCH` |
| Delete | Remove data | `DELETE` |

Example for a user resource:

```text
GET    /users          → View users
GET    /users/10       → View user 10
POST   /users          → Create a user
PUT    /users/10       → Update user 10
DELETE /users/10       → Delete user 10
```

### Important

An endpoint does **not automatically mean that every user can perform every operation**.

The backend can determine what a particular user is allowed to do.

For example:

```text
Normal User
   ↓
GET /products       ✅ Allowed
DELETE /products/5  ❌ Not Allowed

Admin
   ↓
GET /products       ✅ Allowed
DELETE /products/5  ✅ Allowed
```

This is called **authorization**.

---

# 5. Authentication vs Authorization

These two concepts are important when building APIs.

## Authentication

Authentication answers:

> **Who are you?**

For example, a user logs in with:

```text
Email + Password
```

The backend verifies the identity.

## Authorization

Authorization answers:

> **What are you allowed to do?**

For example:

```text
User
 ├── View products ✅
 ├── Create order ✅
 └── Delete products ❌

Admin
 ├── View products ✅
 ├── Create order ✅
 └── Delete products ✅
```

An API should check authorization before allowing sensitive operations.

---

# 6. Complete Request Flow

A typical web, Android, or iOS application can work like this:

```text
              ┌──────────────┐
              │   Frontend   │
              │ Web / Mobile │
              └──────┬───────┘
                     │
                     │ API Request
                     ↓
              ┌──────────────┐
              │     API      │
              │   Endpoint   │
              └──────┬───────┘
                     │
                     ↓
              ┌──────────────┐
              │   Backend    │
              │ Business     │
              │ Logic        │
              └──────┬───────┘
                     │
                     ↓
              ┌──────────────┐
              │   Database   │
              └──────┬───────┘
                     │
                     │ Data
                     ↓
              ┌──────────────┐
              │   Backend    │
              └──────┬───────┘
                     │
                     │ API Response
                     ↓
              ┌──────────────┐
              │   Frontend   │
              └──────────────┘
```

### Step-by-step

1. The user performs an action in the frontend.
2. The frontend sends an API request.
3. The API receives the request.
4. The backend validates the request.
5. Authentication/authorization checks may be performed.
6. The backend runs the required business logic.
7. The backend communicates with the database if necessary.
8. The database returns the requested data or confirms the operation.
9. The backend creates an API response.
10. The frontend receives and displays the result.

---

# 7. One Backend, Multiple Frontends

One major advantage of APIs is that different clients can use the same backend.

For example:

```text
             ┌─────────────┐
             │ Web App     │
             └──────┬──────┘
                    │
             ┌──────▼──────┐
             │             │
             │     API     │
             │             │
             └──────┬──────┘
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
    ┌──────────┐        ┌──────────┐
    │ Backend  │───────→│ Database │
    └──────────┘        └──────────┘
          ↑
          │
    ┌─────┴──────┐
    │ Mobile App │
    └────────────┘
```

The frontend technologies may be different:

```text
Web       → HTML/CSS/JavaScript/React/etc.
Android   → Kotlin/Java/Flutter/etc.
iOS       → Swift/Flutter/etc.
```

But they can all communicate with the same backend through APIs.

---

# 8. Real-World Example: Airline Ticket Booking

Imagine an airline such as **Biman Bangladesh Airlines** provides booking functionality through its systems.

A third-party travel platform such as **Trip.com** or another booking service may need to communicate with airline systems through APIs, subject to the airline's integrations, agreements, and access rules.

Conceptually:

```text
Customer
   ↓
Trip / Travel Website
   ↓
Travel Platform API
   ↓
Airline / Booking System API
   ↓
Flight Database / Reservation System
   ↓
Available Flights
   ↓
API Response
   ↓
Travel Website
   ↓
Customer
```

The third-party application does not need to directly manipulate the airline's database. It communicates through supported interfaces/APIs.

This general pattern is also common for many services, such as:

- Payment gateways
- Maps
- Food delivery
- Ride sharing
- Hotel booking
- Shipping
- Social media integrations
- Cloud services

---

# 9. Example API Request

Suppose our backend provides this endpoint:

```text
GET /products
```

The frontend sends:

```http
GET /products
```

The backend may query the database:

```sql
SELECT * FROM products;
```

The backend then returns data, often using **JSON**:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Keyboard",
      "price": 2500
    },
    {
      "id": 2,
      "name": "Mouse",
      "price": 1200
    }
  ]
}
```

The frontend can then display these products to the user.

---

# 10. Example: Creating an Order

A customer selects a product and presses **Buy Now**.

The frontend could send:

```http
POST /orders
```

with JSON data such as:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

The backend may then:

```text
Receive Request
      ↓
Validate Data
      ↓
Check User Authentication
      ↓
Check Product Availability
      ↓
Calculate Price
      ↓
Create Order in Database
      ↓
Return Response
```

Example response:

```json
{
  "message": "Order created successfully",
  "order_id": 1025,
  "status": "confirmed"
}
```

---

# 11. HTTP Methods

The most commonly used HTTP methods in REST-style APIs are:

### GET
Used to retrieve information.

```text
GET /products
```

### POST
Used to create/send new data.

```text
POST /products
```

### PUT
Usually used to replace/update an existing resource.

```text
PUT /products/5
```

### PATCH
Usually used to partially update an existing resource.

```text
PATCH /products/5
```

### DELETE
Used to delete a resource.

```text
DELETE /products/5
```

---

# 12. Flask and FastAPI

Python provides several frameworks for building APIs. Two popular choices are **Flask** and **FastAPI**.

## Flask

Flask is a lightweight and flexible Python web framework.

Example:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Hello World"}

if __name__ == "__main__":
    app.run(debug=True)
```

The endpoint is:

```text
GET /hello
```

## FastAPI

FastAPI is a modern Python framework designed for building APIs using Python type hints.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello World"}
```

The endpoint is:

```text
GET /hello
```

FastAPI can also automatically generate interactive API documentation.

---

# 13. Flask vs FastAPI: Basic Idea

| Feature | Flask | FastAPI |
|---|---|---|
| Language | Python | Python |
| Type hints | Supported | Core to the framework's design |
| API development | Very flexible | API-focused |
| Automatic validation | Requires additional tools/libraries for many cases | Strong support through type hints and Pydantic-based models |
| Automatic API docs | Requires additional setup/tools | Built in |
| Learning curve | Beginner-friendly | Beginner-friendly with some modern Python concepts |
| Async support | Available, but Flask's model differs | Strong async support |
| Use cases | Web apps, APIs, flexible services | APIs, backend services, modern web/mobile backends |

Both can be excellent choices. The right choice depends on project requirements, team experience, architecture, and ecosystem.

---

# 14. API Is the Communication Layer

A useful way to remember the architecture is:

```text
Frontend
   │
   │ API Request
   ↓
Backend / API
   │
   │ Database Query
   ↓
Database
   │
   │ Data
   ↓
Backend / API
   │
   │ API Response
   ↓
Frontend
```

The API acts as the controlled communication layer between the client and backend services.


# 15. FastAPI Automatic API Documentation

One useful feature of **FastAPI** is that it automatically generates interactive API documentation from your API code.

For example, after starting a FastAPI application locally:

```text
http://127.0.0.1:8000/docs
```

you can open the URL in your browser to view and test your API endpoints through an interactive documentation page.

### Example FastAPI code

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello World"}
```

Start the application, then open:

```text
http://127.0.0.1:8000/docs
```

You will see a documentation interface where the `/hello` endpoint is listed and can be tested.

### Why this is useful

Instead of manually creating a separate documentation page for every endpoint, FastAPI can generate documentation based on the API definitions in your code.

The interactive documentation is especially useful while learning and developing APIs because you can:

```text
See available endpoints
        ↓
Choose an endpoint
        ↓
See HTTP method
        ↓
See parameters / request body
        ↓
Send a test request
        ↓
See the server response
```

FastAPI also provides an alternative OpenAPI-based documentation interface at:

```text
http://127.0.0.1:8000/redoc
```
---
