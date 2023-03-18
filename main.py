from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Session
from models import Category
from database import engine 

# Define main app name and database session name
app = FastAPI()
session = Session(bind=engine)

# Routes
# Root folder (home page)
@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <h1>Home Page</h1>
    <a href='http://127.0.0.1:8000/docs'>http://127.0.0.1:8000/docs</a>
    '''

# Get all categories
@app.get('/category')
async def get_all_categories():
    pass

# Post a new category 
@app.post('/category')
async def post_a_category():
    pass

# Get a specific category
@app.get('/category/{category_id}')
async def get_a_category(category_id:int):
    pass

# Update a specific category
@app.put('/category/{category_id}')
async def update_a_category(category_id:int):
    pass

# Delete a specific category
@app.delete('/category/{category_id}')
async def delete_a_category(category_id:int):
    pass