# InjamTanvir(INJAM UL HAQUE)

import json
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field # Used for data validation and serialization
from typing import Annotated, Optional  # Used for type hinting and validation # Optional is used to indicate that a field is optional and may not be present in the input data.

def load_data():
    with open("expenses.json", "r") as file:  
        data = json.load(file)
    return data


def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4) # josn.dump() function is used to write the data to the file in JSON format. The indent parameter is used to format the JSON data with indentation for better readability.


# For Validation Class
class Expense(BaseModel):
    id: Annotated[str, Field(..., description="The unique ID of the expense", example='E001')]  # Annotated is used to provide additional metadata for the field, such as description and example.
    name: Annotated[str, Field(..., description="The name of the expense", example='Lunch')]
    amount: Annotated[float, Field(..., description="The amount of the expense", example=100.0)]
    date: Annotated[str, Field(..., description="The date of the expense", example='2023-01-01')]
    category: Annotated[str, Field(..., description="The category of the expense", example='Food')]
    description: Annotated[str, Field(..., description="The description of the expense", example='Lunch at restaurant')]

# Used for update request, wherever optional field needs to use, Cause, update request doesn't need all field. That's why Optional type have to use.
class ExpenseUpdate(BaseModel):
    name: Annotated[Optional[str], Field(description="The name of the expense", example='Lunch', default=None)]    # Default value None means that if the field is not provided in the input data, it will be set to None. This is useful for update requests, where we may not want to update all fields of the expense.
    amount: Annotated[Optional[float], Field(description="The amount of the expense", example=100.0, default=None)]
    date: Annotated[Optional[str], Field(description="The date of the expense", example='2023-01-01', default=None)]
    category: Annotated[Optional[str], Field(description="The category of the expense", example='Food', default=None)]
    description: Annotated[Optional[str], Field(description="The description of the expense", example='Lunch at restaurant', default=None)]


app = FastAPI() 

@app.get("/view")      # Load all the expenses from the database      # http://127.0.0.1:8000/view
def view_expense():
    return load_data()

# Find Specific Expense by ID
@app.get("/view/{expense_id}")           # http://127.0.0.1:8000/view/E008
def view_specific_expense(expense_id: str = Path(...,description="The ID of the expense to retrieve", example='E001')):      # here ... means that the expense_id is a required parameter and it will be passed in the URL path. The description and example are used for documentation purposes.
    data = load_data()
    if expense_id in data: 
        return data[expense_id] 
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


# Sorted by name, amount, date, category (ascending or descending order) 
@app.get("/sort")          # http://127.0.0.1:8000/sort?sorted_by=amount&order=desc
def view_sorted_expense(sorted_by: str, order: str):
    data = load_data()  
    sorted_data = list(data.values())
    if order == "asc":
        sorted_data.sort(key=lambda x: x[sorted_by], reverse=False)
    elif order == "desc":
        sorted_data.sort(key=lambda x: x[sorted_by], reverse=True)

    return sorted_data 




# Create 
# post, put, delete --> here can't request view
@app.post("/create")  # Ekhon Input er onek gulo data thakbe, tai amra Pydantic model use korbo. Ekhane amra Expense class ke use korbo, ja amader input data ke validate korbe.
def create_expense(expense: Expense):    # Expense class er object hisebe expense parameter ke receive korbo. Ekhane amra Expense class er object ke use kore input data ke validate korbo.
    data = load_data()
    if expense.id in data:  # Check if the expense ID already exists in the data. If it does, raise an HTTPException with a 400 status code and a message indicating that the expense ID already exists.
        raise HTTPException(status_code=400, detail="Expense ID already exists")
    data[expense.id] = expense.model_dump(exclude=['id'])   # model_dump() method is used to convert the Pydantic model instance into a dictionary. The exclude parameter is used to exclude the id field from the dictionary, since we don't want to store it in the JSON file.
    save_data(data)                                          # exclude=['id'] means that the id field will not be included in the dictionary representation of the Expense object. This is because we are using the id as the key in the JSON file, so we don't need to store it as a separate field in the value.
# Corner Case ager Data gulo ke override kore felse ei way te


#update
@app.put("/edit/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")
    data[expense_id].update(expense.model_dump(exclude_unset=True)) # only update the fields that are provided in the request. The exclude_unset parameter is used to exclude any fields that are not provided in the request, so that they are not overwritten with None values.
    save_data(data)
    return {"message": "Expense updated successfully"}



# Delete
@app.delete("/delete/{expense_id}")
def delete_expense(expense_id: str):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")
    del data[expense_id]
    save_data(data)
    return {"message": "Expense deleted successfully"}


# uvicorn main:app --reload  
# http://127.0.0.1:8000/docs