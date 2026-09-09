

CRUD
--> Data Create er age data validation korte hobe
validation korar jonno pydantic library ja data validation er jonno kaaj kore 


from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field # Used for data validation and serialization
from typing import Annotated  # Used for type hinting and validation



def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4) # josn.dump() function is used to write the data to the file in JSON format. The indent parameter is used to format the JSON data with indentation for better readability.


# Validation korar jonno Class
class Expense(BaseModel):
    id: Annotated[str, Field(..., description="The unique ID of the expense", example='E001')]  # Annotated is used to provide additional metadata for the field, such as description and example.
    name: Annotated[str, Field(..., description="The name of the expense", example='Lunch')]
    amount: Annotated[float, Field(..., description="The amount of the expense", example=100.0)]
    date: Annotated[str, Field(..., description="The date of the expense", example='2023-01-01')]
    category: Annotated[str, Field(..., description="The category of the expense", example='Food')]
    description: Annotated[str, Field(..., description="The description of the expense", example='Lunch at restaurant')]



# Create 
@app.post("/create")  # Ekhon Input er onek gulo data thakbe, tai amra Pydantic model use korbo. Ekhane amra Expense class ke use korbo, ja amader input data ke validate korbe.
def create_expense(expense: Expense):    # Expense class er object hisebe expense parameter ke receive korbo. Ekhane amra Expense class er object ke use kore input data ke validate korbo.
    data = load_data()
    data[expense.id] = expense.model_dump(exclude=['id'])   # model_dump() method is used to convert the Pydantic model instance into a dictionary. The exclude parameter is used to exclude the id field from the dictionary, since we don't want to store it in the JSON file.
    save_data(data)    

# UPDATE kon id and konta change korte hobe
Put request can't view , view only works on get request
Update existing data 
#update
@app.put("/edit/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")
    data[expense_id].update(expense.model_dump(exclude_unset=True))  #"exclude_unset=True eta r kaaj oi gulo kei include kore jegula user diyeche
    save_data(data)
    return {"message": "Expense updated successfully"}




# Used for update request, jekhane amra optional field use korbo, karon update request e sob gulo field thakbe na. Tai amra Optional type use korbo.
class ExpenseUpdate(BaseModel):
    name: Annotated[Optional[str], Field(description="The name of the expense", example='Lunch', default=None)]    # Default value None means that if the field is not provided in the input data, it will be set to None. This is useful for update requests, where we may not want to update all fields of the expense.
    amount: Annotated[Optional[float], Field(description="The amount of the expense", example=100.0, default=None)]
    date: Annotated[Optional[str], Field(description="The date of the expense", example='2023-01-01', default=None)]
    category: Annotated[Optional[str], Field(description="The category of the expense", example='Food', default=None)]
    description: Annotated[Optional[str], Field(description="The description of the expense", example='Lunch at restaurant', default=None)]
 



# Update
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





# Database Connect and Deploy
--> sqlalchemy
-->sqlite3
--> Postgress
--> mysql
# ToDo Application using fastapi