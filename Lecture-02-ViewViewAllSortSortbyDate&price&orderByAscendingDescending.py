# InjamTanvir(INJAM UL HAQUE)

# Expense Tracker API using FastAPI connected with Dummy Database(expenses.json) and CRUD Operations
import json
from fastapi import FastAPI, HTTPException, Path


def load_data(): # Load the data from the expenses.json file
    with open("expenses.json", "r") as file:   # read mode to open the expenses.json file
        data = json.load(file)
    return data

app = FastAPI() # Create a FastAPI instance named app. This instance will be used to define the API endpoints and handle incoming requests.


@app.get("/view")  # Load all the expenses from the database  # http://127.0.0.1:8000/view
def view_expense():
    return load_data()

# Use path parameter to get a specific expense by id
@app.get("/view/{expense_id}")  # Load a specific expense by id     # http://127.0.0.1:8000/view/E008
def view_specific_expense(expense_id: str = Path(...,description="The ID of the expense to retrieve", example='E001')):      # here ... means that the expense_id is a required parameter and it will be passed in the URL path. The description and example are used for documentation purposes.
    data = load_data() # load the data from the expenses.json file
    if expense_id in data:  # check if the expense_id exists in the data
        return data[expense_id]  # simply return the expense data if it exists
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/sort")  # Sort the expenses by amount in ascending or descending order based on the query parameters sorted_by and order.
def view_sorted_expense(sorted_by: str, order: str):  # http://127.0.0.1:8000/sort?sorted_by=amount&order=desc
    data = load_data()  # load the data from the expenses.json file
    sorted_data = list(data.values())  # convert the data to a list of values
    if order == "asc":
        sorted_data.sort(key=lambda x: x[sorted_by], reverse=False)  # sort the data by amount in ascending order
    elif order == "desc":
        sorted_data.sort(key=lambda x: x[sorted_by], reverse=True)  # sort the data by amount in descending order

    return sorted_data  # return the sorted data



# uvicorn main:app --reload  
