# InjamTanvir(INJAM UL HAQUE)

# Instal packages `uv pip install fastapi uvicorn`

from fastapi import FastAPI # Import FastAPI class from the fastapi module.

app = FastAPI() # Create a FastAPI instance named app. This instance will be used to define the API endpoints and handle incoming requests.

# Making API endpoint or Root URL
@app.get("/") # Decorator @app.get("/") is used to define a GET endpoint for the root URL ("/"). When a client sends a GET request to this URL, the function below it will be executed. # if we go to this url below function will be called.
# http://127.0.0.1:8000/
def view(): # ei url ey gel hello world print hobe # The function view() is defined to handle the GET request. When this endpoint is accessed, it will return the string "Hello World".
    return "Hello World"

# uvicorn main:app --reload      # Run the server using this command in terminal gives a live url link to test the API endpoint. The --reload flag allows the server to automatically reload when code changes are made.

@app.get("/view")   # http://127.0.0.1:8000/view
def view(): # Print Hello Tanvir on this URL  # The function view() is defined to handle the GET request. When this endpoint is accessed, it will return the string "Hello Tanvir".
    return "Hello Tanvir"


@app.get("/about")     # http://127.0.0.1:8000/about
def view(): # There "This is our about page" will be print # The function view() is defined to handle the GET request. When this endpoint is accessed, it will return the string "This is our about page".
    return "This is our about page"

# FastApi have automatic Documentation  so type /docs in the url and you will see the documentation of your API endpoints.
# http://127.0.0.1:8000/docs
