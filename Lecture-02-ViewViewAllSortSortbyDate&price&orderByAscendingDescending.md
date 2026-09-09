# Expense Tracker API — FastAPI Tutorial

This tutorial introduces the basic API concepts used to build an **Expense Tracker API with FastAPI** and a simple JSON file (`expenses.json`) as a dummy database.

The main focus of this lecture is understanding how an API can **read expense data, retrieve a specific expense, and sort expenses using query parameters**.

> **Note:** CRUD is introduced conceptually in this tutorial. The provided code currently implements the **Read** operations and **sorting**. Create, Update, and Delete are part of the CRUD concept but are not implemented in the supplied code.

---

## 1. CRUD Operations

CRUD represents the four basic operations normally performed on data in an API or database.

| Operation | HTTP Method | Purpose |
|---|---|---|
| **Create** | `POST` | Add a new resource |
| **Read** | `GET` | Retrieve existing data |
| **Update** | `PUT` | Update an existing resource |
| **Delete** | `DELETE` | Remove an existing resource |

### CRUD in an Expense Tracker

For an expense application, these operations could look like:

```text
POST   /expenses          -> Create a new expense
GET    /expenses          -> Read all expenses
GET    /expenses/{id}     -> Read one specific expense
PUT    /expenses/{id}     -> Update an expense
DELETE /expenses/{id}     -> Delete an expense
```

In this lecture, the main implemented operations are:

```text
GET /view
GET /view/{expense_id}
GET /sort
```

The API reads data from `expenses.json`, so the file acts as a **dummy database** for learning purposes.

---

# 2. Expense Tracker API Using FastAPI

The project uses:

- **FastAPI** — to create the API
- **Python** — to write the backend logic
- **JSON** — to store sample expense data
- **Uvicorn** — to run the FastAPI application

The basic flow is:

```text
Client
  ↓
FastAPI API
  ↓
Python Function
  ↓
expenses.json
  ↓
Response to Client
```

The API loads data from the JSON file and returns it to the client.

---

# 3. Loading Data From `expenses.json`

The helper function below reads the JSON file and converts it into Python data.

```python
def load_data():
    with open("expenses.json", "r") as file:
        data = json.load(file)
    return data
```

### Why create `load_data()`?

Instead of writing the file-reading code repeatedly inside every API endpoint, we put it into one reusable function.

Whenever we need expense data, we can simply use:

```python
load_data()
```

This keeps the API code cleaner and easier to understand.

---

# 4. Read All Expenses — GET

The following endpoint returns all expense data.

```python
@app.get("/view")
def view_expense():
    return load_data()
```

Open:

```text
http://127.0.0.1:8000/view
```

### What happens?

1. Client sends a `GET` request to `/view`.
2. FastAPI calls `view_expense()`.
3. `load_data()` reads `expenses.json`.
4. The complete expense data is returned as the API response.

This is the **Read** part of CRUD.

---

# 5. Path Parameters

A **path parameter** is a variable part of a URL used to identify a specific resource.

Example:

```text
/view/E008
```

Here:

```text
E008
```

is the `expense_id`.

Path parameters are useful when we want to retrieve **one specific item** instead of returning every item.

## Why use an ID in the URL?

Suppose `expenses.json` contains many expenses. We do not want the user to search through every expense manually.

Instead, the user can request:

```text
/view/E001
```

and the API can directly look for that expense ID.

This makes the request clear and efficient conceptually, because the resource identifier is included directly in the URL.

---

# 6. Reading a Specific Expense Using a Path Parameter

```python
@app.get("/view/{expense_id}")
def view_specific_expense(
    expense_id: str = Path(
        ...,
        description="The ID of the expense to retrieve",
        example="E001"
    )
):
    data = load_data()

    if expense_id in data:
        return data[expense_id]
    else:
        raise HTTPException(status_code=404, detail="Expense not found")
```

Example request:

```text
http://127.0.0.1:8000/view/E008
```

### How it works

The URL contains:

```text
/view/{expense_id}
```

When the client requests:

```text
/view/E008
```

FastAPI puts `E008` into:

```python
expense_id
```

Then the code checks whether that ID exists:

```python
if expense_id in data:
```

If it exists:

```python
return data[expense_id]
```

If it does not exist, the API returns a `404 Not Found` error.

---

# 7. `Path()` Function in FastAPI

FastAPI provides the `Path()` function for adding validation and documentation information to path parameters.

Import it like this:

```python
from fastapi import Path
```

Then:

```python
expense_id: str = Path(
    ...,
    description="The ID of the expense to retrieve",
    example="E001"
)
```

### What does `...` mean?

In this context:

```python
Path(...)
```

means the parameter is **required**.

The `description` and `example` values help explain the API parameter in FastAPI's automatically generated API documentation.

For example:

```text
expense_id
The ID of the expense to retrieve
Example: E001
```

This makes the API easier for another developer to understand and use.

---

# 8. HTTP Status Codes

HTTP stands for **Hypertext Transfer Protocol**. It defines how clients and servers communicate over HTTP requests and responses.

An **HTTP status code** tells the client what happened to its request.

## Status Code Categories

| Range | Category | Meaning |
|---|---|---|
| `1XX` | Informational | Request/process information |
| `2XX` | Success | Request was successful |
| `3XX` | Redirection | Resource or request is being redirected |
| `4XX` | Client Error | Problem with the client request |
| `5XX` | Server Error | Problem on the server side |

## Important Status Codes

### `200 OK`

The request was successful.

Example:

```text
GET /view
```

returns the requested expense data successfully.

### `201 Created`

A new resource was successfully created.

This is commonly used after a successful `POST` request.

### `301 Moved Permanently`

The requested resource has permanently moved to another location.

### `302 Found`

The resource is temporarily available at another location.

### `400 Bad Request`

The request contains invalid data or syntax.

### `401 Unauthorized`

Authentication is required or the authentication information is invalid.

### `404 Not Found`

The requested resource does not exist.

In this project, it is used when an expense ID cannot be found:

```python
raise HTTPException(
    status_code=404,
    detail="Expense not found"
)
```

### `500 Internal Server Error`

A general server-side error occurred.

### `503 Service Unavailable`

The server is currently unavailable, overloaded, or unable to handle the request.

---

# 9. `HTTPException` in FastAPI

FastAPI provides `HTTPException` for returning an HTTP error response from an endpoint.

Import it with:

```python
from fastapi import HTTPException
```

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Expense not found"
)
```

This tells the client:

```text
Status Code: 404
Detail: Expense not found
```

Instead of returning normal data, the API explicitly tells the client that the requested resource was not found.

---

# 10. Query Parameters

A **query parameter** is optional data added to the end of a URL as a key-value pair.

Example:

```text
/sort?sorted_by=amount&order=asc
```

Here there are two query parameters:

```text
sorted_by = amount
order     = asc
```

The `?` starts the query string, and `&` separates multiple query parameters.

Query parameters are useful when the client wants to control **how the API should return data** without changing the main resource path.

For example:

```text
/sort?sorted_by=amount&order=asc
```

means:

> Sort the expenses by `amount` in ascending order.

---

# 11. Sorting Database Data

The API can sort expenses based on a selected field.

For example:

```text
amount
```

can be sorted from low to high or high to low.

A date can also be sorted:

```text
date
```

This is useful for showing things such as:

```text
Latest expense first
Oldest expense first
Lowest amount first
Highest amount first
```

---

# 12. Multiple Query Parameters

The `/sort` endpoint accepts two query parameters:

```text
sorted_by
order
```

Example:

```text
http://127.0.0.1:8000/sort?sorted_by=amount&order=asc
```

This can be read as:

```text
sorted_by = amount
order     = asc
```

Other examples:

```text
http://127.0.0.1:8000/sort?sorted_by=amount&order=desc
```

Sort by amount in descending order.

```text
http://127.0.0.1:8000/sort?sorted_by=date&order=asc
```

Sort by date in ascending order.

```text
http://127.0.0.1:8000/sort?sorted_by=date&order=desc
```

Sort by date in descending order.

---

# 13. Sorting Implementation

The FastAPI endpoint is:

```python
@app.get("/sort")
def view_sorted_expense(sorted_by: str, order: str):
    data = load_data()
    sorted_data = list(data.values())

    if order == "asc":
        sorted_data.sort(
            key=lambda x: x[sorted_by],
            reverse=False
        )

    elif order == "desc":
        sorted_data.sort(
            key=lambda x: x[sorted_by],
            reverse=True
        )

    return sorted_data
```

## Step 1 — Load the data

```python
data = load_data()
```

The JSON file is loaded into Python.

## Step 2 — Get the expense values

```python
sorted_data = list(data.values())
```

If the JSON data is structured using expense IDs as keys, `data.values()` gives the actual expense objects.

`list()` converts those values into a list so Python's `.sort()` method can be used.

## Step 3 — Sort in ascending order

```python
if order == "asc":
    sorted_data.sort(
        key=lambda x: x[sorted_by],
        reverse=False
    )
```

`sorted_by` decides which field is used for sorting.

For example:

```text
sorted_by=amount
```

means:

```python
x["amount"]
```

`reverse=False` keeps the sort in ascending order.

## Step 4 — Sort in descending order

```python
elif order == "desc":
    sorted_data.sort(
        key=lambda x: x[sorted_by],
        reverse=True
    )
```

`reverse=True` changes the order to descending.

---

# 14. `lambda` Used in Sorting

The expression:

```python
lambda x: x[sorted_by]
```

is a small anonymous function.

Conceptually, it means:

```text
For each expense,
use the value of the selected field as the sorting value.
```

For example, if:

```text
sorted_by = "amount"
```

then:

```python
lambda x: x[sorted_by]
```

acts like:

```python
lambda x: x["amount"]
```

This lets the same endpoint sort by different fields without writing a separate endpoint for every field.

---

# 15. Complete Code Used in This Tutorial

```python
# InjamTanvir (INJAM UL HAQUE)
# Expense Tracker API using FastAPI connected with Dummy Database (expenses.json)
# and CRUD Concepts

import json
from fastapi import FastAPI, HTTPException, Path


def load_data():
    # Load the data from the expenses.json file
    with open("expenses.json", "r") as file:
        # Read the JSON file and convert it into Python data
        data = json.load(file)
    return data


# Create a FastAPI instance named app.
# This object is used to define API endpoints and handle requests.
app = FastAPI()


@app.get("/view")
# Load all the expenses from the database
# URL: http://127.0.0.1:8000/view
def view_expense():
    return load_data()


# Use a path parameter to get a specific expense by ID
@app.get("/view/{expense_id}")
# URL example: http://127.0.0.1:8000/view/E008
def view_specific_expense(
    expense_id: str = Path(
        ...,
        description="The ID of the expense to retrieve",
        example="E001"
    )
):
    # Load the data from expenses.json
    data = load_data()

    # Check whether the expense ID exists in the data
    if expense_id in data:
        # Return the matching expense
        return data[expense_id]
    else:
        # Return a 404 error when the expense does not exist
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )


@app.get("/sort")
# Sort expenses using the query parameters sorted_by and order
# URL example:
# http://127.0.0.1:8000/sort?sorted_by=amount&order=desc
def view_sorted_expense(sorted_by: str, order: str):
    # Load the data from expenses.json
    data = load_data()

    # Convert the expense values into a list so it can be sorted
    sorted_data = list(data.values())

    # Ascending order
    if order == "asc":
        sorted_data.sort(
            key=lambda x: x[sorted_by],
            reverse=False
        )

    # Descending order
    elif order == "desc":
        sorted_data.sort(
            key=lambda x: x[sorted_by],
            reverse=True
        )

    return sorted_data


# Another way to write the sorting function:
#
# def get_value(expense):
#     return expense[sorted_by]
#
# if order == "asc":
#     sorted_data.sort(key=get_value)
```

---

# 16. Run the FastAPI Application

Use Uvicorn to start the development server:

```bash
uvicorn main:app --reload
```

### Meaning of the command

```text
uvicorn   -> ASGI server used to run FastAPI
main      -> Python file named main.py
app       -> FastAPI instance inside main.py
--reload  -> Restart the server automatically when code changes
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 17. API Endpoints From This Lecture

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/view` | View all expenses |
| `GET` | `/view/{expense_id}` | View one expense by ID |
| `GET` | `/sort?sorted_by=amount&order=asc` | Sort by amount ascending |
| `GET` | `/sort?sorted_by=amount&order=desc` | Sort by amount descending |
| `GET` | `/sort?sorted_by=date&order=asc` | Sort by date ascending |
| `GET` | `/sort?sorted_by=date&order=desc` | Sort by date descending |

---

# 18. Important Concepts Learned

### CRUD

```text
Create -> POST
Read   -> GET
Update -> PUT
Delete -> DELETE
```

### Path Parameter

Used to identify a specific resource:

```text
/view/E008
```

### Query Parameter

Used to pass optional/control information:

```text
/sort?sorted_by=amount&order=asc
```

### `Path()`

Used to define and document a path parameter.

### `HTTPException`

Used to return API errors with an HTTP status code.

### HTTP Status Codes

Used to communicate the result of a request to the client.

### Sorting

Allows the client to request data in a particular order, such as ascending or descending by amount or date.

---

# 19. One Important Distinction

This tutorial uses:

```text
expenses.json
```

as a **dummy database** for learning.

The API is therefore reading from a file rather than from a real database such as PostgreSQL or MySQL.

The same API concepts—CRUD, path parameters, query parameters, status codes, and sorting—are also used when the backend is connected to a real database. The database layer changes, but the HTTP/API concepts remain important.

---

## Author

**Injam Tanvir (Injam Ul Haque)**

FastAPI / API Concepts Tutorial — Lecture 02
