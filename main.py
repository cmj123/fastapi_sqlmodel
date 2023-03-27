from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Session, select
from models import Category, CategoryBase
from database import engine 
import uvicorn
from typing import List

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
@app.get('/category', response_model=List[Category])
async def get_all_categories():
    with Session(engine) as session:
        statement = select(Category)
        result = session.exec(statement)
        all_categories = result.all()
    return all_categories

# Post a new category 
@app.post('/category', status_code=status.HTTP_201_CREATED)
async def post_a_category(category:CategoryBase):
    new_category = Category(name=category.name)
    with Session(engine) as session:
        # See if that category name is already in the table
        statement = select(Category).where(Category.name == category.name)
        # Reject if name already in use
        if session.exec(statement).one_or_none():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Category name already in use')
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
    return new_category

# Get a specific category
@app.get('/category/{category_id}',response_model=Category)
async def get_a_category(category_id:int):
    with Session(engine) as session:
        # Alternative syntax when getting one row by id
        category = session.get(Category, category_id)
        # Return error if no such category
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category")
    return category

# Update a specific category
@app.put('/category/{category_id}', response_model=Category)
async def update_a_category(category_id:int, category:CategoryBase):
    with Session(engine) as session:
        # Get current category object from table
        current_category = session.get(Category, category_id)
        # Replace current category name with the one just passed in
        current_category.name = category.name
        # Put back in table with new name
        session.add(current_category)
        session.commit()
        session.refresh(current_category)
    return current_category


# Delete a specific category
@app.delete('/category/{category_id}',)
async def delete_a_category(category_id:int):
    with Session(engine) as session:
        # Get the category to delete
        category = session.get(Category, category_id)
        # Delete the category
        session.delete(category)
        session.commit()
    return {'Deleted':category_id}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)