# Lecture 03 — Create, Update & Delete with FastAPI

**InjamTanvir (INJAM UL HAQUE)**

This lecture continues the **Expense Tracker API** project from the previous lecture.

In this lecture, we work with the same **dummy database (`expenses.json`)** and learn how to perform:

- **Create → POST**
- **Update → PUT**
- **Delete → DELETE**

We also learn how to use **Pydantic for data validation** and how to test these requests using **FastAPI Swagger UI**.

> **Scope of this lecture:** We are using `expenses.json` as a dummy database only for learning. Real database connection and deployment/hosting are **not covered here** and will be discussed later (Lecture 5).

---

# 1. CRUD

CRUD means the four common operations performed on data:

| Operation | HTTP Method | Purpose |
|---|---|---|
| Create | `POST` | Create a new expense |
| Read | `GET` | Read existing expense data |
| Update | `PUT` | Update an existing expense |
| Delete | `DELETE` | Delete an expense |

In the previous lecture, we mainly worked with **GET** requests.

In this lecture, we implement the remaining three operations using the dummy JSON data.

```text
POST   → Create
PUT    → Update
DELETE → Delete
```

---

# 2. Dummy Database — `expenses.json`

For now, `expenses.json` is acting like our database.

```text
FastAPI
   ↓
Python Function
   ↓
expenses.json
```

So, when we create, update, or delete data, the changes are actually written back to this JSON file.

This is useful for learning the API concepts without introducing a real database yet.

---

# 3. Imports

```python
import json
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Annotated, Optional
```

### Why do we need these?

### `json`

JSON file theke data **read** and **write** korar jonno use korchi.

### `FastAPI`

FastAPI application create and API endpoint define korar jonno.

### `HTTPException`

Jokhon kono request properly process kora possible na, tokhon proper HTTP status code and message return korar jonno use kori.

### `Path`

Path parameter-er documentation and validation information add korar jonno.

### `BaseModel` and `Field`

Pydantic-er মাধ্যমে input data validation korar jonno use kori.

### `Annotated`

Type-er sathe additional validation/documentation information add korte help kore.

### `Optional`

Update request-er khetre sob field provide kora lagbe na. Tai optional field define korar jonno `Optional` use kori.

---

# 4. Loading Data from `expenses.json`

```python
def load_data():
    with open("expenses.json", "r") as file:
        data = json.load(file)
    return data
```

### What is happening here?

`expenses.json` file-ta **read mode (`"r"`)** e open hocche.

```python
json.load(file)
```

JSON file-er data Python data structure-e convert kore.

### Why make a separate function?

Same code repeatedly na likhe amra ekta reusable function banalam.

Jokhon data lagbe:

```python
load_data()
```

---

# 5. Saving Data to `expenses.json`

Create, Update, Delete korar por data file-e save korte hobe.

Tai `save_data()` function use kori:

```python
def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)
```

### Why use `"w"`?

`"w"` means **write mode**.

Existing JSON data update kore abar file-er moddhe save korar jonno write mode use kori.

### Why `indent=4`?

```python
json.dump(data, file, indent=4)
```

`indent=4` JSON file-ke nicely formatted kore rakhe, tai human-readable hoy.

---

# 6. Pydantic Data Validation

Create request-e user multiple fields পাঠাবে.

For example:

```text
id
name
amount
date
category
description
```

User je data pathacche, seta expected format-er kina check korar jonno **Pydantic** use kori.

Pydantic validation korar jonno `BaseModel` use kore ekta class create kori.

---

# 7. `Expense` Validation Model

```python
class Expense(BaseModel):
    id: Annotated[str, Field(..., description="The unique ID of the expense", example="E001")]
    name: Annotated[str, Field(..., description="The name of the expense", example="Lunch")]
    amount: Annotated[float, Field(..., description="The amount of the expense", example=100.0)]
    date: Annotated[str, Field(..., description="The date of the expense", example="2023-01-01")]
    category: Annotated[str, Field(..., description="The category of the expense", example="Food")]
    description: Annotated[str, Field(..., description="The description of the expense", example="Lunch at restaurant")]
```

### Why create this class?

Eta amader **input validation model**.

For example, `amount` should be a `float`:

```python
amount: float
```

So user wrong type-er data dile Pydantic validation error dite parbe.

---

# 8. `Field()` — Description and Example

Example:

```python
Field(
    ...,
    description="The unique ID of the expense",
    example="E001"
)
```

### `...`

`...` means the field is **required**.

### `description`

Field-ta ki represent kore, seta explain kore.

### `example`

Swagger UI-te user-er jonno example value show kore.

So, `Field()` mainly validation-er sathe **documentation information** o provide korte help kore.

---

# 9. Create — `POST`

Create operation-er jonno `POST` request use kori.

```python
@app.post("/create")
def create_expense(expense: Expense):
    data = load_data()

    if expense.id in data:
        raise HTTPException(status_code=400, detail="Expense ID already exists")

    data[expense.id] = expense.model_dump(exclude=["id"])
    save_data(data)
```

### Step-by-step

### Step 1 — Receive input

```python
def create_expense(expense: Expense):
```

`expense` is an object of the Pydantic `Expense` model.

So request data first validation-er moddhe jay.

### Step 2 — Load existing data

```python
data = load_data()
```

Current JSON data load kori.

### Step 3 — Check duplicate ID

```python
if expense.id in data:
```

Same ID already exist kore kina check kori.

Already thakle:

```python
raise HTTPException(status_code=400, detail="Expense ID already exists")
```

`400 Bad Request` return kori.

### Step 4 — Save new expense

```python
data[expense.id] = expense.model_dump(exclude=["id"])
```

`model_dump()` Pydantic model-ke Python dictionary-te convert kore.

We use:

```python
exclude=["id"]
```

because JSON data-te `id` already key hisebe use hocche.

Conceptually:

```text
E001 → {name, amount, date, category, description}
```

Tai value-er moddhe abar `id` store korar dorkar nai.

### Step 5 — Save changes

```python
save_data(data)
```

Updated data abar `expenses.json` file-e save hoy.

---

# 10. Why Pydantic is Important for POST

Without validation, user je kono unexpected data পাঠাতে পারে.

Pydantic ensure kore je input data expected structure-er sathe match kore.

For example:

```text
name      → string
amount    → float
category  → string
```

Tai **Create operation-er age data validation** important.

---

# 11. Update — `PUT`

Existing data modify korar jonno `PUT` request use kori.

Endpoint:

```python
@app.put("/edit/{expense_id}")
```

Example:

```text
/edit/E001
```

Ekhane `E001` holo kon expense-ta update korte hobe tar ID.

---

# 12. `ExpenseUpdate` Model

Update request-e normally sob field change korte hoy na.

Suppose user only amount change korte chay.

Tahole name, category, description etc. abar pathanor dorkar nai.

Tai update-er jonno separate model use kori:

```python
class ExpenseUpdate(BaseModel):
    name: Annotated[Optional[str], Field(description="The name of the expense", example="Lunch", default=None)]
    amount: Annotated[Optional[float], Field(description="The amount of the expense", example=100.0, default=None)]
    date: Annotated[Optional[str], Field(description="The date of the expense", example="2023-01-01", default=None)]
    category: Annotated[Optional[str], Field(description="The category of the expense", example="Food", default=None)]
    description: Annotated[Optional[str], Field(description="The description of the expense", example="Lunch at restaurant", default=None)]
```

### Why `Optional`?

Update request-e **all fields mandatory na**.

For example, only this data pathano possible:

```json
{
    "amount": 250.0
}
```

Other fields provide kora hoyni, so they should not be changed.

---

# 13. Update Function

```python
@app.put("/edit/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate):
    data = load_data()

    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")

    data[expense_id].update(
        expense.model_dump(exclude_unset=True)
    )

    save_data(data)

    return {"message": "Expense updated successfully"}
```

### Step 1 — Receive ID and update data

```python
def update_expense(expense_id: str, expense: ExpenseUpdate):
```

Duita jinis receive korchi:

```text
expense_id → kon data update hobe
expense     → ki ki data update hobe
```

### Step 2 — Check ID

```python
if expense_id not in data:
```

Expense na thakle:

```python
raise HTTPException(status_code=404, detail="Expense not found")
```

### Step 3 — Update only provided fields

```python
expense.model_dump(exclude_unset=True)
```

**`exclude_unset=True` is very important here.**

Eta sudhu user je field-gulo request-e actually diyeche, segulo include kore.

Example request:

```json
{
    "amount": 300.0
}
```

Tahole update hobe only:

```text
amount → 300.0
```

Other field unnecessaryভাবে `None` diye overwrite hobe na.

### Step 4 — Save data

```python
save_data(data)
```

Updated data JSON file-e save kori.

---

# 14. Delete — `DELETE`

Data remove korar jonno `DELETE` request use kori.

```python
@app.delete("/delete/{expense_id}")
def delete_expense(expense_id: str):
    data = load_data()

    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")

    del data[expense_id]
    save_data(data)

    return {"message": "Expense deleted successfully"}
```

### Step 1 — Receive ID

```python
/delete/{expense_id}
```

Example:

```text
/delete/E001
```

### Step 2 — Check whether ID exists

```python
if expense_id not in data:
```

ID na thakle:

```python
raise HTTPException(status_code=404, detail="Expense not found")
```

### Step 3 — Delete

```python
del data[expense_id]
```

Python dictionary theke specific expense remove kore.

### Step 4 — Save the changed data

```python
save_data(data)
```

Delete korar por updated dictionary abar JSON file-e save hoy.

---

# 15. Why `save_data()` is Necessary After POST, PUT and DELETE

Ei three operation-e data change hocche.

```text
POST   → New data add
PUT    → Existing data change
DELETE → Existing data remove
```

Change korar por jodi `save_data(data)` call na kori, tahole change memory-te thakte pare but JSON file-e permanently save hobe na.

So flow-ta:

```text
Load JSON
   ↓
Modify Python data
   ↓
Save JSON
```

---

# 16. Swagger UI দিয়ে Testing

FastAPI automatically interactive API documentation provide kore.

Application run korar por browser-e open korte pari:

```text
http://127.0.0.1:8000/docs
```

Eikhane Swagger UI te API endpoints dekhte parbo.

### Why Swagger is useful in this lecture?

Postman বা separate frontend chara amra directly API test korte pari.

Especially POST, PUT and DELETE request-er khetre Swagger diye:

- Request body provide kora jay
- Path parameter set kora jay
- API execute kora jay
- Response dekha jay
- Validation error dekha jay
- Error status code test kora jay

---

# 17. Testing POST in Swagger

Swagger-e:

```text
POST /create
```

select kore **Try it out** click korte parbo.

Example request body:

```json
{
  "id": "E009",
  "name": "Lunch",
  "amount": 250.0,
  "date": "2023-01-01",
  "category": "Food",
  "description": "Lunch at restaurant"
}
```

Execute korle FastAPI Pydantic model-er maddhome input validate korbe.

Validation successful hole data `expenses.json`-e add hobe.

---

# 18. Testing PUT in Swagger

Swagger-e:

```text
PUT /edit/{expense_id}
```

Example path parameter:

```text
E009
```

Request body only required field-gulo contain korte pare.

Example:

```json
{
  "amount": 300.0
}
```

Then API execute korle only `amount` update hobe because:

```python
exclude_unset=True
```

use kora hoyeche.

---

# 19. Testing DELETE in Swagger

Swagger-e:

```text
DELETE /delete/{expense_id}
```

Example:

```text
E009
```

Execute korle oi ID-er data delete hobe.

Then `expenses.json` check korle data-ta আর thakbe na.

---

# 20. Important HTTP Methods Used in This Lecture

```text
POST
 ↓
Create new resource

PUT
 ↓
Update existing resource

DELETE
 ↓
Delete existing resource
```

Previous lecture-er:

```text
GET
 ↓
Read resource
```

So together:

```text
GET    → Read
POST   → Create
PUT    → Update
DELETE → Delete
```

---

# 21. Complete Code Used in Lecture 03

```python
import json
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Annotated, Optional


def load_data():
    with open("expenses.json", "r") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)


# Validation korar jonno Class
class Expense(BaseModel):
    id: Annotated[str, Field(..., description="The unique ID of the expense", example="E001")]
    name: Annotated[str, Field(..., description="The name of the expense", example="Lunch")]
    amount: Annotated[float, Field(..., description="The amount of the expense", example=100.0)]
    date: Annotated[str, Field(..., description="The date of the expense", example="2023-01-01")]
    category: Annotated[str, Field(..., description="The category of the expense", example="Food")]
    description: Annotated[str, Field(..., description="The description of the expense", example="Lunch at restaurant")]


# Used for update request, jekhane amra optional field use korbo,
# karon update request e sob gulo field thakbe na.
class ExpenseUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(description="The name of the expense", example="Lunch", default=None)
    ]
    amount: Annotated[
        Optional[float],
        Field(description="The amount of the expense", example=100.0, default=None)
    ]
    date: Annotated[
        Optional[str],
        Field(description="The date of the expense", example="2023-01-01", default=None)
    ]
    category: Annotated[
        Optional[str],
        Field(description="The category of the expense", example="Food", default=None)
    ]
    description: Annotated[
        Optional[str],
        Field(description="The description of the expense", example="Lunch at restaurant", default=None)
    ]


app = FastAPI()


# -------------------- CREATE --------------------

# POST request diye new expense create korbo.
# Pydantic Expense model input data validate korbe.
@app.post("/create")
def create_expense(expense: Expense):
    data = load_data()

    # Same expense ID already exist korle duplicate data create korbo na.
    if expense.id in data:
        raise HTTPException(status_code=400, detail="Expense ID already exists")

    # model_dump() Pydantic object ke dictionary te convert kore.
    # id exclude korchi because id JSON dictionary-r key hisebe use hocche.
    data[expense.id] = expense.model_dump(exclude=["id"])

    # New data JSON file-e save korchi.
    save_data(data)

    return {"message": "Expense created successfully"}


# -------------------- UPDATE --------------------

# PUT request diye existing expense update korbo.
# expense_id path parameter diye kon expense update hobe seta identify korbo.
@app.put("/edit/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate):
    data = load_data()

    # Requested expense ID data-te na thakle 404 error.
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")

    # exclude_unset=True means only user je fields request-e diyeche,
    # sudhu oi fields-gulo update hobe.
    data[expense_id].update(
        expense.model_dump(exclude_unset=True)
    )

    # Updated data JSON file-e save kori.
    save_data(data)

    return {"message": "Expense updated successfully"}


# -------------------- DELETE --------------------

# DELETE request diye specific expense remove korbo.
@app.delete("/delete/{expense_id}")
def delete_expense(expense_id: str):
    data = load_data()

    # Expense ID exist na korle 404 error return korbo.
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Dictionary theke specific expense delete korchi.
    del data[expense_id]

    # Delete korar por updated data JSON file-e save korte hobe.
    save_data(data)

    return {"message": "Expense deleted successfully"}
```

---

# 22. Run the FastAPI Application

Use Uvicorn to run the application:

```bash
uvicorn main:app --reload
```

Then Swagger UI open korar jonno:

```text
http://127.0.0.1:8000/docs
```

---

# 23. Lecture Summary

Ei lecture-e amra dummy JSON database use kore FastAPI-r CRUD-er remaining three operations implement korechi.

```text
POST
 ↓
Create new expense

PUT
 ↓
Update existing expense

DELETE
 ↓
Delete expense
```

Important concepts:

```text
Pydantic BaseModel
        ↓
Input validation

ExpenseUpdate + Optional
        ↓
Partial update data structure

model_dump()
        ↓
Pydantic model → dictionary

exclude=["id"]
        ↓
ID ke JSON value-r moddhe duplicate na rakha

exclude_unset=True
        ↓
Only provided update fields change kora

HTTPException
        ↓
Proper error status + message return

Swagger UI
        ↓
POST / PUT / DELETE directly test kora
```

> **Not covered in Lecture 03:** Real database connection, SQLAlchemy, PostgreSQL, MySQL, SQLite database integration, and API deployment/hosting. These topics are planned for **Lecture 5**.
