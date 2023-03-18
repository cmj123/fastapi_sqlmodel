from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from models import Category
from database import engine 

# Define main app name and database session name
app = FastAPI()
session = Session(bind=engine)

# Routes
# Root folder (home page)
@app.get(/)

# Get all categories
@app.get('/category')

# Post a new category 
@app.post('/category')

# Get a specific category
@app.get('/category/{category_id}')

# Update a specific category
@app.put('/category/{category_id}')

# Delete a specific category
@app.delete('/category/{category_id}')